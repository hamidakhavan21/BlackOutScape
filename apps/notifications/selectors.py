from apps.notifications.models import Notification


def get_pending_notifications():
    return Notification.objects.filter(status="PENDING")
