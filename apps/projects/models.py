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
