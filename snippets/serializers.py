from rest_framework import serializers
from snippets.models import Snippet, Schedule
from django.contrib.auth.models import User


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    sended = serializers.ReadOnlyField()
    title = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
    schedule_date = serializers.DateTimeField(required=True)

    class Meta:
        model = Schedule
        fields = ['id', 'title', 'sended', 'schedule_date', 'message', 'created', 'owner']


class ActualScheduleSerializer(serializers.Serializer):
    schedule_ids = serializers.ListField(
        allow_empty=False,
        child=serializers.PrimaryKeyRelatedField(queryset=Schedule.objects.all())
    )
