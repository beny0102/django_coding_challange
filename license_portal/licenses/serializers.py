from licenses.models import MailLog, License
from rest_framework import serializers


class MailLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailLog
        fields = ['sent_datetime', 'reason', 'license']

class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ['id', 'license_type', 'package', 'client', 'expiration_datetime', 'created_datetime']