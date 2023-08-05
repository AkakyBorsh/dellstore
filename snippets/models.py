from attr import attrs, attrib
from attr.validators import instance_of
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Schedule(models.Model):
    title = models.TextField()
    message = models.TextField()
    sended = models.BooleanField(default=False)
    schedule_date = models.DateTimeField(null=True)
    send_date = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='schedules', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']


@attrs()
class Schedules:
    schedule_ids = attrib(type=list, validator=instance_of(list))
