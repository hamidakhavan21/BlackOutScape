import uuid

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer
from apps.notifications.tasks import process_notification
from core.utils.hash import generate_payload_hash


class NotificationCreateAPIView(APIView):
    def post(self, request):
        breakpoint()
        serializer = NotificationSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        payload_hash = generate_payload_hash(data)

        if Notification.objects.filter(payload_hash=payload_hash).exists():
            return Response(
                {"detail": "Duplicate notification payload."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        notification = serializer.save(
            external_id=str(uuid.uuid4()), payload_hash=payload_hash
        )

        process_notification.delay(notification.id)

        return Response(
            NotificationSerializer(notification).data,
            status=status.HTTP_201_CREATED,
        )
