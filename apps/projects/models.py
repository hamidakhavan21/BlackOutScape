from django.db import models

from core.utils.models.base_models import CreatedModel


class Project(CreatedModel):
    name = models.CharField(max_length=255)

    api_key_key = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
    )

    rate_limit = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.name


class APIRequestLog(CreatedModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )

    endpoint = models.CharField(max_length=255)

    method = models.CharField(max_length=10)

    status_code = models.PositiveIntegerField()

    latency_ms = models.PositiveIntegerField()

    idempotency_key = models.UUIDField(
        null=True,
        blank=True,
    )

    request_hash = models.CharField(
        max_length=64,
        blank=True,
    )
