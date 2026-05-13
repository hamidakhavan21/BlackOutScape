from django.urls import path

from apps.notifications.views import NotificationCreateAPIView

urlpatterns = [
    path("", NotificationCreateAPIView.as_view(), name="notifications"),
]
