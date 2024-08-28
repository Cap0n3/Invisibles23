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


    # @unittest.skip("Skip test_stripe_event_registration_webhook")
    @patch("proxy.views.stripe.Webhook.construct_event")
    @patch("proxy.views.stripe.Customer.modify", return_value=None)
    def test_stripe_membership_webhook(self, mock_stripe_customer_modify, mock_construct_event):
        """
        This test simulates a Stripe webhook event for a membership payment.
        It uses invoice.paid event to simulate a successful payment.
        """
        # Setup the mock to return a simulated Stripe event
        mock_event_data = {
            "id": "evt_1MqqbKLt4dXK03v5qaIbiNCC",
            "object": "event",
            "api_version": "2024-06-20",
            "created": 1680064028,
            "type": "invoice.paid",
            "data": {
                "object": {
                    "id": "in_1PqZkjBpqKPTmGHq9GboPpEb",
                    "object": "invoice",
                    "livemode": False,
                    "payment_intent": "pi_3PqZkjBpqKPTmGHq1IGc4TCP",
                    "status": "paid",
                    "account_country": "CH",
                    "account_name": "DEV Test",
                    "account_tax_ids": None,
                    "amount_due": 2500,
                    "amount_paid": 2500,
                    "amount_remaining": 0,
                    "amount_shipping": 0,
                    "application": None,
                    "application_fee_amount": None,
                    "attempt_count": 1,
                    "attempted": True,
                    "auto_advance": False,
                    "automatic_tax": {
                        "enabled": False,
                        "liability": None,
                        "status": None,
                    },
                    "automatically_finalizes_at": None,
                    "billing_reason": "subscription_create",
                    "charge": "ch_3PqZkjBpqKPTmGHq1oIzGdon",
                    "collection_method": "charge_automatically",
                    "created": 1724328273,
                    "currency": "chf",
                    "custom_fields": None,
                    "customer": "cus_Qhzk8mRaY916py",
                    "customer_address": {
                        "city": None,
                        "country": "CH",
                        "line1": None,
                        "line2": None,
                        "postal_code": None,
                        "state": None,
                    },
                    "customer_email": "afra.amaya@tutanota.com",
                    "customer_name": "Anita Cassiette",
                    "customer_phone": None,
                    "customer_shipping": None,
                    "customer_tax_exempt": "none",
                    "customer_tax_ids": [],
                    "default_payment_method": None,
                    "default_source": None,
                    "default_tax_rates": [],
                    "description": None,
                    "discount": None,
                    "discounts": [],
                    "due_date": None,
                    "effective_at": 1724328273,
                    "ending_balance": 0,
                    "footer": None,
                    "from_invoice": None,
                    "hosted_invoice_url": "https://invoice.stripe.com/i/acct_1OaKnuBpqKPTmGHq/test_YWNjdF8xT2FLbnVCcHFLUFRtR0hxLF9RaHprWGRENWhJNjFoRElrQkhFSjdlVFBCdVFOSWxFLDExNDg2OTA4MQ0200jK3MhQ8m?s=ap",
                    "invoice_pdf": "https://pay.stripe.com/invoice/acct_1OaKnuBpqKPTmGHq/test_YWNjdF8xT2FLbnVCcHFLUFRtR0hxLF9RaHprWGRENWhJNjFoRElrQkhFSjdlVFBCdVFOSWxFLDExNDg2OTA4MQ0200jK3MhQ8m/pdf?s=ap",
                    "issuer": {"type": "self"},
                    "last_finalization_error": None,
                    "latest_revision": None,
                    "lines": {
                        "object": "list",
                        "data": [
                            {
                                "id": "il_1PqZkjBpqKPTmGHqXaRTCH24",
                                "object": "line_item",
                                "amount": 2500,
                                "amount_excluding_tax": 2500,
                                "currency": "chf",
                                "description": "1 × Reduit (at CHF 25.00 / year)",
                                "discount_amounts": [],
                                "discountable": True,
                                "discounts": [],
                                "invoice": "in_1PqZkjBpqKPTmGHq9GboPpEb",
                                "livemode": False,
                                "metadata": {
                                    "address": "Chemin des Fauvettes 6",
                                    "birthday": "2024-08-21",
                                    "city": "Lancy",
                                    "customer_email": "afra.amaya@tutanota.com",
                                    "name": "Anita Cassiette",
                                    "phone": "076 543 22 11",
                                    "zip_code": "1212",
                                    "type": "membership",
                                },
                                "period": {"end": 1755864273, "start": 1724328273},
                                "plan": {
                                    "id": "price_1OaLHXBpqKPTmGHqDgKxIUWn",
                                    "object": "plan",
                                    "active": True,
                                    "aggregate_usage": None,
                                    "amount": 2500,
                                    "amount_decimal": "2500",
                                    "billing_scheme": "per_unit",
                                    "created": 1705683063,
                                    "currency": "chf",
                                    "interval": "year",
                                    "interval_count": 1,
                                    "livemode": False,
                                    "metadata": {},
                                    "meter": None,
                                    "nickname": None,
                                    "product": "prod_PP9ZbtTQVNPi4g",
                                    "tiers_mode": None,
                                    "transform_usage": None,
                                    "trial_period_days": None,
                                    "usage_type": "licensed",
                                },
                                "price": {
                                    "id": "price_1OaLHXBpqKPTmGHqDgKxIUWn",
                                    "object": "price",
                                    "active": True,
                                    "billing_scheme": "per_unit",
                                    "created": 1705683063,
                                    "currency": "chf",
                                    "custom_unit_amount": None,
                                    "livemode": False,
                                    "lookup_key": "reduced-yearly",
                                    "metadata": {},
                                    "nickname": None,
                                    "product": "prod_PP9ZbtTQVNPi4g",
                                    "recurring": {
                                        "aggregate_usage": None,
                                        "interval": "year",
                                        "interval_count": 1,
                                        "meter": None,
                                        "trial_period_days": None,
                                        "usage_type": "licensed",
                                    },
                                    "tax_behavior": "unspecified",
                                    "tiers_mode": None,
                                    "transform_quantity": None,
                                    "type": "recurring",
                                    "unit_amount": 2500,
                                    "unit_amount_decimal": "2500",
                                },
                                "proration": False,
                                "proration_details": {"credited_items": None},
                                "quantity": 1,
                                "subscription": "sub_1PqZkjBpqKPTmGHq9L9WTWI1",
                                "subscription_item": "si_QhzkGIKL0MWZ3u",
                                "tax_amounts": [],
                                "tax_rates": [],
                                "type": "subscription",
                                "unit_amount_excluding_tax": "2500",
                            }
                        ],
                        "has_more": False,
                        "total_count": 1,
                        "url": "/v1/invoices/in_1PqZkjBpqKPTmGHq9GboPpEb/lines",
                    },
                    "metadata": {},
                    "next_payment_attempt": None,
                    "number": "B3D0FDDC-0001",
                    "on_behalf_of": None,
                    "paid": True,
                    "paid_out_of_band": False,
                    "payment_settings": {
                        "default_mandate": None,
                        "payment_method_options": {
                            "acss_debit": None,
                            "bancontact": None,
                            "card": {"request_three_d_secure": "automatic"},
                            "customer_balance": None,
                            "konbini": None,
                            "sepa_debit": None,
                            "us_bank_account": None,
                        },
                        "payment_method_types": None,
                    },
                    "period_end": 1724328273,
                    "period_start": 1724328273,
                    "post_payment_credit_notes_amount": 0,
                    "pre_payment_credit_notes_amount": 0,
                    "quote": None,
                    "receipt_number": None,
                    "rendering": None,
                    "rendering_options": None,
                    "shipping_cost": None,
                    "shipping_details": None,
                    "starting_balance": 0,
                    "statement_descriptor": None,
                    "status_transitions": {
                        "finalized_at": 1724328273,
                        "marked_uncollectible_at": None,
                        "paid_at": 1724328280,
                        "voided_at": None,
                    },
                    "subscription": "sub_1PqZkjBpqKPTmGHq9L9WTWI1",
                    "subscription_details": {
                        "metadata": {
                            "address": "Chemin des Fauvettes 6",
                            "birthday": "2024-08-21",
                            "city": "Lancy",
                            "customer_email": "afra.amaya@tutanota.com",
                            "name": "Anita Cassiette",
                            "phone": "076 543 22 11",
                            "zip_code": "1212",
                        }
                    },
                    "subtotal": 2500,
                    "subtotal_excluding_tax": 2500,
                    "tax": None,
                    "test_clock": None,
                    "total": 2500,
                    "total_discount_amounts": [],
                    "total_excluding_tax": 2500,
                    "total_tax_amounts": [],
                    "transfer_data": None,
                    "webhooks_delivered_at": 1724328275,
                },
            },
        }

        mock_construct_event.return_value = mock_event_data
        #mock_stripe_customer_modify.return_value = None
        
        # Simulated payload
        payload = b'{\n  "id": "evt_3PqcGjBpqKPTmGHq28tgNN8c",\n  "object": "event",\n  "api_version": "2023-10-16",\n  "created": 1724337945,\n  "data": {\n    "object": {\n      "id": "pi_3PqcGjBpqKPTmGHq25tIse2a",\n      "object": "payment_intent",\n      "amount": 3000,\n      "currency": "usd",\n      "status": "requires_payment_method",\n      "shipping": {\n        "address": {\n          "city": "San Francisco",\n          "country": "US",\n          "line1": "510 Townsend St",\n          "postal_code": "94103",\n          "state": "CA"\n        },\n        "name": "Jenny Rosen"\n      }\n    }\n  },\n  "livemode": false,\n  "pending_webhooks": 2,\n  "request": {\n    "id": "req_88lDWA22gUCC9F",\n    "idempotency_key": "be9654eb-1ac6-4066-9632-06061b826f44"\n  },\n  "type": "invoice.paid"\n}'

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

    
    # @unittest.skip("Skip test_stripe_event_registration_webhook")
    @patch("proxy.views.stripe.Webhook.construct_event")
    def test_stripe_event_registration_webhook(self, mock_construct_event):
        """
        This test simulates a Stripe webhook event for an event registration payment.
        It uses the checkout.session.completed event to simulate a successful payment.
        """
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
                        "type": "talk-group",
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
        payload = b'{\n  "id": "evt_1Pqe58BpqKPTmGHqynffid90",\n  "object": "event",\n  "api_version": "2023-10-16",\n  "created": 1724344914,\n  "data": {\n    "object": {\n      "id": "in_1Pqe56BpqKPTmGHqp2kNJxXq",\n      "object": "invoice",\n      "account_country": "CH",\n      "account_name": "DEV Test",\n      "account_tax_ids": null,\n      "amount_due": 2000,\n      "amount_paid": 2000,\n      "amount_remaining": 0,\n      "amount_shipping": 0,\n      "application": null,\n      "application_fee_amount": null,\n      "attempt_count": 1,\n      "attempted": true,\n      "auto_advance": false,\n      "automatic_tax": {\n        "enabled": false,\n        "liability": null,\n        "status": null\n      },\n      "automatically_finalizes_at": null,\n      "billing_reason": "manual",\n      "charge": "ch_3Pqe57BpqKPTmGHq2v3e9CWG",\n      "collection_method": "charge_automatically",\n      "created": 1724344912,\n      "currency": "usd",\n      "custom_fields": null,\n      "customer": "cus_Qi4DTEv9x00sDf",\n      "customer_address": null,\n      "customer_email": null,\n      "customer_name": null,\n      "customer_phone": null,\n      "customer_shipping": null,\n      "customer_tax_exempt": "none",\n      "customer_tax_ids": [\n\n      ],\n      "default_payment_method": null,\n      "default_source": null,\n      "default_tax_rates": [\n\n      ],\n      "description": "(created by Stripe CLI)",\n      "discount": null,\n      "discounts": [\n\n      ],\n      "due_date": null,\n      "effective_at": 1724344912,\n      "ending_balance": 0,\n      "footer": null,\n      "from_invoice": null,\n      "hosted_invoice_url": "https://invoice.stripe.com/i/acct_1OaKnuBpqKPTmGHq/test_YWNjdF8xT2FLbnVCcHFLUFRtR0hxLF9RaTREd1FnWFFhQVJxMXVENkdoQzJISUt4Sk5ROVNZLDExNDg4NTcxNA0200lfW01cC4?s=ap",\n      "invoice_pdf": "https://pay.stripe.com/invoice/acct_1OaKnuBpqKPTmGHq/test_YWNjdF8xT2FLbnVCcHFLUFRtR0hxLF9RaTREd1FnWFFhQVJxMXVENkdoQzJISUt4Sk5ROVNZLDExNDg4NTcxNA0200lfW01cC4/pdf?s=ap",\n      "issuer": {\n        "type": "self"\n      },\n      "last_finalization_error": null,\n      "latest_revision": null,\n      "lines": {\n        "object": "list",\n        "data": [\n          {\n            "id": "il_1Pqe55BpqKPTmGHqS8KnkXnV",\n            "object": "line_item",\n            "amount": 2000,\n            "amount_excluding_tax": 2000,\n            "currency": "usd",\n            "description": "(created by Stripe CLI)",\n            "discount_amounts": [\n\n            ],\n            "discountable": true,\n            "discounts": [\n\n            ],\n            "invoice": "in_1Pqe56BpqKPTmGHqp2kNJxXq",\n            "invoice_item": "ii_1Pqe55BpqKPTmGHqIQ75qoAc",\n            "livemode": false,\n            "metadata": {\n            },\n            "period": {\n              "end": 1724344911,\n              "start": 1724344911\n            },\n            "plan": null,\n            "price": {\n              "id": "price_1Ox9snBpqKPTmGHqTPlpqFze",\n              "object": "price",\n              "active": false,\n              "billing_scheme": "per_unit",\n              "created": 1711120789,\n              "currency": "usd",\n              "custom_unit_amount": null,\n              "livemode": false,\n              "lookup_key": null,\n              "metadata": {\n              },\n              "nickname": null,\n              "product": "prod_PmjLdvl8ljFdzr",\n              "recurring": null,\n              "tax_behavior": "unspecified",\n              "tiers_mode": null,\n              "transform_quantity": null,\n              "type": "one_time",\n              "unit_amount": 2000,\n              "unit_amount_decimal": "2000"\n            },\n            "proration": false,\n            "proration_details": {\n              "credited_items": null\n            },\n            "quantity": 1,\n            "subscription": null,\n            "tax_amounts": [\n\n            ],\n            "tax_rates": [\n\n            ],\n            "type": "invoiceitem",\n            "unit_amount_excluding_tax": "2000"\n          }\n        ],\n        "has_more": false,\n        "total_count": 1,\n        "url": "/v1/invoices/in_1Pqe56BpqKPTmGHqp2kNJxXq/lines"\n      },\n      "livemode": false,\n      "metadata": {\n      },\n      "next_payment_attempt": null,\n      "number": "189A881C-0001",\n      "on_behalf_of": null,\n      "paid": true,\n      "paid_out_of_band": false,\n      "payment_intent": "pi_3Pqe57BpqKPTmGHq2AIB1eSd",\n      "payment_settings": {\n        "default_mandate": null,\n        "payment_method_options": null,\n        "payment_method_types": null\n      },\n      "period_end": 1724344912,\n      "period_start": 1724344912,\n      "post_payment_credit_notes_amount": 0,\n      "pre_payment_credit_notes_amount": 0,\n      "quote": null,\n      "receipt_number": null,\n      "rendering": {\n        "amount_tax_display": null,\n        "pdf": {\n          "page_size": "letter"\n        }\n      },\n      "rendering_options": null,\n      "shipping_cost": null,\n      "shipping_details": null,\n      "starting_balance": 0,\n      "statement_descriptor": null,\n      "status": "paid",\n      "status_transitions": {\n        "finalized_at": 1724344912,\n        "marked_uncollectible_at": null,\n        "paid_at": 1724344912,\n        "voided_at": null\n      },\n      "subscription": null,\n      "subscription_details": {\n        "metadata": null\n      },\n      "subtotal": 2000,\n      "subtotal_excluding_tax": 2000,\n      "tax": null,\n      "test_clock": null,\n      "total": 2000,\n      "total_discount_amounts": [\n\n      ],\n      "total_excluding_tax": 2000,\n      "total_tax_amounts": [\n\n      ],\n      "transfer_data": null,\n      "webhooks_delivered_at": null\n    }\n  },\n  "livemode": false,\n  "pending_webhooks": 2,\n  "request": {\n    "id": "req_5FkcGhYzIugBUt",\n    "idempotency_key": "5d0f73fb-1e37-4c17-9587-4ca3d6636ef1"\n  },\n  "type": "checkout.session.completed"\n}'

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
        
        # Check that the participant has been created
        participant = Participant.objects.get(email="afra.amaya@tutanota.com")
        self.assertEqual(participant.email, "afra.amaya@tutanota.com")
        self.assertEqual(participant.fname, "Marc")
        self.assertEqual(participant.lname, "Cash")
        
        # Check that the participant has been added to the event
        event_participant = EventParticipants.objects.get(event=self.event, participant=participant)
        self.assertEqual(event_participant.event, self.event)
        self.assertEqual(event_participant.participant, participant)
        