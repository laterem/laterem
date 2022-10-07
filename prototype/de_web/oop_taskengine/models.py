from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class task_1(models.Model):
    title  = models.CharField(max_length=255)
    text   = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)