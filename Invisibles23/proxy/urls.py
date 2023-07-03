from django.urls import path
from . import views

urlpatterns = [
    path('mailchimp/', views.MailchimpProxy.as_view(), name='mailchimp-proxy'),
    path('ausha/', views.AushaProxy.as_view(), name='ausha-proxy'),
]