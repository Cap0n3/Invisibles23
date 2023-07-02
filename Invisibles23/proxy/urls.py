from django.urls import path
from . import views

urlpatterns = [
    path('mailchimp/', views.MailchimpProxy.as_view(), name='mailchimp-proxy'),
]