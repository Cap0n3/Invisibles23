from django.shortcuts import render
from django.views import View
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
import environ
import requests
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Read the .env file
env = environ.Env()
env.read_env('../.env')

class AushaProxy(View):
    http_method_names = ['post'] # Only POST requests are allowed
    ausha_api_key = env('AUSHA_API_TOKEN')

    def post(self, request):
        show_id = request.POST.get('show_id')
        
        if not show_id:
            return HttpResponseBadRequest('Show ID is required')
        
        url = f"https://developers.ausha.co/v1/shows/{show_id}/podcasts"

        # Send a request to Ausha API
        try:
            response = requests.get(url, headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.ausha_api_key}'
            })
            return JsonResponse(response.json(), safe=False)
        except Exception as error:
            print(f"An exception occurred: {error}")
            return JsonResponse({
                'message': f"An error occurred: {error}",
            }, status=500)

class MailchimpProxy(View):
    http_method_names = ['post'] # Only POST requests are allowed
    server_prefix = "us21"
    mailchimp_api_key = env('MAILCHIMP_API_KEY')
    list_id = env('MAILCHIMP_LIST_ID')
    
    def post(self, request):        
        email = request.POST.get('email')
        test_status = request.POST.get('test_status')
        test_status = int(test_status) if test_status != "null" else None

        if not email:
            return HttpResponseBadRequest('Email is required')

        member_info = {
            'email_address': email,
            'status': 'subscribed'
        }

        # Mailchimp API endpoint
        try:
            if test_status and isinstance(test_status, int):
                # Simulating a test error with custom status code and error message
                raise ApiClientError("An error occurred", status_code=test_status)
            
            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": self.mailchimp_api_key,
                "server": self.server_prefix
            })
            response = client.lists.add_list_member(self.list_id, member_info)
            print("response: {}".format(response))
            
            return JsonResponse({
                'message': 'You have successfully subscribed to our mailing list.',
            },  status=200)
        except ApiClientError as error:
            # Same with f string
            print(f"An exception occurred: {error.text}")

            return JsonResponse({
                'message': f"An error occurred: {error.text}",
            }, status=error.status_code)

class StripeProxy(View):
    http_method_names = ['post'] # Only POST requests are allowed 
    stripe.api_key = env('STRIPE_API_TOKEN')
    
    def post(self, request):
        # Get the form data
        lookup_key = request.POST.get('lookup_key')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')

        try:
            domain = "http://127.0.0.1:8000" if settings.DEBUG else settings.DOMAIN

            # Check if customer already exists
            customer_search = stripe.Customer.search(
                query=f"name:'{fname} {lname}' AND email:'{email}'",
            )

            if customer_search.data:
                print("Customer found")
                return JsonResponse({
                    'error': 'Customer already exists in database.',
                    'error-message': "Vous êtes déjà membre de notre association ! Si vous souhaitez modifier votre abonnement, veuillez nous contacter à l'adresse suivante : ",
                },  status=409)
            
            # Get prices from Stripe
            prices = stripe.Price.list(
                lookup_keys=[lookup_key],
                expand=['data.product']
            )

            # Create payment intent (necessary ?)
            # payment_intent = stripe.PaymentIntent.create(
            #     amount=prices.data[0].unit_amount,
            #     currency=prices.data[0].currency,
            #     payment_method_types=['card'],
            #     customer=customer_search.data[0].id,
            #     setup_future_usage='off_session',
            #     metadata={
            #         'fname': fname,
            #         'lname': lname,
            #     }
            # )

            # Create checkout session to redirect to Stripe
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': prices.data[0].id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url = domain + '/success.html?session_id={CHECKOUT_SESSION_ID}',
                cancel_url = domain + '/cancel.html',
            )
            
            return JsonResponse({
                'sessionId': checkout_session['id'],
                'sessionUrl': checkout_session['url'],
            }, status=200)

        except Exception as error:
            print(f"An exception occurred: {error}")
            return JsonResponse({
                'message': f"An error occurred: {error}",
            }, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhook(View):
    http_method_names = ['post'] # Only POST requests are allowed
    
    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        stripe_secret = env('STRIPE_WEBHOOK_SECRET')
        event = None
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, stripe_secret
            )
            data = event['data']
            return HttpResponse(status=200)
        except ValueError as e:
            # Invalid payload
            print("Invalid payload")
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print("Invalid signature")
            return HttpResponse(status=403)