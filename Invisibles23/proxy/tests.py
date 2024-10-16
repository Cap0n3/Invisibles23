# ================================ #
# ====== WEBHOOK VIEW TESTS ====== #
# ================================ #

from django.test import TestCase, override_settings
from django.urls import reverse
import unittest
import requests
from proxy.views import StripeWebhook, MailchimpProxy
from website.models import Members, MembershipPlans, Event, Participant, EventParticipants
from proxy.test_data.test_objects import MOCK_MEMBERSHIP_EVENT, MOCK_TALK_EVENT
from Invisibles23.logging_config import logger
from django.test import TestCase, RequestFactory, Client
from unittest.mock import patch, Mock
from Invisibles23.logging_utils import log_debug_info
import random
import string


class StripeWebhookTest(TestCase):
    """
    Test case for the Stripe webhook view (member registration and event registration).
    Note: This test is a simulation of a Stripe webhook event, it does not actually send a request to Stripe.
    """

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
            talk_event_link="https://iamazoomlink.com",
        )
        
        # Create a test membership plan
        self.membership_plan = MembershipPlans.objects.create(
            name="Test Membership Plan",
            description="This is a test membership plan",
            price=25.00,
            frequency="yearly",
            lookup_key="reduced-yearly",
        )
    
    @patch("proxy.views.stripe.Webhook.construct_event")
    @patch("proxy.views.stripe.Customer.modify", return_value=None)
    def test_stripe_membership_webhook(
        self, mock_stripe_customer_modify, mock_construct_event
    ):
        """
        This test simulates a Stripe webhook event for a membership payment.
        It uses invoice.paid event to simulate a successful payment. It should
        trigger notification emails to the user and the admin.
        """
        mock_construct_event.return_value = MOCK_MEMBERSHIP_EVENT

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

        self.assertEqual(response.status_code, 200)
        
        # Check if member was added to the database
        member = Members.objects.get(email="afra.amaya@tutanota.com")
        self.assertEqual(member.fname, "Anita")
        self.assertEqual(member.lname, "Cassiette")
        self.assertEqual(member.phone, "076 543 22 11")
        self.assertEqual(member.address, "Chemin des Fauvettes 6")
        self.assertEqual(member.zip_code, "1212")
        self.assertEqual(member.city, "Lancy")
        self.assertEqual(member.country, "Suisse")
        self.assertEqual(member.stripe_customer_id, "cus_Qhzk8mRaY916py")
        self.assertEqual(member.payment_info_name, "Anita Cassiette")
        self.assertEqual(member.payment_info_country, "CH")
        self.assertEqual(member.membership_plan.lookup_key, "reduced-yearly")

    @patch("proxy.views.stripe.Webhook.construct_event")
    @patch("proxy.views.stripe.Customer.modify", return_value=None)
    def test_stripe_existing_member_webhook(self, mock_stripe_customer_modify, mock_construct_event):
        """
        This test simulates a Stripe webhook event for a membership payment
        if the member already exists in the database (edge case). It should 
        simply update the member information.
        
        Note: this could happen if a member stops their subscription and then
        starts it again. An existing active member will be filtered out at the 
        subscription creation level by the frontend.
        """
        # Create a test member (with a different address than in the payload)
        member = Members.objects.create(
            fname="Anita",
            lname="Cassiette",
            email="afra.amaya@tutanota.com",
            phone="076 543 22 11",
            birthdate="2024-08-21",
            address="Chemin de la Source 12", # Addrees is different
            zip_code="1233",
            city="Genève",
            country="Suisse",
            membership_plan=self.membership_plan
        )
        
        # The already existing member will pay for a membership plan
        mock_construct_event.return_value = MOCK_MEMBERSHIP_EVENT

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
        
        self.assertEqual(response.status_code, 200)
        
        # Get member
        member = Members.objects.get(email="afra.amaya@tutanota.com")
        self.assertEqual(member.fname, "Anita")
        self.assertEqual(member.lname, "Cassiette")
        self.assertEqual(member.membership_plan.lookup_key, "reduced-yearly")
        
        # Check if member infos were updated in the database
        self.assertEqual(member.address, "Chemin des Fauvettes 6")
        self.assertEqual(member.zip_code, "1212")
        self.assertEqual(member.city, "Lancy")
        self.assertEqual(member.country, "Suisse")
        
    @patch("proxy.views.stripe.Webhook.construct_event")
    def test_stripe_event_registration_webhook(self, mock_construct_event):
        """
        This test simulates a Stripe webhook event for an event registration payment.
        It uses the checkout.session.completed event to simulate a successful payment.
        """
        mock_construct_event.return_value = MOCK_TALK_EVENT

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
        
        logger.info(f"EVENT ID: {self.event.id}")

        # Assert that the response status is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the participant has been created
        participant = Participant.objects.get(email="afra.amaya@tutanota.com")
        logger.info(f"PARTICIPANT EMAIL: {participant.email}")
        self.assertEqual(participant.email, "afra.amaya@tutanota.com")
        self.assertEqual(participant.fname, "Marc")
        self.assertEqual(participant.lname, "Cash")

        # Check that the participant has been added to the event
        event_participant = EventParticipants.objects.get(
            event=self.event, participant=participant
        )
        self.assertEqual(event_participant.event, self.event)
        self.assertEqual(event_participant.participant, participant)


class MailchimpProxyTest(TestCase):
    """
    Important: This test case requires a Mailchimp account and a list to be created.
    Don't forget that many of the tests will add a fake contact to the list, so you may need to remove them manually.
    """

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
        # Create a random email address
        self.random_email = MailchimpProxyTest._generate_random_email()
        (
            self.random_fname,
            self.random_lname,
        ) = MailchimpProxyTest._generate_fake_name()

        self.mailchimp_proxy = MailchimpProxy()

    @unittest.skip("Skip test_mailchimp_add_full_contact")
    def test_mailchimp_add_contact(self):
        """
        This test simulate the addition of a full contact to the Mailchimp list (like it was done through the website newsletter form).
        IMPORTANT: This test will fail if the contact already exists in the list, you MUST manually remove contact from the list.
        """
        client = Client()
        response = client.post(
            reverse("mailchimp-proxy"),
            data={
                "email": self.random_email,
                "test_status": "null",
            },
        )
        self.assertEqual(response.status_code, 200)

    @staticmethod
    def _generate_random_email():
        """
        Generate a realistic but random email address with a fake username and domain.
        """
        # Generate a random username (mix of letters)
        username_length = random.randint(5, 10)
        random_username = "".join(
            random.choices(string.ascii_lowercase, k=username_length)
        )

        # Generate random numbers
        random_numbers = "".join(random.choices(string.digits, k=random.randint(1, 5)))

        # List of possible domains
        domains = ["com", "ch", "fr"]

        # Randomly select a domain
        domain = random.choice(domains)

        # Construct and return the email address
        return f"{random_username}_{random_numbers}@fallen.{domain}"

    @staticmethod
    def _generate_fake_name():
        """
        Generate a fake first name and last name for testing purposes.

        Returns
        -------
        tuple
            A tuple containing the fake first name and last name.
        """
        # Lists of sample first names and last names
        first_names = [
            "John",
            "Jane",
            "Alex",
            "Emily",
            "Chris",
            "Katie",
            "Michael",
            "Sarah",
            "David",
            "Laura",
            "Kevin",
            "Rachel",
            "Mark",
            "Julie",
        ]
        last_names = [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Miller",
            "Davis",
            "Garcia",
            "Martinez",
            "Taylor",
            "Clark",
            "Lewis",
            "Lee",
            "Walker",
        ]

        # Randomly select a first name and last name
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)

        return first_name, last_name
