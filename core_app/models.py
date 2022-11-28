from django.db import models
from django.contrib.auth.models import AbstractUser

class LateremUser(AbstractUser):
    is_teacher = models.BooleanField()

class LateremGroup(models.Model):
    name = models.CharField(primary_key=True, unique=True, max_length=80)
    users = models.ManyToManyField(LateremUser, related_name='in_latgroup')
    owners = models.ManyToManyField(LateremUser,related_name='owns_latgroup')

class LateremWork(models.Model):
    name = models.CharField(primary_key=True, unique=True, max_length=80)
    task_names = models.TextField()
    task_types = models.TextField()

class LateremAssignment(models.Model):
    user = models.ForeignKey(LateremUser, null=True, on_delete=models.CASCADE)
    group = models.ForeignKey(LateremGroup, null=True, on_delete=models.CASCADE)
    work = models.ForeignKey(LateremWork, on_delete=models.CASCADE)

class LateremRecord(models.Model):
    user = models.ForeignKey(LateremUser, on_delete=models.CASCADE)
    work = models.ForeignKey(LateremWork, on_delete=models.CASCADE)
    task = models.CharField(max_length=100)
    verdict = models.CharField(max_length=2)


