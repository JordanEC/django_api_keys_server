# coding=utf-8
from __future__ import unicode_literals
import hashlib
from django.db import models


class APIKey(models.Model):
    mail = models.EmailField(unique=True)
    api_key = models.CharField(max_length=150, editable=False, blank=True, null=True)
    requests = models.IntegerField(default=0, editable=False)

    def save(self, *args, **kwargs):
        h = hashlib.new('md5')
        h.update(self.mail)
        self.api_key = h.hexdigest()
        super(APIKey, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.mail

