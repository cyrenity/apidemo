import json
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from api.models import GENDER, ProcessQueueAction, Tasks
from api.serializers import TaskSerializer, ProcessQueueActionSerializer


class PqCreateAPIViewTestCase(APITestCase):
    url = reverse("pq-list")

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_processqueue(self):
        data  = {
                "name": "John",
                "gender": "male",
                "type": "type1",
                "remarks": "Nothing much to say!",
                "citizen_number": 3630271385869,
                "phone": 923005004297
            }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_user_processqueue(self):
        """
        Test to verify user processqueue list
        """
        ProcessQueueAction.objects.create(
            owner=self.user, 
            name="Clean the car!", 
            tracking_id="23432434", 
            phone=923005004297, 
            gender="male",
            type="type2",
            remarks="Done!",
            citizen_number=3630271385869
        )
        response = self.client.get(self.url)
        self.assertTrue(len(json.loads(response.content)) == ProcessQueueAction.objects.count())

