from django.db import models


class ProviderType(models.TextChoices):
    SMS = "SMS", "SMS"
    EMAIL = "EMAIL", "EMAIL"
    WEBHOOK = "WEBHOOK", "WEBHOOK"