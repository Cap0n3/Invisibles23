from django.shortcuts import render
from django.views import View
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from django.http import JsonResponse, HttpResponseBadRequest
import environ

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Read the .env file
env = environ.Env()
env.read_env('../.env')

@method_decorator(csrf_exempt, name='dispatch')
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

        
        
        