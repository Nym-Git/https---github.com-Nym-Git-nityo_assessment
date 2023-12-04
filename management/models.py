from django.db import models

class RequestCounter(models.Model):
    count = models.IntegerField(default=0)
    