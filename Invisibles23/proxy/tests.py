# ================================ #
# ====== WEBHOOK VIEW TESTS ====== #
# ================================ #

from django.test import TestCase, override_settings
from django.urls import reverse
import unittest
from proxy.views import StripeWebhook
from website.models import Event, Participant, EventParticipants
from Invisibles23.logging_config import logger
from django.test import TestCase, RequestFactory
from unittest.mock import patch, Mock


class StripeWebhookTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Necessary to override the DEBUG setting to True, otherwise DEBUG mode is set to OFF.
        I don't know why it is necessary to do this, environs seems to not load the .env file correctly
        during testing (therefore setting DEBUG to false, see settings.py).
        """
        super().setUpClass()
        cls.override = override_settings(DEBUG=True)
        cls.override.enable()
    
    
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.override.disable()
        
        
    def setUp(self):
        self.factory = RequestFactory()
        # Create test event
        self.event = Event.objects.create(
            is_talk_event=True,
            title="Test Event",
            short_description="This is a test event",
            full_description="This is a test event, please ignore it.",
            date="2022-12-12",
            start_time="12:00",
            end_time="14:00",
        )


    @patch("proxy.views.stripe.Webhook.construct_event")
    def test_stripe_event_registration_webhook(self, mock_construct_event):
        # Setup the mock to return a simulated Stripe event
        mock_event_data = {
            "id": "evt_1MqqbKLt4dXK03v5qaIbiNCC",
            "object": "event",
            "api_version": "2024-06-20",
            "created": 1680064028,
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test_b1IzczycFQsKHH6LkN1RLhkz2XNmDG8walMTeUZrZQqTzQO7hdgrokVuuw",
                    "object": "checkout.session",
                    "after_expiration": None,
                    "allow_promotion_codes": True,
                    "amount_subtotal": 2500,
                    "amount_total": 2500,
                    "automatic_tax": {
                        "enabled": False,
                        "liability": None,
                        "status": None,
                    },
                    "billing_address_collection": None,
                    "cancel_url": "http://127.0.0.1:8000/rendez-vous/",
                    "client_reference_id": None,
                    "client_secret": None,
                    "consent": None,
                    "consent_collection": None,
                    "created": 1724319331,
                    "currency": "chf",
                    "currency_conversion": None,
                    "custom_fields": [],
                    "custom_text": {
                        "after_submit": None,
                        "shipping_address": None,
                        "submit": None,
                        "terms_of_service_acceptance": None,
                    },
                    "customer": None,
                    "customer_creation": "if_required",
                    "customer_details": {
                        "address": {
                            "city": None,
                            "country": "CH",
                            "line1": None,
                            "line2": None,
                            "postal_code": None,
                            "state": None,
                        },
                        "email": "afra.amaya@tutanota.com",
                        "name": "Marc Cash",
                        "phone": None,
                        "tax_exempt": "none",
                        "tax_ids": [],
                    },
                    "customer_email": "afra.amaya@tutanota.com",
                    "expires_at": 1724405731,
                    "invoice": None,
                    "invoice_creation": {
                        "enabled": False,
                        "invoice_data": {
                            "account_tax_ids": None,
                            "custom_fields": None,
                            "description": None,
                            "footer": None,
                            "issuer": None,
                            "metadata": {},
                            "rendering_options": None,
                        },
                    },
                    "livemode": False,
                    "locale": None,
                    "metadata": {
                        "address": "Chemin des Fauvettes 6",
                        "city": "Lancy",
                        "customer_email": "afra.amaya@tutanota.com",
                        "event_description": "Maecenas gravida felis turpis, vitae imperdiet ante consequat sit amet. Morbi et nisi nec felis suscipit ultricies. Vivamus interdum sodales nunc, ac lobortis massa dictum bibendum.",
                        "event_id": self.event.id,
                        "event_infos": f"{self.event.title} - {self.event.date} - {self.event.start_time}",
                        "fname": "Marc",
                        "lname": "Cash",
                        "membership_status": "isNotMember",
                        "phone": "+41 75 701 58 68",
                        "zip_code": "1212",
                    },
                    "mode": "payment",
                    "payment_intent": "pi_3PqXQhBpqKPTmGHq2XCmwoxH",
                    "payment_link": None,
                    "payment_method_collection": "if_required",
                    "payment_method_configuration_details": {
                        "id": "pmc_1One75BpqKPTmGHq1mDAP5CU",
                        "parent": None,
                    },
                    "payment_method_options": {
                        "card": {"request_three_d_secure": "automatic"}
                    },
                    "payment_method_types": ["card", "link"],
                    "payment_status": "paid",
                    "phone_number_collection": {"enabled": False},
                    "recovered_from": None,
                    "saved_payment_method_options": None,
                    "setup_intent": None,
                    "shipping_address_collection": None,
                    "shipping_cost": None,
                    "shipping_details": None,
                    "shipping_options": [],
                    "status": "complete",
                    "submit_type": None,
                    "subscription": None,
                    "success_url": "http://127.0.0.1:8000/success/",
                    "total_details": {
                        "amount_discount": 0,
                        "amount_shipping": 0,
                        "amount_tax": 0,
                    },
                    "ui_mode": "hosted",
                    "url": None,
                }
            },
        }

        mock_construct_event.return_value = mock_event_data

        # Simulated payload
        payload = b'{\n  "id": "evt_3PqcGjBpqKPTmGHq28tgNN8c",\n  "object": "event",\n  "api_version": "2023-10-16",\n  "created": 1724337945,\n  "data": {\n    "object": {\n      "id": "pi_3PqcGjBpqKPTmGHq25tIse2a",\n      "object": "payment_intent",\n      "amount": 3000,\n      "currency": "usd",\n      "status": "requires_payment_method",\n      "shipping": {\n        "address": {\n          "city": "San Francisco",\n          "country": "US",\n          "line1": "510 Townsend St",\n          "postal_code": "94103",\n          "state": "CA"\n        },\n        "name": "Jenny Rosen"\n      }\n    }\n  },\n  "livemode": false,\n  "pending_webhooks": 2,\n  "request": {\n    "id": "req_88lDWA22gUCC9F",\n    "idempotency_key": "be9654eb-1ac6-4066-9632-06061b826f44"\n  },\n  "type": "checkout.session.completed"\n}'

        # Create a simulated POST request with a payload and a signature header
        request = self.factory.post(
            "/stripe-webhook/",
            data=payload,
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="t=1724337946,v1=2eea770c22f79220ed33a8f248be4ce0ea7ef19811abe00a68edc529f59f308b,v0=1d5f50957c23bad9050e7ebe05ff20c494701385c9941d518b66733b84f17724",
        )

        # Instantiate the view and call the post method
        response = StripeWebhook.as_view()(request)

        # Assert that the response status is 200 OK
        self.assertEqual(response.status_code, 200)
