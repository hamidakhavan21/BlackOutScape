from rest_framework import serializers

from apps.notifications.models import Notification
from apps.projects import models


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ["project", "payload", "idempotency_key"]