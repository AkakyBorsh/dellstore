from rest_framework import serializers
from snippets.models import Schedule
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']


class ScheduleSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    sended = serializers.ReadOnlyField()
    title = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
    schedule_date = serializers.DateTimeField(required=True)

    class Meta:
        model = Schedule
        fields = ['id', 'title', 'sended', 'schedule_date', 'message', 'created', 'owner', 'send_date']


class CreateScheduleSerializer(ScheduleSerializer):
    class Meta:
        model = Schedule
        fields = ['title', 'sended', 'schedule_date', 'message', 'created', 'owner']


class SchedulesSerializer(serializers.Serializer):
    schedule_ids = serializers.ListField(
        allow_empty=False,
        child=serializers.PrimaryKeyRelatedField(queryset=Schedule.objects.all())
    )
