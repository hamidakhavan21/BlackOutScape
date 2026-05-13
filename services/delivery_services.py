from django.utils import timezone
from django.db import transaction

from apps.deliveries.models import (
    DeliveryAttempt,
    DeliveryAttemptStatus,
)

from apps.notifications.models import (
    Notification,
    NotificationStatus,
)

from apps.providers.sms.kavenegar.provider import (
    KavenegarProvider,
)
from core.logging.logger import logger
from apps.providers.router import ProviderRouter

class NotificationDeliveryService:

    provider_name, provider = ProviderRouter.get_provider()
    
    @classmethod
    def deliver(cls, notification: Notification):
        with transaction.atomic():
            
            if notification.status == NotificationStatus.DELIVERED:
                return

            notification.status = NotificationStatus.PROCESSING
            notification.save(update_fields=["status"])

            try:
                logger.info(
                    "notification_delivery_started",
                    extra={
                        "notification_id": notification.id,
                        "external_id": notification.external_id,
                    }
                )
                response = cls.provider.send(notification.payload)

                DeliveryAttempt.objects.create(
                    notification=notification,
                    status=DeliveryAttemptStatus.SUCCESS,
                    provider=response["provider"],
                    response=response,
                    latency_ms=response["latency_ms"],
                )

                notification.status = NotificationStatus.DELIVERED
                notification.delivered_at = timezone.now()

                notification.save(
                    update_fields=[
                        "status",
                        "delivered_at",
                    ]
                )

            except Exception as exc:

                DeliveryAttempt.objects.create(
                    notification=notification,
                    status=DeliveryAttemptStatus.FAILURE,
                    provider="kavenegar",
                    error_message=str(exc),
                )

                raise exc