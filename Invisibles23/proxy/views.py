from django.shortcuts import render
from django.views import View
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
        print("Getting API secrets...")

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


class StripeProxy(View):
    http_method_names = ["post"]  # Only POST requests are allowed
    stripe.api_key = env("STRIPE_API_TOKEN")
    print("Stripe proxy is ready ...")

    @staticmethod
    def choosePricing(subscription, frequency):
        """
        Choose the pricing based on the subscription and frequency.

        It will return following values:
        - support-monthly
        - support-yearly
        - normal-monthly
        - normal-yearly
        - reduced-monthly
        - reduced-yearly
        """
        _lookup_key = ""
        if subscription == "support":
            _lookup_key = (
                "support-monthly" if frequency == "monthly" else "support-yearly"
            )
        elif subscription == "normal":
            _lookup_key = (
                "normal-monthly" if frequency == "monthly" else "normal-yearly"
            )
        elif subscription == "reduced":
            _lookup_key = (
                "reduced-monthly" if frequency == "monthly" else "reduced-yearly"
            )

        return _lookup_key

    def post(self, request):
        print("Stripe proxy is handling form submission ...")
        # Get the form data
        lookup_key = request.POST.get("lookup_key")
        subscription = request.POST.get("subscription")
        frequency = request.POST.get("frequency")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        birthday = request.POST.get("birthday")
        address = request.POST.get("address")
        zip_code = request.POST.get("zip_code")
        city = request.POST.get("city")
        email = request.POST.get("email")

        try:
            domain = "http://127.0.0.1:8000" if settings.DEBUG else f"https://{settings.DOMAIN}"

            # Check if customer already exists
            customer_search = stripe.Customer.search(
                query=f"name:'{fname} {lname}' AND email:'{email}'",
            )

            # If customer exists, check if they have an active subscription
            if customer_search.data:
                existing_customer_id = customer_search.data[0].id
                # Search for active subscription
                subscription_search = stripe.Subscription.search(
                    query=f"status:'active'",
                )
                # Loop through subscriptions and find the one with the customer ID
                for subscription in subscription_search.data:
                    if subscription.customer == existing_customer_id:
                        print(
                            f"Customer already has an active subscription: {subscription}"
                        )
                        return JsonResponse(
                            {
                                "error": "Customer already exists in database.",
                                "error-message": "Vous êtes déjà membre de notre association ! Si vous souhaitez modifier votre abonnement, veuillez nous contacter à l'adresse suivante : ",
                            },
                            status=409,
                        )

            # Get the lookup key according to the subscription and frequency
            lookup_key = self.choosePricing(subscription, frequency)

            # Get prices from Stripe
            prices = stripe.Price.list(
                lookup_keys=[lookup_key], expand=["data.product"]
            )

            # Create checkout session to redirect to Stripe
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": prices.data[0].id,
                        "quantity": 1,
                    },
                ],
                currency="chf",
                customer_email=email,
                subscription_data={
                    "metadata": {
                        "Nom": f"{fname} {lname}",
                        "Anniversaire": birthday,
                        "adresse": address,
                        "CP": zip_code,
                        "Ville": city,
                        "Email": email,
                    },
                },
                mode="subscription",
                success_url=domain + "/success/",
                cancel_url=domain + "/cancel/",
            )

            return JsonResponse(
                {
                    "sessionId": checkout_session["id"],
                    "sessionUrl": checkout_session["url"],
                },
                status=200,
            )

        except Exception as error:
            print(f"An exception occurred: {error}")
            return JsonResponse(
                {
                    "message": f"An error occurred: {error}",
                },
                status=500,
            )


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhook(View):
    http_method_names = ["post"]  # Only POST requests are allowed

    def post(self, request):
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        stripe_secret = env("STRIPE_WEBHOOK_SECRET")
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, stripe_secret)
            data = event["data"]
        except ValueError as e:
            # Invalid payload
            print("Invalid payload")
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print("Invalid signature")
            return HttpResponse(status=403)

        # Handle the event
        if event["type"] == "checkout.session.completed":
            # Maybe log the event (to do later)
            print("Checkout session completed")     

        elif event["type"] == "invoice.finalized":
            print("Invoice finalized")
    
            # Get data from event
            member_name = data["object"]["customer_name"]
            member_email = data["object"]["customer_email"]
            invoice_url = data["object"]["hosted_invoice_url"]
            member_birthday = data["object"]["subscription_details"]["metadata"]["Anniversaire"]
            member_address = data["object"]["subscription_details"]["metadata"]["adresse"]
            member_postal_code = data["object"]["subscription_details"]["metadata"]["CP"]
            member_city = data["object"]["subscription_details"]["metadata"]["Ville"]
            membership_description = data["object"]["lines"]["data"][0]["description"]

            # FOR TESTING
            member_email = "afra.amaya@tutanota.com"

            # Send email to owner
            sendEmail(
                member_email,
                "Un nouveau membre a rejoint l'association Les Invisibles",
                "adhesion_notification.html",
                {
                    "name": member_name,
                    "email": member_email,
                    "birthday": member_birthday,
                    "address": member_address,
                    "postal_code": member_postal_code,
                    "city": member_city,
                    "description": membership_description,
                },
            )            
            
            # Send email to member
            sendEmail(
                member_email, 
                "Adhésion à l'association Les Invisibles", 
                "adhesion_email.html", 
                {
                    "name": member_name,
                    "invoice_url": invoice_url,
                }
            )

        return HttpResponse(status=200)

class EmailSender(View):
    http_method_names = ["post"]  # Only POST requests are allowed
    print("EmailSender initialized ...")

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
                print("Recaptcha verified. Sending email...")
                sendEmail(
                    email,
                    "Merci pour votre message",
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
                print(f"An exception occurred: {error}")
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
    