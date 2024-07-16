from django.test import TestCase, override_settings
import unittest
from .views import EventRegistrationView
from .models import Event, Participant, EventParticipants
from Invisibles23.logging_config import logger
import random


class EventRegistrationViewTest(TestCase):
    """
    This test case will test a registration submission for an event. It'll check if:
    - The user is redirected to a stripe checkout page
    - The user is redirected to the event registration page if the form is invalid
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
        # Create a test event
        Event.objects.create(
            is_talk_event=False,
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
        logger.info(f"Created event for testing: {self.event}")

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


class EventParticipantsModelTest(TestCase):
    """
    This test case will test the EventParticipants model. It will test if:
    - A participant can be correctly associated with an event
    - An event/participant relation cannot be created if it already exists
    - The EventParticipants model can correctly count the number of participants for an event
    - The EventParticipants model will refuse to create a relation if the event is fully booked
    - If an event was fully booked but a participant cancels, check if the event is no longer fully booked
    """

    def setUp(self):
        # Create a test event with a participants limit of 10
        self.event = Event.objects.create(
            is_talk_event=True,
            title="Test Event",
            short_description="This is a test event",
            full_description="This is a test event, please ignore it.",
            date="2022-12-12",
            start_time="12:00",
            end_time="14:00",
            address="Chemin de la Mairie 1",
            link="https://www.myevent.com",
            participants_limit=10,
        )
        logger.debug(f"Created event for testing: {self.event.title} with participant limit: {self.event.participants_limit}")

        # Create a list of test participants with real names
        self.test_participants = [
            {"fname": "John", "lname": "Doe"},
            {"fname": "Jane", "lname": "Smith"},
            {"fname": "Michael", "lname": "Johnson"},
            {"fname": "Emily", "lname": "Brown"},
            {"fname": "David", "lname": "Wilson"},
            {"fname": "Sarah", "lname": "Taylor"},
            {"fname": "Christopher", "lname": "Anderson"},
            {"fname": "Jessica", "lname": "Thomas"},
            {"fname": "Matthew", "lname": "Jackson"},
            {"fname": "Olivia", "lname": "White"},
            {"fname": "Daniel", "lname": "Harris"}
        ]

        # Create 11 participants using a loop
        self.participants = []
        for i, participant_data in enumerate(self.test_participants):
            participant = Participant.objects.create(
                fname=participant_data["fname"],
                lname=participant_data["lname"],
                email=f"{participant_data['fname'].lower()}.{participant_data['lname'].lower()}@test.com",
                address=f"{random.randint(1, 100)} Test Street",
                zip_code=f"{random.randint(10000, 99999)}",
                city="Test City",
            )
            self.participants.append(participant)
            logger.debug(f"Created participant for testing: {participant.fname} {participant.lname}")

    #@unittest.skip("Skip for now")
    def test_associate_participant(self):
        """Test if a participant can be correctly associated with an event"""
        EventParticipants.objects.create(event=self.event, participant=self.participants[0])
        self.assertEqual(self.event.participants.count(), 1)
        logger.debug(f"Participants for event: {self.event.participants.all()}")
        participant = self.event.participants.first()
        self.assertEqual(participant.email, f"{self.test_participants[0]['fname'].lower()}.{self.test_participants[0]['lname'].lower()}@test.com")
        logger.debug(f"Successfully associated participant {participant.fname} {participant.lname} with event '{self.event.title}'")

    #@unittest.skip("Skip for now")
    def test_associate_participant_twice(self):
        """Test if an event/participant relation cannot be created if it already exists"""
        EventParticipants.objects.create(event=self.event, participant=self.participants[0])
        self.assertEqual(self.event.participants.count(), 1)
        logger.debug(f"Participants for event: {self.event.participants.all()}")
        logger.debug("Attempting to associate the same participant again...")
        with self.assertRaises(Exception):
            EventParticipants.objects.create(event=self.event, participant=self.participants[0])
        logger.debug("Successfully raised exception when trying to associate participant twice")

    #@unittest.skip("Skip for now")
    def test_participants_limit(self):
        """Test if the EventParticipants model correctly handles the participants limit"""
        logger.debug(f"The limit of participants for event {self.event.title} is set to {self.event.participants_limit} participants.")
        
        for i in range(11):
            if i < 10:
                EventParticipants.objects.create(event=self.event, participant=self.participants[i])
                updated_event = Event.objects.get(pk=self.event.id)
                self.assertEqual(self.event.participants.count(), i + 1)
                self.assertEqual(updated_event.is_fully_booked, i == 9)
                logger.debug(f"Added participant {i+1}: {self.participants[i].fname} {self.participants[i].lname}")
                logger.debug(f"Participants for event: {self.event.participants.all()}")
                logger.debug(f"Event {updated_event.title} is {'fully booked' if updated_event.is_fully_booked else 'not fully booked'}, state: {updated_event.is_fully_booked}")
            else:
                logger.debug(f"Attempting to add participant {i+1} (exceeding limit)...")
                with self.assertRaises(Exception):
                    EventParticipants.objects.create(event=self.event, participant=self.participants[i])
                logger.debug("Successfully raised exception when trying to exceed participant limit")

        final_event = Event.objects.get(pk=self.event.id)
        self.assertTrue(final_event.is_fully_booked)
        self.assertEqual(final_event.participants.count(), 10)
        logger.debug(f"Final event state: Fully booked: {final_event.is_fully_booked}, Participant count: {final_event.participants.count()}")

    #@unittest.skip("Skip for now")
    def test_cancel_participant(self):
        """Test if an event is no longer fully booked if a participant cancels"""
        for i in range(10):
            EventParticipants.objects.create(event=self.event, participant=self.participants[i])
        updated_event = Event.objects.get(pk=self.event.id)
        self.assertTrue(updated_event.is_fully_booked)
        logger.debug(f"Event {updated_event.title} is fully booked, state: {updated_event.is_fully_booked}")
        logger.debug(f"Participant {self.participants[0].fname} {self.participants[0].lname} will be removed from the event")
        EventParticipants.delete(EventParticipants.objects.get(event=self.event, participant=self.participants[0]))
        updated_event = Event.objects.get(pk=self.event.id)
        logger.debug(f"New participant count: {self.event.participants.count()}")
        self.assertFalse(updated_event.is_fully_booked)
        logger.debug(f"Event {updated_event.title} is no longer fully booked, state: {updated_event.is_fully_booked}")
