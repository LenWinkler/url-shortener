from django.db import models

class Url(models.Model):
    raw = models.CharField(max_length=250)
    url_hash = models.CharField(max_length=8)