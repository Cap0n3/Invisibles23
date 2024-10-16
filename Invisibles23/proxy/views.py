from django.views import View
from website.models import Members, MembershipPlans, Event, Participant, EventParticipants
from Invisibles23.logging_config import logger
from Invisibles23.logging_utils import log_debug_info
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import environ
import requests
import stripe
from datetime import datetime
from .utils.helpers import (
    sendEmail,
    find_key_in_dict,
    mailchimp_add_subscriber,
    format_birthdate_for_mailchimp,
)

# Read the .env file
env = environ.Env()
env.read_env("../.env")


class GetAPISecrets(View):
    http_method_names = ["post"]  # Only POST requests are allowed

    def post(self, request):
        logger.info("Getting API secrets...")

        data = {
            "ausha_api_token": env("AUSHA_API_TOKEN"),
            "mailchimp_api_key": env("MAILCHIMP_API_KEY"),
            "mailchimp_list_id": env("MAILCHIMP_LIST_ID"),
            "emailjs_service_id": env("EMAILJS_SERVICE_ID"),
            "emailjs_template_id": env("EMAILJS_TEMPLATE_ID"),
            "emailjs_user_id": env("EMAILJS_USER_ID"),
        }

        return JsonResponse(data)


class AushaProxy(View):
    http_method_names = ["post"]  # Only POST requests are allowed
    ausha_api_key = env("AUSHA_API_TOKEN")

    def post(self, request):
        show_id = request.POST.get("show_id")

        if not show_id:
            return HttpResponseBadRequest("Show ID is required")

        url = f"https://developers.ausha.co/v1/shows/{show_id}/podcasts"

        # Send a request to Ausha API
        try:
            response = requests.get(
                url,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.ausha_api_key}",
                },
            )
            return JsonResponse(response.json(), safe=False)
        except Exception as error:
            print(f"An exception occurred: {error}")
            return JsonResponse(
                {
                    "message": f"An error occurred: {error}",
                },
                status=500,
            )


class MailchimpProxy(View):
    """
    This view handles all subscription requests sent by the newsletter subscription form (frontend).
    """

    http_method_names = ["post"]  # Only POST requests are allowed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mailchimp_api_key = env("MAILCHIMP_API_KEY")
        self.list_id = env("MAILCHIMP_LIST_ID")
        self.subscriber_email = None

    def post(self, request):
        logger.info("MailchimpProxy initiated ...")
        self.subscriber_email = request.POST.get("email")
        logger.info(
            f"A person subscribed to the newsletter through the website form: {self.subscriber_email}"
        )
        self._handle_test_status(request)

        if not self.subscriber_email:
            logger.error("No email provided for newsletter subscription")
            return HttpResponseBadRequest("Email is required")

        member_info = {
            "email_address": self.subscriber_email,
            "status": "subscribed",
            "tags": ["Abonné"],
        }

        # Mailchimp API endpoint
        response = mailchimp_add_subscriber(
            self.mailchimp_api_key,
            "us9" if settings.DEBUG else "us21",
            self.list_id,
            member_info,
        )

        return response

    def _handle_test_status(self, request):
        """
        To easily test the error handling in frontend, this method simulates an error based on the test_status parameter.

        Example:
        - test_status=400: Simulates a 400 Bad Request error
        - test_status="null": No error, normal behavior
        """
        test_status = request.POST.get("test_status")
        if test_status and test_status != "null":
            test_status = int(test_status)
            raise ApiClientError("An error occurred", status_code=test_status)


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhook(View):
    """
    Stripe webhook handler for event registration payments.
    """

    http_method_names = ["post"]  # Only POST requests are allowed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = None
        self.csrf_token = None
        self.owner_email = (
            settings.DEV_EMAIL if (settings.DEBUG) else settings.OWNER_EMAIL
        )
        self.customer_id = None
        self.customer_name = None
        self.customer_email = None
        self.customer_country_code = None
        self.customer_invoice_url = None
        self.customer_subscription_plan = None
        self.plan_lookup_key = None
        self.meeting_id = None
        self.meeting = None
        self.talk_event_link = None
        self.data = None
        self.metadata = None
        self.event_type = None

    def post(self, request) -> HttpResponse:
        """
        Handle the POST request for the Stripe webhook.
        """
        logger.info("Stripe event registration webhook initiated ...")
        self.request = request
        try:
            payload = request.body
            sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
            stripe_secret = env("STRIPE_WEBHOOK_SECRET")
            stripe.api_key = env("STRIPE_API_TOKEN")
            event = stripe.Webhook.construct_event(payload, sig_header, stripe_secret)
            self.event_type = event["type"]

            log_debug_info(f"Event type: {self.event_type}")

            # Get metadata from event data
            self.data = event["data"]
            self._extract_metadata()
            registration_type = None

            if self.metadata:
                log_debug_info("Extracted metadata : ", self.metadata)
                logger.info(f"Registration type: {self.metadata['type']}")
                registration_type = self.metadata["type"]

            if (
                self.event_type == "checkout.session.completed"
                and registration_type == "talk-group"
            ):
                self.handle_talk_group()
            elif (
                self.event_type == "invoice.paid" and registration_type == "membership"
            ):
                self.handle_membership()
            elif self.event_type == "payment_intent.payment_failed":
                logger.warning(
                    f"[EVENT] Payment failed event initiated for {self.metadata['type'] if self.metadata else None}: {self.metadata}"
                )
            elif self.event_type == "invoice.payment_failed":
                logger.warning(
                    f"[EVENT] Invoice payment failed event initiated for {self.metadata['type'] if self.metadata else None}: {self.metadata}"
                )
            else:
                logger.warning(f"Unhandled event type: {event['type']}")

            return HttpResponse(status=200)

        except ValueError as e:
            logger.error(f"Invalid payload: {str(e)}")
            return HttpResponse(status=400)
        except Exception as e:
            logger.error(f"Unexpected error in webhook: {str(e)}")
            return HttpResponse(status=500)

    def handle_membership(self) -> None:
        """
        Subroutine to handle the membership subscription. It updates the member's metadata and sends email alerts
        Note : Updating is the only way I found to transmit the metadata to stripe
        """
        try:
            # Extract member data from the event data
            self._extract_customer_data()
            
            # Get the right membership plan with lookup key
            logger.info(f"Getting membership plan from database with lookup key: {self.plan_lookup_key}")
            member_plan = MembershipPlans.objects.get(lookup_key=self.plan_lookup_key)
            
            # Add member to Members database if not already present
            logger.info(f"Adding member to database: {self.metadata['name']}")
            obj, created = Members.objects.update_or_create(
                email=self.customer_email,
                defaults={
                    "fname": self.metadata["name"].split(" ")[0],
                    "lname": self.metadata["name"].split(" ")[1],
                    "email": self.customer_email,
                    "phone": self.metadata["phone"],
                    "birthdate": self.metadata["birthday"],
                    "address": self.metadata["address"],
                    "zip_code": self.metadata["zip_code"],
                    "city": self.metadata["city"],
                    "country": self.metadata["country"],
                    "membership_plan": member_plan,
                },
            )
            
            if created:
                logger.info(f"New member added to database: {obj}")
            else:
                logger.warning(f"Member already exists in database, information updated.")

            # Update the member's metadata in Stripe
            logger.info("Updating customer metadata on Stripe ...")
            stripe.Customer.modify(
                self.customer_id,
                metadata={
                    "name": self.metadata["name"],
                    "birthday": self.metadata["birthday"],
                    "email": self.metadata["email"],
                    "phone": self.metadata["phone"],
                    "address": self.metadata["address"],
                    "zip_code": self.metadata["zip_code"],
                    "city": self.metadata["city"],
                    "country": self.metadata["country"],
                },
            )

            self._log_event()

        except ValueError as e:
            logger.error(f"Invalid data in webhook payload: {str(e)}")
            raise ValueError("Invalid data in webhook payload")
        except ObjectDoesNotExist as e:
            logger.error(f"Membership plan not found: {str(e)}")
            raise ObjectDoesNotExist("Membership plan not found")
        except Exception as e:
            logger.error(f"Error processing membership event: {str(e)}")
            raise Exception("Error processing membership event")
        else:
            logger.info("Membership subscription event completed.")
            self._send_membership_alerts()
        finally:
            self._subscribe_to_mailing_list()

    def handle_talk_group(self) -> None:
        """
        Subroutine to handle the checkout for talk group event.
        """
        logger.info("[EVENT] Checkout completed event initiated ...")

        try:
            #self._extract_customer_data()
            self._extract_meeting_id()
            self._create_and_associate_participant_with_event()
            self._get_talk_event_zoom_link()
            self._log_event()
        except ObjectDoesNotExist as e:
            logger.error(f"Event not found: {str(e)}")
        except ValueError as e:
            logger.error(f"Invalid data in webhook payload: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing checkout completed event: {str(e)}")
        else:
            logger.info("Checkout completed event completed.")
            self._send_event_registration_alerts()

    def _extract_customer_data(self) -> None:
        """
        Extract customer data from the event data (only for membership subscription)(setter).
        """

        self.customer_id = find_key_in_dict(self.data["object"], "customer")
        self.customer_name = find_key_in_dict(self.data["object"], "customer_name")
        self.customer_email = find_key_in_dict(self.data["object"], "customer_email")
        self.customer_country_code = find_key_in_dict(self.data["object"], "country")
        self.customer_invoice_url = find_key_in_dict(
            self.data["object"], "hosted_invoice_url"
        )
        self.customer_subscription_plan = self.data["object"]["lines"]["data"][0]["description"]
        self.plan_lookup_key = self.data["object"]["lines"]["data"][0]["price"]["lookup_key"]

        missing_fields = []

        if not self.customer_id:
            missing_fields.append("customer_id")
        if not self.customer_name:
            missing_fields.append("customer_name")
        if not self.customer_email:
            missing_fields.append("customer_email")
        if not self.customer_country_code:
            missing_fields.append("customer_country_code")
        if not self.customer_invoice_url:
            missing_fields.append("customer_invoice_url")
        if not self.customer_subscription_plan:
            missing_fields.append("customer_subscription_plan")
        if not self.plan_lookup_key:
            missing_fields.append("plan_lookup_key")

        if missing_fields:
            raise ValueError(
                f"Missing member data in event payload: {', '.join(missing_fields)}"
            )
        logger.info(
            f"Customer data extracted: {self.customer_name}, {self.customer_email}, {self.customer_subscription_plan}, {self.customer_country_code}, {self.customer_id}"
        )

    def _extract_metadata(self) -> None:
        """
        Extract metadata from the event data based on the event type (setter).
        """
        log_debug_info(f"Event type: {self.event_type}")

        if self.event_type in [
            "checkout.session.completed",
            "payment_intent.payment_failed",
        ]:
            self.metadata = find_key_in_dict(self.data["object"], "metadata")
        elif self.event_type in ["invoice.paid", "invoice.payment_failed"]:
            self.metadata = find_key_in_dict(
                self.data["object"]["lines"]["data"][0], "metadata"
            )

    def _extract_meeting_id(self) -> None:
        """
        Extract the meeting ID from the event data (setter).
        Note: This method must be called after extracting metadata.
        """
        self.meeting_id = self.metadata.get("event_id")
        if not self.meeting_id:
            raise ValueError("Meeting ID not found in metadata")
    
    def _create_and_associate_participant_with_event(self) -> None:
        """
        This method creates a new participant if they do not already exist in the database and associates them with the event.
        """
        self.meeting = Event.objects.get(id=self.meeting_id)
        logger.info(f"Extracted all data for event registration: {self.meeting}")

        participant, created = Participant.objects.get_or_create(
            email=self.metadata["email"],
            defaults={
                "fname": self.metadata["fname"],
                "lname": self.metadata["lname"],
                "email": self.metadata["email"],
                "phone": self.metadata["phone"],
                "address": self.metadata["address"],
                "zip_code": self.metadata["zip_code"],
                "city": self.metadata["city"],
            },
        )

        logger.info(f"{'New' if created else 'Existing'} participant: {participant}")

        # Associate the participant with the event
        EventParticipants.objects.create(event=self.meeting, participant=participant)
        logger.info(f"Participant {participant} registered for event {self.meeting}")

    def _get_talk_event_zoom_link(self) -> str:
        """
        Get the Zoom link for the talk event from the Event
        """
        zoom_link = Event.objects.get(id=self.meeting_id).talk_event_link
        if not zoom_link:
            logger.error("No Zoom link found for the event, clean() verification failed to catch this")
        
        self.talk_event_link = zoom_link
    
    def _send_membership_alerts(self) -> None:
        """
        Send email alerts to the member and owner after a successful membership subscription.
        """
        # Sending confirmation to member
        logger.info(
            f"Sending notification and invoice to member at {self.customer_email} ..."
        )
        sendEmail(
            self.customer_email,
            "Confirmation d'adhésion à l'association Les Invisibles",
            "adhesion_email.html",
            {
                "name": self.customer_name,
            },
        )

        sendEmail(
            self.customer_email,
            "Reçu de paiement adhésion",
            "invoice_email.html",
            {
                "name": self.customer_name,
                "email": self.customer_email,
                "invoice_url": self.customer_invoice_url,
                "customer_id": self.customer_id,
                "membership_plan": self.customer_subscription_plan,
            },
        )

        # Sending invoice to owner
        logger.info(
            f"Sending notification and invoice to owner at {self.owner_email} ..."
        )

        sendEmail(
            self.owner_email,
            "Un nouveau membre a rejoint l'association Les Invisibles",
            "adhesion_notification.html",
            {
                "name": self.customer_name,
                "email": self.customer_email,
                "country": self.customer_country_code,
            },
        )

        sendEmail(
            self.owner_email,
            "Reçu de paiement adhésion",
            "invoice_email_accounting.html",
            {
                "name": self.customer_name,
                "email": self.customer_email,
                "invoice_url": self.customer_invoice_url,
                "customer_id": self.customer_id,
                "membership_plan": self.customer_subscription_plan,
            },
        )

    def _send_event_registration_alerts(self) -> None:
        # Sending notification to owner
        sendEmail(
            self.owner_email,
            "Nouvelle inscription à un groupe de parole",
            "event_notification.html",
            {
                "fname": self.metadata["fname"],
                "lname": self.metadata["lname"],
                "email": self.metadata["email"],
                "phone": self.metadata["phone"],
                "address": self.metadata["address"],
                "zip_code": self.metadata["zip_code"],
                "city": self.metadata["city"],
                "event_title": self.meeting.title,
                "event_date": self.meeting.date.strftime("%d/%m/%Y"),
                "event_start_time": self.meeting.start_time.strftime("%H:%M"),
                "event_end_time": self.meeting.end_time.strftime("%H:%M"),
                "talk_event_link": self.talk_event_link,
            },
        )

        # Sending confirmation to participant
        sendEmail(
            self.metadata["email"],
            "Confirmation d'inscription à un groupe de parole",
            "event_confirmation_email.html",
            {
                "fname": self.metadata["fname"],
                "lname": self.metadata["lname"],
                "event_title": self.meeting.title,
                "event_date": self.meeting.date.strftime("%d/%m/%Y"),
                "event_start_time": self.meeting.start_time.strftime("%H:%M"),
                "event_end_time": self.meeting.end_time.strftime("%H:%M"),
                "talk_event_link": self.talk_event_link,
            },
        )

    def _subscribe_to_mailing_list(self) -> None:
        """
        Subscribe the member to the mailing list (Mailchimp).
        """
        logger.info("Subscribing member to the mailing list ...")
        try:
            member_info = {
                "email_address": self.customer_email,
                "status": "subscribed",
                "merge_fields": {
                    "FNAME": self.customer_name.split(" ")[0],
                    "LNAME": self.customer_name.split(" ")[1],
                    "ADDRESS": {
                        "addr1": self.metadata["address"],
                        "city": self.metadata["city"],
                        "state": "-",
                        "zip": self.metadata["zip_code"],
                        "country": self.customer_country_code, # only accepts country code
                    },
                    "PHONE": self.metadata["phone"],
                    "BIRTHDAY": format_birthdate_for_mailchimp(
                        self.metadata["birthday"]
                    ),
                },
                "tags": ["Membre"],
            }
            response = mailchimp_add_subscriber(
                env("MAILCHIMP_API_KEY"),
                "us9" if settings.DEBUG else "us21",
                env("MAILCHIMP_LIST_ID"),
                member_info,
            )
            logger.info(f"Mailchimp response status: {response.status_code}")
            logger.info(f"Mailchimp response message: {response.content}")
        except Exception as e:
            logger.error(f"Error subscribing member to the mailing list: {str(e)}")

    def _log_event(self) -> None:
        """
        Log event data and metadata.
        """
        if self.event_type == "invoice.paid":
            logger.info(f"Invoice paid for: customer ID {self.customer_id}")
            logger.info(
                f"Member name: {self.customer_name}, email: {self.customer_email}, country code: {self.customer_country_code}, plan: {self.customer_subscription_plan}"
            )
            logger.info(f"Invoice URL: {self.customer_invoice_url}")
            log_debug_info("Event data for invoice paid:", self.data)
            log_debug_info("Metadata for customer:", self.metadata)
            logger.info("Updating customer metadata ...")
        elif self.event_type == "checkout.session.completed":
            logger.info(f"Checkout completed for: event ID {self.meeting_id}")
            logger.info(
                f"Customer name: {self.metadata['fname']} {self.metadata['lname']}, email: {self.metadata['email']}, country: {self.metadata['country']}"
            )
            log_debug_info("Event data for payment:", self.data)


class EmailSender(View):
    http_method_names = ["post"]  # Only POST requests are allowed
    logger.info("EmailSender initialized ...")

    def post(self, request):
        # Get the form data
        fname = request.POST.get("first_name")
        lname = request.POST.get("last_name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        g_recaptcha_response = request.POST.get("recaptcha_token")

        # Verify reCAPTCHA
        if self.verifyRecaptchaV2(g_recaptcha_response):
            try:
                logger.info("Recaptcha verified. Sending email...")
                sendEmail(
                    settings.DEV_EMAIL if (settings.DEBUG) else settings.OWNER_EMAIL,
                    "Un nouveau message a été envoyé depuis le site web",
                    "contact_email.html",
                    {
                        "fname": fname,
                        "lname": lname,
                        "email": email,
                        "message": message,
                    },
                )

                return JsonResponse(
                    {
                        "message": "Email sent successfully.",
                    },
                    status=200,
                )

            except Exception as error:
                logger.error(f"An exception occurred: {error}")
                return JsonResponse(
                    {
                        "message": f"An error occurred: {error}",
                    },
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    "message": "reCAPTCHA verification failed.",
                },
                status=500,
            )

    def verifyRecaptchaV2(self, g_recaptcha_response):
        # Build POST request
        data = {
            "secret": env("RECAPTCHA_SECRET"),
            "response": g_recaptcha_response,
        }
        # Send request to Google
        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
        result = r.json()

        return result["success"]
