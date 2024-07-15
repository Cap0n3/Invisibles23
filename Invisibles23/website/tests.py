from django.test import TestCase, override_settings
import unittest
from .views import EventRegistrationView
from .models import Event
from Invisibles23.logging_config import logger


class EventRegistrationViewTest(TestCase):
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
        # Create a test event
        Event.objects.create(
            title="Test Event",
            short_description="This is a test event",
            full_description="This is a test event, please ignore it.",
            date="2022-12-12",
            start_time="12:00",
            end_time="14:00",
            address="Chemin de la Mairie 1",
            link="https://www.myevent.com",
        )
        self.event = Event.objects.get(title="Test Event")

    # @unittest.skip("Skip for now")
    def test_post(self):
        """
        Check if the user is redirected to a stripe checkout page
        """
        plans = ["support", "normal", "reduced"]
        form_data = {
            "fname": "John",
            "lname": "Doe",
            "email": "test@gmail.com",
            "address": "Chemin du Pré-Fleuri 3",
            "zip_code": "1228",
            "city": "Plan-les-Ouates",
            "membership_status": "isMember",
        }
        for plan in plans:
            form_data["plan"] = plan  # Add the plan to the form data
            response = self.client.post(
                f"/rendez-vous/{self.event.id}/inscription/", form_data
            )
            logger.debug(f"Response: {response}")
            self.assertEqual(response.status_code, 302)
            # Check if checkout session is created
            logger.debug(f"Response URL: {response.url}")
            self.assertTrue(response.url)

    # @unittest.skip("Skip for now")
    def test_invalid_post(self):
        """
        If the user inputs invalid data, the form should be displayed again with the error messages.
        """
        response = self.client.post(
            f"/rendez-vous/{self.event.id}/inscription/",
            {
                "fname": "John",
                "lname": "Doe",
                "email": "invalid_email",
                "membership_status": "isMember",
                "zip_code": "1228",
                "city": "Plan-les-Ouates",
            },
        )
        # Get context data from the response
        error_inputs = response.context.get(
            "error_inputs"
        )  # Returns a dict_keys object
        error_messages = response.context.get("error_messages")
        logger.debug(f"Error inputs: {error_inputs}")
        logger.debug(f"Error messages: {error_messages}")
        logger.debug(f"Response: {response}")
        # Checks
        error_inputs_list = list(error_inputs)  # Convert the dict_keys object to a list
        self.assertTemplateUsed(response, "pages/event-registration.html")
        self.assertEqual(error_inputs_list, ["plan", "email", "address"])
        self.assertTrue(error_messages)
