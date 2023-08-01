from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from snippets.models import Snippet, Schedule, ActualSchedule
from snippets.serializers import SnippetSerializer
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer, ScheduleSerializer, ActualScheduleSerializer
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ActualizeSchedule(GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @swagger_auto_schema(request_body=ActualScheduleSerializer)
    def post(self, request, *args, **kwargs):
        req_sr = ActualScheduleSerializer(data=request.data)
        req_sr.is_valid(raise_exception=True)

        schedules_to_actualize = ActualSchedule(**req_sr.validated_data)

        for schedule in schedules_to_actualize.schedule_ids:
            schedule.schedule_date = datetime.now() + timedelta(days=1)
            schedule.save()

        res_sr = ScheduleSerializer(schedules_to_actualize.schedule_ids, many=True)
        return Response(res_sr.data)
