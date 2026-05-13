from celery import shared_task

from apps.notifications.models import (
    Notification,
    NotificationStatus,
)

from services.delivery_services import (
    NotificationDeliveryService,
)

from core.retry.backoff import exponential_backoff

@shared_task(bind=True, max_retries=5)
def process_notification(self, notification_id):
    notification = Notification.objects.get(id=notification_id)

    try:

        NotificationDeliveryService.deliver(notification)

    except Exception:

        notification.retry_count += 1

        if notification.retry_count >= notification.max_retries:

            notification.status = NotificationStatus.DEAD_LETTER

            notification.save(
                update_fields=[
                    "retry_count",
                    "status",
                ]
            )

            return

        notification.status = NotificationStatus.RETRYING

        notification.save(
            update_fields=[
                "retry_count",
                "status",
            ]
        )

        countdown = exponential_backoff(notification.retry_count)

        raise self.retry(countdown=countdown)