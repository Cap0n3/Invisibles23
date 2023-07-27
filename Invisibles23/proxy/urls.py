from django.urls import path
from . import views

urlpatterns = [
    path("mailchimp/", views.MailchimpProxy.as_view(), name="mailchimp-proxy"),
    path("ausha/", views.AushaProxy.as_view(), name="ausha-proxy"),
    path("stripe/", views.StripeProxy.as_view(), name="stripe-proxy"),
    path("stripe-webhook/", views.StripeWebhook.as_view(), name="stripe-webhook"),
]
