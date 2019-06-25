from django.db import models
import datetime
# Create your models here.


class Event(models.Model):

    event_id = models.CharField(max_length=100, default="AZKXNEAA")
    name = models.CharField(max_length=50)
    start_date = models.DateField('Date Start', default=datetime.date.today)
    end_date = models.DateField('Date End', default=datetime.date.today)
    event_url = models.URLField()
    img_url = models.URLField()

    def __str__(self):
        return self.name
