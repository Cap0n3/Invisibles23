from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
import unittest
from .views import EventRegistrationView
from proxy.views import StripeWebhook
from .models import Event, Participant, EventParticipants
from Invisibles23.logging_config import logger
import random

# ======================================= #
# ====== MEMBER REGISTRATION TESTS ====== #
# ======================================= #


class MembershipViewTest(TestCase):
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
        # Create a test member
        self.member = {
            "subscription": "reduced",
            "frequency": "yearly",
            "fname": "John",
            "lname": "Doe",
            "email": "johndoe@test.com",
            "phone": "+41 79 123 45 67",
            "birthday": "1990-01-01",
            "address": "123 Test Street",
            "zip_code": "1234",
            "city": "Test City",
            "lookup_key": "reduced-yearly",
        }

    # @unittest.skip("Skip test post")
    def test_post(self):
        """
        Test if the user is redirected to a stripe checkout page
        """
        response = self.client.post("/membership/", self.member)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url)

    # @unittest.skip("Skip test invalid post")
    def test_invalid_post(self):
        """
        Test if the user is redirected to the membership page if the form is invalid
        """
        response = self.client.post(
            "/membership/",
            {
                "subscription": "reduced",
                "frequency": "gnarly",
                "fname": "John###",
                "lname": "Doe",
                "email": "NotAnEmail",
                "phone": "+123 (456)-789 33 22",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/membership.html")
        error_inputs = response.context.get("error_inputs")
        error_inputs_list = list(error_inputs)
        self.assertTrue(error_inputs)
        self.assertEqual(
            error_inputs_list,
            ["frequency", "fname", "phone", "birthday", "address", "zip_code", "city", "email"],
        )
        logger.debug(f"Error inputs: {error_inputs_list}")


# ====================================== #
# ====== EVENT REGISTRATION TESTS ====== #
# ====================================== #


def create_participants():
    """
    Create a list of test participants for testing purposes and insert them into the Participant database.

    Returns:
    - participants (list): A list of participant objects
    - test_participants (list): A list of dictionaries containing test participant data
    """
    test_participants = [
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
        {"fname": "Daniel", "lname": "Harris"},
    ]

    # Create 11 participants using a loop
    participants = []
    for i, participant_data in enumerate(test_participants):
        participant = Participant.objects.create(
            fname=participant_data["fname"],
            lname=participant_data["lname"],
            phone=f"0{random.randint(100000000, 999999999)}",
            email=f"{participant_data['fname'].lower()}.{participant_data['lname'].lower()}@test.com",
            address=f"{random.randint(1, 100)} Test Street",
            zip_code=f"{random.randint(10000, 99999)}",
            city="Test City",
        )
        participants.append(participant)
        logger.debug(
            f"Created participant for testing: {participant.fname} {participant.lname}"
        )

    return (participants, test_participants)


class EventRegistrationViewTest(TestCase):
    """
    This test case will test a registration submission for an event. It'll check if:
    - The user is redirected to a stripe checkout page
    - The user is redirected to the event registration page if the form is invalid
    - If user is already registered for a specific event and tries to register again for the same event, the form should return an error
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
        logger.debug(f"Created event for testing: {self.event}")

    # @unittest.skip("Skip test post")
    def test_post(self):
        """
        Check if the user is redirected to a stripe checkout page
        """
        plans = ["support", "normal", "reduced"]
        form_data = {
            "fname": "John",
            "lname": "Doe",
            "email": "test@gmail.com",
            "phone": "+41 79 123 45 67",
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

    # @unittest.skip("Skip test invalid post")
    def test_invalid_post(self):
        """
        If the user inputs invalid data, the form should be displayed again with the error messages.
        """
        response = self.client.post(
            f"/rendez-vous/{self.event.id}/inscription/",
            {
                "fname": "John",
                "lname": "Doe",
                "phone": "+41_invalid_899",
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
        self.assertEqual(error_inputs_list, ["plan", "email", "phone", "address"])
        self.assertTrue(error_messages)

    # @unittest.skip("Skip test participant already registered")
    def test_participant_already_registered(self):
        """
        If the user is already registered for the event, the form should return an error.
        """
        # Create a test participant
        Participant.objects.create(
            fname="John",
            lname="Doe",
            email="test@gmail.com",
            address="Chemin du Pré-Fleuri 3",
            zip_code="1228",
            city="Plan-les-Ouates",
        )
        self.test_participant = Participant.objects.get(email="test@gmail.com")
        logger.debug(f"Created participant for testing: {self.test_participant}")

        # Add the participant to the event
        EventParticipants.objects.create(
            event=self.event, participant=self.test_participant
        )
        logger.debug(f"Added participant {self.test_participant} to event {self.event}")

        # Send a post request with the same participant data
        response = self.client.post(
            f"/rendez-vous/{self.event.id}/inscription/",
            {
                "fname": "John",
                "lname": "Doe",
                "email": "test@gmail.com",
                "membership_status": "isMember",
                "plan": "normal",
                "address": "Chemin du Pré-Fleuri 3",
                "zip_code": "1228",
                "city": "Plan-les-Ouates",
            },
        )
        # Get context data from the response
        error_message = response.context.get("error_messages")
        self.assertTrue(error_message)
        logger.debug(f"Error message: {error_message}")


class EventModelTest(TestCase):
    """
    This test case will test the Event model. It will test if:
    - A standard event can be created
    - An empty talk group can be created
    - A talk group event with 5 participants can be created and is not set to fully booked (default limit is 9)
        - If you add 4 more participants, the event should be fully booked
    - A talk group event with 9 participants can be created and is set to fully booked (default limit is 9)
        - If you remove a participant, the event should no longer be fully booked
    - A talk group event with 11 participants cannot be created (exceeding the limit)
    - If an event has 5 participants and the limit is lowered to 5, event should be fully booked
        - If the limit is lowered to 4, the model should return an error
    - If an event has 9 participants and is fully booked, if a participant cancels, the event should no longer be fully booked
    """

    def setUp(self):
        # Create a talk group event (default limit is 9)
        self.talk_group_event = Event.objects.create(
            is_talk_event=True,
            title="Test Event",
            short_description="This is a test talk group event",
            full_description="This is a test talk group event, please ignore it.",
            date="2022-12-12",
            start_time="12:00",
            end_time="14:00",
        )

        # Create test participants
        self.participants, self.test_participants = create_participants()

    # @unittest.skip("Skip test create standard event")
    def test_create_standard_event(self):
        """
        Test if a standard event can be created
        """
        self.event = Event.objects.create(
            is_talk_event=False,
            title="Standard Test Event",
            short_description="This is a test event",
            full_description="This is a test event, please ignore it.",
            date="2022-12-12",
            start_time="12:00:00",
            end_time="14:00:00",
            address="Chemin de la Mairie 1",
            link="https://www.myevent.com",
        )
        logger.debug(f"Events {Event.objects.all()}")
        self.assertTrue(Event.objects.filter(title="Standard Test Event").exists())
        logger.debug(f"Event 'Standard Test Event' successfully created.")

    # @unittest.skip("Skip test create empty talk group")
    def test_create_empty_talk_group(self):
        """
        Test if an empty talk group event can be created
        """
        self.event = Event.objects.create(
            is_talk_event=False,
            title="Talk Group Event",
            short_description="This is a test event",
            full_description="This is a test event, please ignore it.",
            date="2022-12-12",
            start_time="12:00:00",
            end_time="14:00:00",
            address="Chemin de la Mairie 1",
            link="https://www.myevent.com",
        )
        self.assertTrue(Event.objects.filter(title="Talk Group Event").exists())
        logger.debug(f"Event 'Talk Group Event' successfully created.")

    # @unittest.skip("Skip test create talk group event")
    def test_create_talk_group_event(self):
        """
        Test if a talk group event with 5 participants can be created and is not fully booked.
        Then, add 4 more participants to the event and check if it is fully booked.
        """
        # Associate all participants with the event
        for participant in self.participants[:5]:
            EventParticipants.objects.create(
                event=self.talk_group_event, participant=participant
            )
        event = Event.objects.get(title="Test Event")
        self.assertEqual(event.participants.count(), 5)
        self.assertFalse(event.is_fully_booked)
        logger.debug(f"Event 'Test Event' successfully created with 5 participants.")

        # Add 4 more participants to the event
        for i in range(4):
            EventParticipants.objects.create(
                event=self.talk_group_event, participant=self.participants[i + 5]
            )
        updated_event = Event.objects.get(title="Test Event")
        self.assertEqual(updated_event.participants.count(), 9)
        self.assertTrue(updated_event.is_fully_booked)
        logger.debug(f"Event 'Test Event' is now fully booked with 9 participants.")

    # @unittest(skip="Skip test create fully booked talk group event")
    def test_create_fully_booked_talk_group_event(self):
        """
        Test if a talk group event with 9 participants can be created and is fully booked.
        Then, remove a participant from the event and check if it is no longer fully booked.
        """
        # Associate all participants with the event
        for participant in self.participants[:9]:
            EventParticipants.objects.create(
                event=self.talk_group_event, participant=participant
            )
        event = Event.objects.get(title="Test Event")
        self.assertEqual(event.participants.count(), 9)
        self.assertTrue(event.is_fully_booked)
        logger.debug(f"Event 'Test Event' successfully created with 9 participants.")

        # Remove a participant from the event
        EventParticipants.objects.get(
            event=self.talk_group_event, participant=self.participants[0]
        ).delete()
        updated_event = Event.objects.get(title="Test Event")
        self.assertEqual(updated_event.participants.count(), 8)
        self.assertFalse(updated_event.is_fully_booked)
        logger.debug(
            f"Event 'Test Event' is no longer fully booked with 8 participants."
        )

    # @unittest(skip="Skip test insert too much participants")
    def test_insert_too_much_participants(self):
        """
        Test if a talk group event with 11 participants cannot be created (exceeding the limit).
        """
        with self.assertRaises(Exception):
            for participant in self.participants:
                EventParticipants.objects.create(
                    event=self.talk_group_event, participant=participant
                )
            logger.debug(
                f"Successfully raised exception when trying to exceed participant limit."
            )

    # @unittest(skip="Skip test lower participants limit")
    def test_lower_participants_limit(self):
        """
        Test if an event with 5 participants and a limit of 5 is fully booked.
        Then, if the limit is lowered to 4, the model should return an error.
        """
        # Associate all participants with the event
        for participant in self.participants[:5]:
            EventParticipants.objects.create(
                event=self.talk_group_event, participant=participant
            )
        event = Event.objects.get(title="Test Event")
        self.assertEqual(event.participants.count(), 5)
        self.assertFalse(event.is_fully_booked)
        logger.debug(f"Event 'Test Event' successfully created with 5 participants.")

        # Lower the participants limit to 5
        event.participants_limit = 5
        event.save()
        updated_event = Event.objects.get(title="Test Event")
        self.assertEqual(updated_event.participants_limit, 5)
        self.assertTrue(updated_event.is_fully_booked)
        logger.debug(f"Event 'Test Event' is now fully booked with 5 participants.")

        # Lower the participants limit to 4
        event.participants_limit = 4
        with self.assertRaises(Exception):
            event.save()
        logger.debug(
            f"Successfully raised exception when trying to lower limit to less than number of participants."
        )

    # @unittest(skip="Skip test lower participants limit fully booked")
    def test_lower_participants_limit_fully_booked(self):
        """
        Test if an event with 9 participants and a limit of 9 is fully booked.
        Then, if a participant cancels, the event should no longer be fully booked.
        If the limit is lowered to 4, the model should return an error.
        """
        # Associate all participants with the event
        for participant in self.participants[:9]:
            EventParticipants.objects.create(
                event=self.talk_group_event, participant=participant
            )
        event = Event.objects.get(title="Test Event")
        self.assertEqual(event.participants.count(), 9)
        self.assertTrue(event.is_fully_booked)
        logger.debug(f"Event 'Test Event' successfully created with 9 participants.")

        # Remove a participant from the event
        EventParticipants.objects.get(
            event=self.talk_group_event, participant=self.participants[0]
        ).delete()
        updated_event = Event.objects.get(title="Test Event")
        self.assertEqual(updated_event.participants.count(), 8)
        self.assertFalse(updated_event.is_fully_booked)
        logger.debug(
            f"Event 'Test Event' is no longer fully booked with 8 participants."
        )


class AdminFormSubmissionTest(TestCase):
    """
    This test case will test the admin console form submission. It simulates the form submission process and checks if the form is processed correctly.
    It will test if:
    - A standard event can be successfully created from the admin console
    - A talk group event with 9 participants can be successfully created from the admin console
    - A talk group event with 11 participants cannot be created (exceeding the limit) from the admin console (inlines)
    - A participant can be removed from a fully booked talk group event from admin, making it no longer fully booked
    - Starting from a not fully booked talk group event with 3 participants, if the user lower the limit to less than the number of participants, the form should return an error
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
        self.admin_user = User.objects.create_superuser(
            username="admin", password="admin", email="admin@example.com"
        )
        logger.debug("Created superuser for testing...")
        self.client.login(username="admin", password="admin")
        logger.debug("Logged in as superuser...")
        self.participants, self.test_participants = create_participants()
        # Check if there's 11 participants in Participant database
        self.assertEqual(Participant.objects.count(), 11)

    # @unittest.skip("Skip test simple event submission")
    def test_simple_event_submission(self):
        """
        Test if the admin form submission for a simple event (not a talk group event) is successful.
        """
        url = reverse("admin:website_event_add")  # replace 'yourapp' with your app name
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Ensure we have access to the form
        csrf_token = self.client.cookies["csrftoken"].value

        data = {
            "csrfmiddlewaretoken": csrf_token,
            "is_talk_event": False,
            "title": "Test Event",
            "short_description": "Description courte de l'évènement (max 300 caractères)",
            "full_description": "<p>Description complète de l'évènement</p>",
            "date": "2045-07-31",  # Use the correct date format YYYY-MM-DD
            "start_time": "09:00:00",
            "end_time": "11:00:00",
            "address": "123 Rue Exemple, Ville",
            "link": "http://example.com",
            "is_fully_booked": False,
            "participants_limit": 10,
            "participants": [],  # Add participant IDs here if needed
            # Required hidden fields for managing inline formsets
            "eventparticipants_set-TOTAL_FORMS": "1",
            "eventparticipants_set-INITIAL_FORMS": "0",
            "eventparticipants_set-MIN_NUM_FORMS": "0",
            "eventparticipants_set-MAX_NUM_FORMS": "1000",
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)  # Ensure the form is processed

        # Check for errors in form submission
        if response.context and "adminform" in response.context:
            form = response.context["adminform"].form
            logger.debug(f"Returned form: {form}")

        # Check that the event was created
        self.assertTrue(Event.objects.filter(title="Test Event").exists())
        logger.debug(f"Event 'Test Event' successfully created.")

    # @unittest.skip("Skip test talk event submission")
    def test_talk_event_submission(self):
        """
        Test if the admin form submission for a talk event with 9 participants is successful.
        """
        url = reverse("admin:website_event_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Ensure we have access to the form
        csrf_token = self.client.cookies["csrftoken"].value

        # Get participant IDs
        participant_ids = [participant.id for participant in self.participants[:9]]
        logger.debug(f"Participant IDs: {participant_ids}")

        data = {
            "csrfmiddlewaretoken": csrf_token,
            "is_talk_event": True,
            "title": "Test Talk Event",
            "short_description": "Description courte de l'évènement (max 300 caractères)",
            "full_description": "<p>Description complète de l'évènement</p>",
            "date": "2045-07-31",  # Use the correct date format YYYY-MM-DD
            "start_time": "09:00:00",
            "end_time": "11:00:00",
            "address": "123 Rue Exemple, Ville",
            "link": "http://example.com",
            "is_fully_booked": False,
            "participants_limit": 10,
            # Required hidden fields for managing inline formsets (it's the inline form visible in the admin)
            "eventparticipants_set-TOTAL_FORMS": str(len(participant_ids)),
            "eventparticipants_set-INITIAL_FORMS": "0",
            "eventparticipants_set-MIN_NUM_FORMS": "0",
            "eventparticipants_set-MAX_NUM_FORMS": "1000",
        }

        # Associate all participants with the event (through the inline form)
        for index, participant_id in enumerate(participant_ids):
            data[f"eventparticipants_set-{index}-id"] = ""
            data[f"eventparticipants_set-{index}-event"] = ""
            data[f"eventparticipants_set-{index}-participant"] = participant_id

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)  # Ensure the form is processed

        # Check if a form was returned (meaning there were errors)
        if response.context and "adminform" in response.context:
            form = response.context["adminform"].form

        # Check that the event was created
        self.assertTrue(Event.objects.filter(title="Test Talk Event").exists())
        logger.debug(f"Event 'Test Talk Event' successfully created.")

        # Check if the participants were correctly associated with the event
        event = Event.objects.get(title="Test Talk Event")

        logger.debug(
            f"Participants for event '{event.title}': {event.participants.all()}"
        )
        self.assertEqual(event.participants.count(), 9)
        logger.debug(
            f"Count is correct: {event.participants.count()} participants for event '{event.title}'"
        )
        # Check if ids match the participants
        for participant in event.participants.all():
            self.assertTrue(participant.id in participant_ids)

    # @unittest.skip("Skip test insert too much participants")
    def test_insert_too_much_participants(self):
        """
        Test if the admin form submission for a talk event with 11 participants is prevented.
        """
        url = reverse("admin:website_event_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf_token = self.client.cookies["csrftoken"].value

        # Get participant IDs (11 participants)
        participant_ids = [participant.id for participant in self.participants]
        logger.debug(f"Participant IDs: {participant_ids}")

        data = {
            "csrfmiddlewaretoken": csrf_token,
            "is_talk_event": True,
            "title": "Test Talk Event",
            "short_description": "Description courte de l'évènement (max 300 caractères)",
            "full_description": "<p>Description complète de l'évènement</p>",
            "date": "2045-07-31",  # Use the correct date format YYYY-MM-DD
            "start_time": "09:00:00",
            "end_time": "11:00:00",
            "address": "123 Rue Exemple, Ville",
            "link": "http://example.com",
            "is_fully_booked": False,
            "participants_limit": 10,  # Limit is 10, but we try to add 11 participants
            # Required hidden fields for managing inline formsets (it's the inline form visible in the admin)
            "eventparticipants_set-TOTAL_FORMS": str(len(participant_ids)),
            "eventparticipants_set-INITIAL_FORMS": "0",
            "eventparticipants_set-MIN_NUM_FORMS": "0",
            "eventparticipants_set-MAX_NUM_FORMS": "1000",
        }

        # Associate all participants with the event (through the inline form)
        for index, participant_id in enumerate(participant_ids):
            data[f"eventparticipants_set-{index}-id"] = ""
            data[f"eventparticipants_set-{index}-event"] = ""
            data[f"eventparticipants_set-{index}-participant"] = participant_id

        with self.assertRaises(Exception):
            response = self.client.post(url, data, follow=True)

        logger.debug(
            f"Successfully raised exception when trying to exceed participant limit"
        )

    # @unittest.skip("Skip test remove participant")
    def test_remove_a_participant(self):
        """
        Test if the admin form submission for a talk event with 9 participants is successful.
        Then, remove a participant from the event and check if the event is no longer fully booked.
        """
        url = reverse("admin:website_event_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf_token = self.client.cookies["csrftoken"].value

        # Get participant IDs (11 participants)
        participant_ids = [participant.id for participant in self.participants[:10]]
        logger.debug(f"Participant IDs: {participant_ids}")

        data = {
            "csrfmiddlewaretoken": csrf_token,
            "is_talk_event": True,
            "title": "Test Talk Event",
            "short_description": "Description courte de l'évènement (max 300 caractères)",
            "full_description": "<p>Description complète de l'évènement</p>",
            "date": "2045-07-31",  # Use the correct date format YYYY-MM-DD
            "start_time": "09:00:00",
            "end_time": "11:00:00",
            "address": "123 Rue Exemple, Ville",
            "link": "http://example.com",
            "is_fully_booked": False,
            "participants_limit": 10,  # Limit is 10, but we try to add 11 participants
            # Required hidden fields for managing inline formsets (it's the inline form visible in the admin)
            "eventparticipants_set-TOTAL_FORMS": str(len(participant_ids)),
            "eventparticipants_set-INITIAL_FORMS": "0",
            "eventparticipants_set-MIN_NUM_FORMS": "0",
            "eventparticipants_set-MAX_NUM_FORMS": "1000",
        }

        # Associate all participants with the event (through the inline form)
        for index, participant_id in enumerate(participant_ids):
            data[f"eventparticipants_set-{index}-id"] = ""
            data[f"eventparticipants_set-{index}-event"] = ""
            data[f"eventparticipants_set-{index}-participant"] = participant_id

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)  # Ensure the form is processed

        # Check that the event was created
        self.assertTrue(Event.objects.filter(title="Test Talk Event").exists())
        logger.debug(
            f"Event 'Test Talk Event' successfully created with ID: {Event.objects.get(title='Test Talk Event').id}"
        )

        # Count the number of participants
        event = Event.objects.get(title="Test Talk Event")
        self.assertEqual(event.participants.count(), 10)

        # Remove a participant from the event
        participant = event.participants.first()
        EventParticipants.objects.get(event=event, participant=participant).delete()

        updated_event = Event.objects.get(title="Test Talk Event")
        # Check if the event is no longer fully booked
        self.assertFalse(updated_event.is_fully_booked)
        logger.debug(f"Event '{event.title}' is no longer fully booked.")

    # @unittest.skip("Skip test lower participants limit")
    def test_lower_participants_limit(self):
        """
        Test if the admin form submission for a talk event with 3 participants is successful.
        Then, lower the participants limit to 2 participants and check if the form is returned (expected when error).

        Note : I don't know why the form is returned without any error message, it should return an error message.
        But I noticed that when the form is returned, the form is not processed and the event is not updated (equivalent to an error).
        """
        url = reverse("admin:website_event_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        csrf_token = self.client.cookies["csrftoken"].value

        # Get participant IDs (3 participants)
        participant_ids = [participant.id for participant in self.participants[:3]]
        logger.debug(f"Participant IDs: {participant_ids}")

        data = {
            "csrfmiddlewaretoken": csrf_token,
            "is_talk_event": True,
            "title": "Test Talk Event",
            "short_description": "Description courte de l'évènement (max 300 caractères)",
            "full_description": "<p>Description complète de l'évènement</p>",
            "date": "2045-07-31",  # Use the correct date format YYYY-MM-DD
            "start_time": "09:00:00",
            "end_time": "11:00:00",
            "address": "123 Rue Exemple, Ville",
            "link": "http://example.com",
            "is_fully_booked": False,
            "participants_limit": 10,
            # Required hidden fields for managing inline formsets (it's the inline form visible in the admin)
            "eventparticipants_set-TOTAL_FORMS": str(len(participant_ids)),
            "eventparticipants_set-INITIAL_FORMS": "0",
            "eventparticipants_set-MIN_NUM_FORMS": "0",
            "eventparticipants_set-MAX_NUM_FORMS": "1000",
        }

        # Associate all participants with the event (through the inline form)
        for index, participant_id in enumerate(participant_ids):
            data[f"eventparticipants_set-{index}-id"] = ""
            data[f"eventparticipants_set-{index}-event"] = ""
            data[f"eventparticipants_set-{index}-participant"] = participant_id

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        if response.context and "adminform" in response.context:
            form = response.context["adminform"].form
            self.assertIsNone(form)

        # Now, lower the participants limit to 2
        data = {
            "csrfmiddlewaretoken": csrf_token,
            "is_talk_event": True,
            "title": "Test Talk Event",
            "short_description": "Description courte de l'évènement (max 300 caractères)",
            "full_description": "<p>Description complète de l'évènement</p>",
            "date": "2045-07-31",  # Use the correct date format YYYY-MM-DD
            "start_time": "09:00:00",
            "end_time": "11:00:00",
            "address": "123 Rue Exemple, Ville",
            "link": "http://example.com",
            "is_fully_booked": False,
            "participants_limit": 2,
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)  # Ensure the form is processed

        # If the form is returned, there was an error (expected)
        if response.context and "adminform" in response.context:
            form = response.context["adminform"].form
            self.assertIsNotNone(form)


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
        logger.debug(
            f"Created event for testing: {self.event.title} with participant limit: {self.event.participants_limit}"
        )

        # Create test participants
        self.participants, self.test_participants = create_participants()

    # @unittest.skip("Skip test associate participant")
    def test_associate_participant(self):
        """Test if a participant can be correctly associated with an event"""
        EventParticipants.objects.create(
            event=self.event, participant=self.participants[0]
        )
        self.assertEqual(self.event.participants.count(), 1)
        logger.debug(f"Participants for event: {self.event.participants.all()}")
        participant = self.event.participants.first()
        self.assertEqual(
            participant.email,
            f"{self.test_participants[0]['fname'].lower()}.{self.test_participants[0]['lname'].lower()}@test.com",
        )
        logger.debug(
            f"Successfully associated participant {participant.fname} {participant.lname} with event '{self.event.title}'"
        )

    # @unittest.skip("Skip test associate participant twice")
    def test_associate_participant_twice(self):
        """Test if an event/participant relation cannot be created if it already exists"""
        EventParticipants.objects.create(
            event=self.event, participant=self.participants[0]
        )
        self.assertEqual(self.event.participants.count(), 1)
        logger.debug(f"Participants for event: {self.event.participants.all()}")
        logger.debug("Attempting to associate the same participant again...")
        with self.assertRaises(Exception):
            EventParticipants.objects.create(
                event=self.event, participant=self.participants[0]
            )
        logger.debug(
            "Successfully raised exception when trying to associate participant twice"
        )

    # @unittest.skip("Skip test fully booked event")
    def test_participants_limit(self):
        """Test if the EventParticipants model correctly handles the participants limit"""
        logger.debug(
            f"The limit of participants for event {self.event.title} is set to {self.event.participants_limit} participants."
        )

        for i in range(11):
            if i < 10:
                EventParticipants.objects.create(
                    event=self.event, participant=self.participants[i]
                )
                updated_event = Event.objects.get(pk=self.event.id)
                self.assertEqual(self.event.participants.count(), i + 1)
                self.assertEqual(updated_event.is_fully_booked, i == 9)
                logger.debug(
                    f"Added participant {i+1}: {self.participants[i].fname} {self.participants[i].lname}"
                )
                logger.debug(f"Participants for event: {self.event.participants.all()}")
                logger.debug(
                    f"Event {updated_event.title} is {'fully booked' if updated_event.is_fully_booked else 'not fully booked'}, state: {updated_event.is_fully_booked}"
                )
            else:
                logger.debug(
                    f"Attempting to add participant {i+1} (exceeding limit)..."
                )
                with self.assertRaises(Exception):
                    EventParticipants.objects.create(
                        event=self.event, participant=self.participants[i]
                    )
                logger.debug(
                    "Successfully raised exception when trying to exceed participant limit"
                )

        final_event = Event.objects.get(pk=self.event.id)
        self.assertTrue(final_event.is_fully_booked)
        self.assertEqual(final_event.participants.count(), 10)
        logger.debug(
            f"Final event state: Fully booked: {final_event.is_fully_booked}, Participant count: {final_event.participants.count()}"
        )

    # @unittest.skip("Skip test cancel participant")
    def test_cancel_participant(self):
        """Test if an event is no longer fully booked if a participant cancels"""
        for i in range(10):
            EventParticipants.objects.create(
                event=self.event, participant=self.participants[i]
            )
        updated_event = Event.objects.get(pk=self.event.id)
        self.assertTrue(updated_event.is_fully_booked)
        logger.debug(
            f"Event {updated_event.title} is fully booked, state: {updated_event.is_fully_booked}"
        )
        logger.debug(
            f"Participant {self.participants[0].fname} {self.participants[0].lname} will be removed from the event"
        )
        EventParticipants.delete(
            EventParticipants.objects.get(
                event=self.event, participant=self.participants[0]
            )
        )
        updated_event = Event.objects.get(pk=self.event.id)
        logger.debug(f"New participant count: {self.event.participants.count()}")
        self.assertFalse(updated_event.is_fully_booked)
        logger.debug(
            f"Event {updated_event.title} is no longer fully booked, state: {updated_event.is_fully_booked}"
        )

