from django.shortcuts import render
from django.http import HttpRequest

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from licenses.models import License, LicenseType, Package, Client

import random

from django.utils import timezone



# Create your views here.


class GenerateLicenseView(APIView):
    """
    Generate a random license soon to expire
    """
    def post(self, request: HttpRequest, *args, **kwargs):

        random_expirations = [
            timezone.now() + timezone.timedelta(days=7),
            timezone.now() + timezone.timedelta(days=30),
            timezone.now() + timezone.timedelta(days=120)
        ]

        license_type = random.choice(LicenseType.get_choices())[1]
        package = random.choice(Package.get_choices())[1]
        client = random.choice(Client.objects.all())
        expiration_datetime = random.choice(random_expirations) + timezone.timedelta(minutes=1)

        license = License.objects.create(
            license_type=license_type,
            package=package,
            client=client,
            expiration_datetime=expiration_datetime
        )

        license.save()

        return Response(status=status.HTTP_201_CREATED, data={
            'id': license.id,
            'license_type': license_type,
            'package': package,
            'client': client.id,
            'exporation_datetime': license.expiration_datetime
        })