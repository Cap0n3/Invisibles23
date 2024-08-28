from django.shortcuts import render
from django.views import View
from website.models import Event, Participant, EventParticipants
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
from .utils.helpers import sendEmail, find_key_in_dict

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
    This view handles the subscription to the mailing list. It uses the Mailchimp API to add a new member to the list.
    """
    http_method_names = ["post"]  # Only POST requests are allowed
    server_prefix = "us21"
    mailchimp_api_key = env("MAILCHIMP_API_KEY")
    list_id = env("MAILCHIMP_LIST_ID")

    def post(self, request):
        email = request.POST.get("email")
        test_status = request.POST.get("test_status")
        test_status = int(test_status) if test_status != "null" else None

        if not email:
            return HttpResponseBadRequest("Email is required")

        member_info = {"email_address": email, "status": "subscribed"}

        # Mailchimp API endpoint
        try:
            if test_status and isinstance(test_status, int):
                # Simulating a test error with custom status code and error message
                raise ApiClientError("An error occurred", status_code=test_status)

            client = MailchimpMarketing.Client()
            client.set_config(
                {"api_key": self.mailchimp_api_key, "server": self.server_prefix}
            )
            response = client.lists.add_list_member(self.list_id, member_info)
            print("response: {}".format(response))

            return JsonResponse(
                {
                    "message": "You have successfully subscribed to our mailing list.",
                },
                status=200,
            )
        except ApiClientError as error:
            # Same with f string
            print(f"An exception occurred: {error.text}")

            return JsonResponse(
                {
                    "message": f"An error occurred: {error.text}",
                },
                status=error.status_code,
            )


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhook(View):
    """
    Stripe webhook handler for event registration payments.
    """

    http_method_names = ["post"]  # Only POST requests are allowed
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Your custom initialization code here
        self.owner_email = settings.DEV_EMAIL if (settings.DEBUG) else settings.OWNER_EMAIL
        self.member_id = None
        self.member_name = None
        self.member_email = None
        self.member_country = None
        self.member_invoice_url = None
        self.member_plan = None
        self.customer_name = None
        self.customer_email = None
        self.customer_country = None
        self.meeting_id = None
        self.meeting = None
        self.data = None
        self.metadata = None
        self.event_type = None
    
    
    def post(self, request) -> HttpResponse:
        """
        Handle the POST request for the Stripe webhook.
        """ 
        logger.info("Stripe event registration webhook initiated ...")

        try:
            payload = request.body
            sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
            stripe_secret = env("STRIPE_WEBHOOK_SECRET")
            stripe.api_key = env("STRIPE_API_TOKEN")
            event = stripe.Webhook.construct_event(payload, sig_header, stripe_secret)
            self.event_type = event["type"]
            
            log_debug_info(f"Event type: {self.event_type}")
            #log_debug_info("Event data", event["data"])
            
            # Get metadata from event data
            self.data = event["data"]
            self._extract_metadata()
            registration_type = None
            
            if self.metadata:
                log_debug_info("Extracted metadata : ", self.metadata)
                logger.info(f"Registration type: {self.metadata['type']}")
                registration_type = self.metadata["type"]
            
            if self.event_type == "checkout.session.completed" and registration_type == "talk-group":
                self.handle_talk_group()
            elif self.event_type == "invoice.paid" and registration_type == "membership":
                self.handle_membership()
            elif self.event_type == "payment_intent.payment_failed":
                logger.warning(f"[EVENT] Payment failed event initiated for {self.metadata['type'] if self.metadata else None}: {self.metadata}")
            elif self.event_type == "invoice.payment_failed":
                logger.warning(f"[EVENT] Invoice payment failed event initiated for {self.metadata['type'] if self.metadata else None}: {self.metadata}")
            else:
                logger.warning(f"Unhandled event type: {event['type']}")

            return HttpResponse(status=200)

        except ValueError as e:
            logger.error(f"Invalid payload: {str(e)}")
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature: {str(e)}")
            return HttpResponse(status=403)
        except Exception as e:
            logger.error(f"Unexpected error in webhook: {str(e)}")
            return HttpResponse(status=500)
        
    
    def handle_membership(self) -> None:
        """
        Subroutine to handle the membership subscription.
        """        
        try:
            # Extract member data from the event data
            self._extract_member_data()

            stripe.Customer.modify(
                self.member_id,
                metadata={
                    "name": self.metadata["name"],
                    "birthday": self.metadata["birthday"],
                    "customer_email": self.metadata["customer_email"],
                    "phone": self.metadata["phone"],
                    "address": self.metadata["address"],
                    "zip_code": self.metadata["zip_code"],
                    "city": self.metadata["city"],
                    "country": self.member_country,
                },
            )
            
            self._log_event()
            self._send_membership_alerts()
            
        except ValueError as e:
            logger.error(f"Invalid data in webhook payload: {str(e)}")
            raise ValueError("Invalid data in webhook payload")
        except Exception as e:
            logger.error(f"Error processing membership event: {str(e)}")
            raise Exception("Error processing membership event")
        else:
            logger.info("Membership subscription event completed.")
        finally:
            self._subscribe_to_mailing_list()
                
    
    def handle_talk_group(self) -> None:
        """
        Subroutine to handle the checkout for talk group event.
        """
        logger.info("[EVENT] Checkout completed event initiated ...")

        try:        
            self._extract_customer_data()
            self._create_and_associate_participant_with_event()
            self._log_event()
            self._send_event_registration_alerts()

        except ObjectDoesNotExist as e:
            logger.error(f"Event not found: {str(e)}")
        except ValueError as e:
            logger.error(f"Invalid data in webhook payload: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing checkout completed event: {str(e)}")

    
    def _extract_member_data(self) -> None:
        """
        Extract member data from the event data (only for membership subscription)(setter).
        """
        
        self.member_id = find_key_in_dict(self.data["object"], "customer")
        self.member_name = find_key_in_dict(self.data["object"], "customer_name")
        self.member_email = find_key_in_dict(self.data["object"], "customer_email")
        self.member_country = find_key_in_dict(self.data["object"], "country")
        self.member_invoice_url = find_key_in_dict(self.data["object"], "hosted_invoice_url")
        self.member_plan = self.data["object"]["lines"]["data"][0]["description"]

        missing_fields = []

        if not self.member_id:
            missing_fields.append("member_id")
        if not self.member_name:
            missing_fields.append("member_name")
        if not self.member_email:
            missing_fields.append("member_email")
        if not self.member_country:
            missing_fields.append("member_country")
        if not self.member_invoice_url:
            missing_fields.append("member_invoice_url")
        if not self.member_plan:
            missing_fields.append("member_plan")

        if missing_fields:
            raise ValueError(f"Missing member data in event payload: {', '.join(missing_fields)}")

            
    def _extract_customer_data(self) -> None:
        """
        Extract customer data from the event data (only for event registration)(setter).
        """
        self.customer_name = find_key_in_dict(self.data["object"]["customer_details"], "name")
        self.customer_email = find_key_in_dict(
            self.data["object"]["customer_details"], "email"
        )
        self.customer_country = find_key_in_dict(
            self.data["object"]["customer_details"], "country"
        )
        self.meeting_id = self.metadata.get("event_id")

        missing_fields = []
        
        if not self.customer_name:
            missing_fields.append("customer_name")
        if not self.customer_email:
            missing_fields.append("customer_email")
        if not self.customer_country:
            missing_fields.append("customer_country")
        if not self.meeting_id:
            missing_fields.append("meeting_id")

        if missing_fields:
            raise ValueError(f"Missing customer data in event payload: {', '.join(missing_fields)}")

    
    def _extract_metadata(self) -> None:
        """
        Extract metadata from the event data based on the event type (setter).
        """
        log_debug_info(f"Event type: {self.event_type}")
        
        if self.event_type in ["checkout.session.completed", "payment_intent.payment_failed"]:
            self.metadata = find_key_in_dict(self.data["object"], "metadata")
        elif self.event_type in ["invoice.paid", "invoice.payment_failed"]:
            self.metadata = find_key_in_dict(self.data["object"]["lines"]["data"][0], "metadata")
        
    
    def _create_and_associate_participant_with_event(self) -> None:
        """
        This method creates a new participant if they do not already exist in the database and associates them with the event.
        """
        self.meeting = Event.objects.get(id=self.meeting_id)
        logger.info(f"Extracted all data for event registration: {self.meeting}")

        participant, created = Participant.objects.get_or_create(
            email=self.customer_email,
            defaults={
                "fname": self.metadata["fname"],
                "lname": self.metadata["lname"],
                "email": self.metadata["customer_email"],
                "phone": self.metadata["phone"],
                "address": self.metadata["address"],
                "zip_code": self.metadata["zip_code"],
                "city": self.metadata["city"],
            },
        )

        logger.info(
            f"{'New' if created else 'Existing'} participant: {participant}"
        )

        # Associate the participant with the event
        EventParticipants.objects.create(event=self.meeting, participant=participant)
        logger.info(f"Participant {participant} registered for event {self.meeting}")
    
    
    def _send_membership_alerts(self) -> None:
        """
        Send email alerts to the member and owner after a successful membership subscription.
        """
        # Sending confirmation to member
        sendEmail(
            self.member_email,
            "Confirmation d'adhésion à l'association Les Invisibles",
            "adhesion_email.html",
            {
                "name": self.member_name,
            },
        )

        sendEmail(
            self.member_email,
            "Reçu de paiement adhésion",
            "invoice_email.html",
            {
                "name": self.member_name,
                "email": self.member_email,
                "invoice_url": self.member_invoice_url,
                "customer_id": self.member_id,
                "membership_plan": self.member_plan,
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
                "name": self.member_name,
                "email": self.member_email,
                "country": self.member_country,
            },
        )

        sendEmail(
            self.owner_email,
            "Reçu de paiement adhésion",
            "invoice_email_accounting.html",
            {
                "name": self.member_name,
                "email": self.member_email,
                "invoice_url": self.member_invoice_url,
                "customer_id": self.member_id,
                "membership_plan": self.member_plan,
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
                "email": self.metadata["customer_email"],
                "phone": self.metadata["phone"],
                "address": self.metadata["address"],
                "zip_code": self.metadata["zip_code"],
                "city": self.metadata["city"],
                "event_title": self.meeting.title,
                "event_date": self.meeting.date.strftime("%d/%m/%Y"),
                "event_start_time": self.meeting.start_time.strftime("%H:%M"),
                "event_end_time": self.meeting.end_time.strftime("%H:%M"),
            },
        )

        # Sending confirmation to participant
        sendEmail(
            self.customer_email,
            "Confirmation d'inscription à un groupe de parole",
            "event_confirmation_email.html",
            {
                "fname": self.metadata["fname"],
                "lname": self.metadata["lname"],
                "event_title": self.meeting.title,
                "event_date": self.meeting.date.strftime("%d/%m/%Y"),
                "event_start_time": self.meeting.start_time.strftime("%H:%M"),
                "event_end_time": self.meeting.end_time.strftime("%H:%M"),
            },
        )
    
    
    def _subscribe_to_mailing_list(self) -> None:
        """
        Subscribe the member to the mailing list (Mailchimp).
        """
        try:
            # Use mailchimp proxy to add member to mailing list
            logger.info("Adding member to mailing list ...")
            mailchimp_data = {
                "email": self.member_email,
                "test_status": None,
            }
            response = requests.post(reverse("mailchimp-proxy"), data=mailchimp_data)
            
            logger.info(f"Mailchimp response: {response}")
        except Exception as e:
            logger.error(f"Error adding member to mailing list: {str(e)}")


    def _log_event(self) -> None:
        """
        Log event data and metadata.
        """
        if self.event_type == "invoice.paid":
            logger.info(f"Invoice paid for: customer ID {self.member_id}")
            logger.info(f"Member name: {self.member_name}, email: {self.member_email}, country: {self.member_country}, plan: {self.member_plan}")
            logger.info(f"Invoice URL: {self.member_invoice_url}")
            log_debug_info("Event data for invoice paid:", self.data)
            log_debug_info("Metadata for customer:", self.metadata)
            logger.info("Updating customer metadata ...")
        elif self.event_type == "checkout.session.completed":
            logger.info(f"Checkout completed for: event ID {self.meeting_id}")
            logger.info(f"Customer name: {self.customer_name}, email: {self.customer_email}, country: {self.customer_country}")
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
