from django.db import models
from django.utils import timezone


class FarmImage(models.Model):
    email = models.EmailField()
    image_name = models.CharField(max_length=256)
    time_created = models.DateTimeField(default=timezone.now, editable=False)
