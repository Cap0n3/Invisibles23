from django.shortcuts import render
from django.views import View
from Invisibles23.logging_config import logger
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
import json
import environ
import requests
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .utils.helpers import sendEmail

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
    http_method_names = ["post"]  # Only POST requests are allowed

    def post(self, request):
        logger.info("Stripe webhook initiated ...")
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        stripe_secret = env("STRIPE_WEBHOOK_SECRET")
        event = None

        try:
            event = stripe.Event.construct_from(
                json.loads(payload), stripe_secret
            )
            data = event["data"]
        except ValueError as e:
            # Invalid payload
            logger.error("Invalid payload")
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            logger.error("Invalid signature")
            return HttpResponse(status=403)

        # Handle events
        if event["type"] == "checkout.session.completed":
            logger.info("Checkout session completed")

            # Log event data
            logger.debug(f"Event data: {data}")
            
            subscription_data = {
                "member_name": data["object"]["customer_details"].get("name", None),
                "member_email": data["object"]["customer_details"].get("email", None),
                "member_country": data["object"]["customer_details"]["address"].get("country", None),
            }

            # Log data
            logger.debug(f"Member name: {subscription_data['member_name']}")
            logger.debug(f"Member email: {subscription_data['member_email']}")
            logger.debug(f"Member country: {subscription_data['member_country']}")

            # Log metadata
            logger.info(f"Sending email to owner at {settings.OWNER_EMAIL} ...")

            # Send email to owner
            sendEmail(
                settings.DEV_EMAIL if (settings.DEBUG) else settings.OWNER_EMAIL,
                "Un nouveau membre a rejoint l'association Les Invisibles",
                "adhesion_notification.html",
                {
                    "name": subscription_data["member_name"],
                    "email": subscription_data["member_email"],
                    "country": subscription_data["member_country"],
                },
            )            
        
            logger.info(f"Sending email to member at {subscription_data['member_email']} ...")
            
            # Send email to member
            sendEmail(
                subscription_data["member_email"], 
                "Confirmation d'adhésion à l'association Les Invisibles", 
                "adhesion_email.html", 
                {
                    "name": subscription_data['member_name'],
                }
            )

        elif event["type"] == "invoice.paid":
            logger.info("Invoice paid")
            logger.debug(f"Event data for invoice paid : {event['data']}")
            
            invoice_data = {
                "member_name": data["object"]["customer_name"] if data["object"]["customer_name"] else None,
                "member_email": data["object"]["customer_email"] if data["object"]["customer_email"] else None,
                "customer_id": data["object"]["customer"] if data["object"]["customer"] else None,
                "invoice_url": data["object"]["hosted_invoice_url"] if data["object"]["hosted_invoice_url"] else None,
                "plan": data["object"]["lines"]["data"][0]["description"] if data["object"]["lines"]["data"][0]["description"] else None,
            }

            logger.debug(f"invoice_data: {invoice_data}")
            
            # Sending invoice to member
            logger.info(f"Sending invoice to member at {invoice_data['member_email']} ...")

            sendEmail(
                invoice_data['member_email'], 
                "Reçu de paiement adhésion", 
                "invoice_email.html", 
                {
                    "name": invoice_data["member_name"],
                    "email": invoice_data["member_email"],
                    "invoice_url": invoice_data["invoice_url"],
                    "customer_id": invoice_data["customer_id"],
                    "membership_plan": invoice_data["plan"],
                }
            )

            # Sending invoice to owner
            logger.info(f"Sending invoice to owner at {settings.OWNER_EMAIL} ...")

            sendEmail(
                settings.DEV_EMAIL if (settings.DEBUG) else settings.OWNER_EMAIL,
                "Reçu de paiement adhésion",
                "invoice_email_accounting.html",
                {
                    "name": invoice_data["member_name"],
                    "email": invoice_data["member_email"],
                    "invoice_url": invoice_data["invoice_url"],
                    "customer_id": invoice_data["customer_id"],
                    "membership_plan": invoice_data["plan"],
                },
            )
   
        elif event["type"] == "invoice.payment_failed":
            logger.warning("Payment failed - Sending back checkout link for payment.")
            logger.debug(f"Event data for payment failed : {event['data']}")

            # Send email to owner for payment failed
            sendEmail(
                settings.DEV_EMAIL if (settings.DEBUG) else settings.OWNER_EMAIL,
                "Erreur lors du paiement d'un abonnement",
                "payment_failed_notification.html",
                {
                    "name": data["object"]["customer_name"] if data["object"]["customer_name"] else None,
                    "email": data["object"]["customer_email"] if data["object"]["customer_email"] else None,
                    "customer_id": data["object"]["customer"] if data["object"]["customer"] else None,
                    "subscription_id": data["object"]["subscription"] if data["object"]["subscription"] else None,
                    "subcription_type": data["object"]["lines"]["data"][0]["description"] if data["object"]["lines"]["data"][0]["description"] else None,
                },
            )

            # === FIX 3D SECURE BEFORE RESENDING CHECKOUT LINK === #

            # Resend checkout link to member
            # sendEmail(
            #     data["object"]["customer_email"],
            #     "Invitation à reprendre le paiement",
            #     "payment_failed_email.html",
            #     {
            #         "name": data["object"]["customer_name"] if data["object"]["customer_name"] else None,
            #         "email": data["object"]["customer_email"] if data["object"]["customer_email"] else None,
            #         "checkout_url": data["object"]["hosted_invoice_url"] if data["object"]["hosted_invoice_url"] else None,
            #     },
            # )

        else:
            logger.warning(f"Unhandled event type: {event['type']}")

        return HttpResponse(status=200)
    

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
                    settings.OWNER_EMAIL,
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
    