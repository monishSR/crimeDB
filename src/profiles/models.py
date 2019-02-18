# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User


from django.conf import settings

from django.contrib.auth.models import AbstractUser


# Create your models here.
class profile(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(default='decription default text')

    def __unicode__(self):
        return self.name


class UserType(models.Model):

    class Meta:
        permissions = (('is_lawenforcer', 'change entries'),)
