from django.urls import path
from . import views

urlpatterns = [
    path("mailchimp/", views.MailchimpProxy.as_view(), name="mailchimp-proxy"),
    path("ausha/", views.AushaProxy.as_view(), name="ausha-proxy"),
    path("stripe-webhook/", views.StripeWebhook.as_view(), name="stripe-webhook"), # For membership payments
    path("stripe-event-webhook/", views.StipeEventRegistrationWebhook.as_view(), name="stripe-event-webhook"),
    path("get_api_secrets/", views.GetAPISecrets.as_view(), name="get-api-secrets"),
    path("email_server/", views.EmailSender.as_view(), name="email-server"),
]
