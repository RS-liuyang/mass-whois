from __future__ import unicode_literals

from django.db import models

# Create your models here.
class qDomain(models.Model):

    ori_id = models.IntegerField()
    name = models.CharField(max_length=512)
    status = models.IntegerField(default=0)