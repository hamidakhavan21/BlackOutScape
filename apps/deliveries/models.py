from django.db import models

from apps.notifications.models import Notification
from core.utils.models.base_models import CreatedModel


class DeliveryAttemptStatus(models.TextChoices):
    SUCCESS = "SUCCESS", "Success"
    FAILURE = "FAILURE", "Failure"


class DeliveryAttempt(CreatedModel):
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name="attempts",
    )

    status = models.CharField(
        max_length=20,
        choices=DeliveryAttemptStatus.choices,
    )

    provider = models.CharField(max_length=100)

    response = models.JSONField(
        null=True,
        blank=True,
    )

    latency_ms = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    error_message = models.TextField(
        blank=True,
    )
    provider_message_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.notification.external_id} - {self.status}"
