from django.db import models

from account.models import Account


class Url(models.Model):
    raw = models.CharField(max_length=250)
    url_hash = models.CharField(max_length=8)
    short = models.CharField(max_length=41)
    created_on = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(Account, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.url_hash + ' | ' + self.created_by.username

    class Meta:
        ordering = ['-created_on']
