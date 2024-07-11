from django.test import TestCase
import unittest
from .views import EventRegistrationView
from .models import Event

class EventRegistrationViewTest(TestCase):
    def setUp(self):
        # Create a test event
        Event.objects.create(
            title='Test Event',
            short_description='This is a test event',
            full_description='This is a test event, please ignore it.',
            date='2022-12-12',
            start_time='12:00',
            end_time='14:00',
            address='Chemin de la Mairie 1',
            link='https://www.myevent.com',
        )
        self.event = Event.objects.get(title='Test Event')
        
    @unittest.skip("Skip for now")
    def test_get(self):
        response = self.client.get(f'/rendez-vous/{self.event.id}/inscription/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/event-registration.html')
    
    #@unittest.skip("Not implemented yet")
    def test_post(self):
        response = self.client.post(f'/rendez-vous/{self.event.id}/inscription/', {
            'fname': 'John',
            'lname': 'Doe',
            'email': 'test@gmail.com',
            'membership_status': 'isMember',
            'plan': 'reduced',
            'address': 'Chemin du Pré-Fleuri 3',
            'zip_code': '1228',
            'city': 'Plan-les-Ouates',
        })
        # Check if the user is redirected to a stripe checkout page
        self.assertEqual(response.status_code, 302)
    
    #@unittest.skip("Not implemented yet")   
    def test_get_invalid_event(self):
        response = self.client.get('/rendez-vous/1000/inscription/')
        self.assertEqual(response.status_code, 404)
        #self.assertTemplateUsed(response, '404.html')
            
