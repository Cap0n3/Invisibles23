from django.urls import path
from . import views

urlpatterns = [
    path("mailchimp/", views.MailchimpProxy.as_view(), name="mailchimp-proxy"),
    path("ausha/", views.AushaProxy.as_view(), name="ausha-proxy"),
    path("stripe/", views.StripeProxy.as_view(), name="stripe-proxy"),
    path("stripe-webhook/", views.StripeWebhook.as_view(), name="stripe-webhook"),
    path("get_api_secrets/", views.GetAPISecrets.as_view(), name="get-api-secrets"),
    path("email_server/", views.EmailServer.as_view(), name="email-server"),
]
