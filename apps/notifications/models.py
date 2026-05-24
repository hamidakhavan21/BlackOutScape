from django.db import models
from django.utils import timezone

from apps.projects.models import Project
from core.utils.models.base_models import TimestampedModel


class NotificationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PROCESSING = "PROCESSING", "Processing"
    RETRYING = "RETRYING", "Retrying"
    DELIVERED = "DELIVERED", "Delivered"
    FAILED = "FAILED", "Failed"
    DEAD_LETTER = "DEAD_LETTER", "Dead Letter"


class Notification(TimestampedModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    external_id = models.CharField(
        max_length=255,
        unique=True,
    )

    payload = models.JSONField()

    status = models.CharField(
        max_length=32,
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING,
    )

    retry_count = models.PositiveIntegerField(default=0)

    max_retries = models.PositiveIntegerField(default=5)

    scheduled_at = models.DateTimeField(default=timezone.now)

    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    idempotency_key = models.UUIDField(unique=True)
    payload_hash = models.CharField(
        max_length=64,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.external_id} - {self.status}"
