from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from licenses.models import License, LicenseType, Package, Client, MailLog

import random

class LicenseTests(TestCase):
    """ Test module for License model """

    fixtures = [
        './dump/user.json',
        './dump/clients.json',
        './dump/licenses.json'
        ]

    def setUp(self):
        self.client = APIClient()


    def test_get_all_licenses(self):
        """ Test if the API can get all licenses """
        response = self.client.get(reverse('licenses-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_license(self):
        """ Test if the API can get a valid license """
        response = self.client.get(reverse('licenses-detail', kwargs={'pk': 1}))
        license = License.objects.get(pk=1)
        self.assertEqual(response.data['client'], license.client.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_license(self):
        """ Test if the API can get a invalid license """
        response = self.client.get(reverse('licenses-detail', kwargs={'pk': 100000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_random_license(self):
        """ Test if the API can generate a random license """
        response = self.client.post("/api/v1/random/license")
        created_license = License.objects.get(pk=response.data['id'])

        self.assertEqual(created_license.client.id, response.data['client'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class MailLogTests(TestCase):
    """ Test module for MailLog model """

    fixtures = [
        './dump/user.json',
        './dump/clients.json',
        './dump/licenses.json',
        './dump/maillog.json'
        ]

    def setUp(self):
        self.client = APIClient()

    def test_get_last_maillogs(self):
        """ Test if the API can get last maillogs """
        length = random.randint(1, 7)
        response = self.client.get(f'/api/v1/maillogs/{length}/')
        self.assertEqual(len(response.data), length)
        self.assertEqual(response.status_code, status.HTTP_200_OK)