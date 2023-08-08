from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from snippets.models import Schedule, Schedules
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer, ScheduleSerializer, SchedulesSerializer, CreateScheduleSerializer
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from snippets.telegram import client


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def __init__(self, *args, **kwargs):
        super(ScheduleViewSet, self).__init__(*args, **kwargs)
        self.serializer_action_classes = {
            'list': ScheduleSerializer,
            'create': CreateScheduleSerializer,
            'retrieve': ScheduleSerializer,
            'update': ScheduleSerializer,
            'partial_update': ScheduleSerializer,
            'destroy': ScheduleSerializer,
        }

    def get_serializer_class(self, *args, **kwargs):
        """Instantiate the list of serializers per action from class attribute (must be defined)."""
        kwargs['partial'] = True
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(ScheduleViewSet, self).get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ActualizeSchedule(GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    @swagger_auto_schema(request_body=SchedulesSerializer)
    def post(self, request, *args, **kwargs):
        req_sr = SchedulesSerializer(data=request.data)
        req_sr.is_valid(raise_exception=True)

        schedules_to_actualize = Schedules(**req_sr.validated_data)

        for schedule in schedules_to_actualize.schedule_ids:
            schedule.schedule_date = datetime.now() + timedelta(days=1)
            schedule.save()

        res_sr = ScheduleSerializer(schedules_to_actualize.schedule_ids, many=True)
        return Response(res_sr.data)


class SendSchedule(GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    @swagger_auto_schema(request_body=SchedulesSerializer)
    def post(self, request, *args, **kwargs):
        req_sr = SchedulesSerializer(data=request.data)
        req_sr.is_valid(raise_exception=True)

        schedules_to_actualize = Schedules(**req_sr.validated_data)
        telegram_cli = client.Client()

        for schedule in schedules_to_actualize.schedule_ids:
            telegram_cli.telegram.send_message(message=schedule.message)
            schedule.send_date = datetime.now()
            schedule.save()

        res_sr = ScheduleSerializer(schedules_to_actualize.schedule_ids, many=True)
        return Response(res_sr.data)
