from django.test import TestCase, override_settings, Client
from website.models import Event
import unittest
from unittest.mock import patch, MagicMock
from django.urls import reverse
import stripe
import environ
from Invisibles23.logging_config import logger
import json
import time

env = environ.Env()
env.read_env("../.env")

# NOT WORKING, NEED TO FIX
"""
Here I'm having trouble to emulate the Stripe webhook event, I'm not sure how to do it. Go back to this when
I'll be a grown up dev ...
"""


@unittest.skip("Don't run the test, need to work on it")
class StipeEventRegistrationWebhookTests(TestCase):
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
        self.client = Client()
        self.url = reverse("stripe-event-webhook")
        self.payload = {
            "id": "evt_test",
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test",
                    "customer_details": {
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "country": "US",
                    },
                    "metadata": {
                        "event": "2024-07-15 - Test Event (1)",
                        "event_description": "A short description for testing",
                        "name": "John Doe",
                        "membership_status": "member",
                        "address": "123 Main St",
                        "zip_code": "12345",
                        "city": "Test City",
                        "customer_email": "john.doe@example.com",
                    },
                }
            },
        }
        self.sig_header = (
            "t=" + str(int(time.time())) + ",v1=fake_signature,v0=fake_signature"
        )

    @patch("stripe.Event.construct_from")
    def test_webhook_checkout_session_completed(self, mock_construct_from):
        mock_event = MagicMock()
        mock_event.type = "checkout.session.completed"
        mock_event.data.object = self.payload["data"]["object"]
        # MagicMock objects do not inherently support dictionary-style item access
        # so we need to define a side_effect to return the correct value
        mock_event.__getitem__.side_effect = lambda key: {
            "type": mock_event.type,
            "data": mock_event.data,
        }[key]
        mock_construct_from.return_value = mock_event

        response = self.client.post(
            self.url,
            data=json.dumps(self.payload),
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE=self.sig_header,
        )
        self.assertEqual(response.status_code, 200)


# HERE ARE SOME EXAMPLES OF PAYLOADS THAT CAN BE USED FOR TESTING

# data = [
#     "object": {
#         "amount": 1500,
#         "amount_captured": 1500,
#         "amount_refunded": 0,
#         "application": null,
#         "application_fee": null,
#         "application_fee_amount": null,
#         "balance_transaction": "txn_3Pc5u6BpqKPTmGHq2Deem5xc",
#         "billing_details": {
#         "address": {
#             "city": null,
#             "country": "CH",
#             "line1": null,
#             "line2": null,
#             "postal_code": null,
#             "state": null
#         },
#         "email": "herov@mailinator.com",
#         "name": "Peter Mealy",
#         "phone": null
#         },
#         "calculated_statement_descriptor": "Stripe",
#         "captured": true,
#         "created": 1720876948,
#         "currency": "chf",
#         "customer": null,
#         "description": null,
#         "destination": null,
#         "dispute": null,
#         "disputed": false,
#         "failure_balance_transaction": null,
#         "failure_code": null,
#         "failure_message": null,
#         "fraud_details": {},
#         "id": "ch_3Pc5u6BpqKPTmGHq2Db8tVRd",
#         "invoice": null,
#         "livemode": false,
#         "metadata": {},
#         "object": "charge",
#         "on_behalf_of": null,
#         "order": null,
#         "outcome": {
#         "network_status": "approved_by_network",
#         "reason": null,
#         "risk_level": "normal",
#         "risk_score": 30,
#         "seller_message": "Payment complete.",
#         "type": "authorized"
#         },
#         "paid": true,
#         "payment_intent": "pi_3Pc5u6BpqKPTmGHq2Gxos0rf",
#         "payment_method": "pm_1Pc5u6BpqKPTmGHq7BeceP9i",
#         "payment_method_details": {
#         "card": {
#             "amount_authorized": 1500,
#             "brand": "visa",
#             "checks": {
#             "address_line1_check": null,
#             "address_postal_code_check": null,
#             "cvc_check": "pass"
#             },
#             "country": "IE",
#             "exp_month": 7,
#             "exp_year": 2037,
#             "extended_authorization": {
#             "status": "disabled"
#             },
#             "fingerprint": "LznUU1TLAZHaDDRt",
#             "funding": "credit",
#             "incremental_authorization": {
#             "status": "unavailable"
#             },
#             "installments": null,
#             "last4": "3220",
#             "mandate": null,
#             "multicapture": {
#             "status": "unavailable"
#             },
#             "network": "visa",
#             "network_token": {
#             "used": false
#             },
#             "overcapture": {
#             "maximum_amount_capturable": 1500,
#             "status": "unavailable"
#             },
#             "three_d_secure": {
#             "authentication_flow": "challenge",
#             "electronic_commerce_indicator": "05",
#             "exemption_indicator": null,
#             "result": "authenticated",
#             "result_reason": null,
#             "transaction_id": "210ea360-e578-4245-a8c2-de44ca27fbca",
#             "version": "2.1.0"
#             },
#             "wallet": null
#         },
#         "type": "card"
#         },
#         "radar_options": {},
#         "receipt_email": null,
#         "receipt_number": null,
#         "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xT2FLbnVCcHFLUFRtR0hxKJX_ybQGMgby5ozrfkM6LBYisKPXNEIByH2ipgxeKqfQQL3yeMTOeIjTTZG5aOLFW5B2nOYZyh4AxQ6_",
#         "refunded": false,
#         "review": null,
#         "shipping": null,
#         "source": null,
#         "source_transfer": null,
#         "statement_descriptor": null,
#         "statement_descriptor_suffix": null,
#         "status": "succeeded",
#         "transfer_data": null,
#         "transfer_group": null
#     }
# ]

# payload = {
#     "id": "evt_3Pc5u6BpqKPTmGHq2tq5M6qU",
#     "object": "event",
#     "api_version": "2023-10-16",
#     "created": 1720876948,
#     "data": {
#         "object": {
#             "id": "ch_3Pc5u6BpqKPTmGHq2Db8tVRd",
#             "object": "charge",
#             "amount": 1500,
#             "amount_captured": 1500,
#             "amount_refunded": 0,
#             "application": None,
#             "application_fee": None,
#             "application_fee_amount": None,
#             "balance_transaction": "txn_3Pc5u6BpqKPTmGHq2Deem5xc",
#             "billing_details": {
#                 "address": {
#                     "city": None,
#                     "country": "CH",
#                     "line1": None,
#                     "line2": None,
#                     "postal_code": None,
#                     "state": None
#                 },
#                 "email": "herov@mailinator.com",
#                 "name": "Peter Mealy",
#                 "phone": None
#             },
#             "calculated_statement_descriptor": "Stripe",
#             "captured": True,
#             "created": 1720876948,
#             "currency": "chf",
#             "customer": None,
#             "description": None,
#             "destination": None,
#             "dispute": None,
#             "disputed": False,
#             "failure_balance_transaction": None,
#             "failure_code": None,
#             "failure_message": None,
#             "fraud_details": {},
#             "invoice": None,
#             "livemode": False,
#             "metadata": {},
#             "on_behalf_of": None,
#             "order": None,
#             "outcome": {
#                 "network_status": "approved_by_network",
#                 "reason": None,
#                 "risk_level": "normal",
#                 "risk_score": 30,
#                 "seller_message": "Payment complete.",
#                 "type": "authorized"
#             },
#             "paid": True,
#             "payment_intent": "pi_3Pc5u6BpqKPTmGHq2Gxos0rf",
#             "payment_method": "pm_1Pc5u6BpqKPTmGHq7BeceP9i",
#             "payment_method_details": {
#                 "card": {
#                     "amount_authorized": 1500,
#                     "brand": "visa",
#                     "checks": {
#                         "address_line1_check": None,
#                         "address_postal_code_check": None,
#                         "cvc_check": "pass"
#                     },
#                     "country": "IE",
#                     "exp_month": 7,
#                     "exp_year": 2037,
#                     "extended_authorization": {
#                         "status": "disabled"
#                     },
#                     "fingerprint": "LznUU1TLAZHaDDRt",
#                     "funding": "credit",
#                     "incremental_authorization": {
#                         "status": "unavailable"
#                     },
#                     "installments": None,
#                     "last4": "3220",
#                     "mandate": None,
#                     "multicapture": {
#                         "status": "unavailable"
#                     },
#                     "network": "visa",
#                     "network_token": {
#                         "used": False
#                     },
#                     "overcapture": {
#                         "maximum_amount_capturable": 1500,
#                         "status": "unavailable"
#                     },
#                     "three_d_secure": {
#                         "authentication_flow": "challenge",
#                         "electronic_commerce_indicator": "05",
#                         "exemption_indicator": None,
#                         "result": "authenticated",
#                         "result_reason": None,
#                         "transaction_id": "210ea360-e578-4245-a8c2-de44ca27fbca",
#                         "version": "2.1.0"
#                     },
#                     "wallet": None
#                 },
#                 "type": "card"
#             },
#             "radar_options": {},
#             "receipt_email": None,
#             "receipt_number": None,
#             "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xT2FLbnVCcHFLUFRtR0hxKJX_ybQGMgby5ozrfkM6LBYisKPXNEIByH2ipgxeKqfQQL3yeMTOeIjTTZG5aOLFW5B2nOYZyh4AxQ6_",
#             "refunded": False,
#             "review": None,
#             "shipping": None,
#             "source": None,
#             "source_transfer": None,
#             "statement_descriptor": None,
#             "statement_descriptor_suffix": None,
#             "status": "succeeded",
#             "transfer_data": None,
#             "transfer_group": None
#         }
#     },
#     "livemode": False,
#     "pending_webhooks": 2,
#     "request": {
#         "id": None,
#         "idempotency_key": "pi_3Pc5u6BpqKPTmGHq2Gxos0rf-payatt_3Pc5u6BpqKPTmGHq2QwUNWtz"
#     },
#     "type": "charge.succeeded"
# }
