import uuid

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.models import Notification

from apps.notifications.serializers import (
    NotificationSerializer,
)

from apps.notifications.tasks import (
    process_notification,
)


class NotificationCreateAPIView(APIView):

    def post(self, request):
        breakpoint()
        serializer = NotificationSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        notification = serializer.save(
            external_id=str(uuid.uuid4())
        )

        process_notification.delay(notification.id)

        return Response(
            NotificationSerializer(notification).data,
            status=status.HTTP_201_CREATED,
        )