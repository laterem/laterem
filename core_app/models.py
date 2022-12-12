from django.db import models
from django.contrib.auth.models import AbstractUser

class LateremUser(AbstractUser):
    settings = models.TextField()

class LateremGroup(models.Model):
    name = models.CharField(primary_key=True, unique=True, max_length=128)
    # Global Permissions (temporary)
    can_solve_tasks = models.BooleanField(default=True)
    can_manage_groups = models.BooleanField(default=False)
    can_manage_users = models.BooleanField(default=False)
    can_manage_works = models.BooleanField(default=False)

class LateremGroupMembership(models.Model):
    user = models.ForeignKey(LateremUser, on_delete=models.CASCADE)
    group = models.ForeignKey(LateremGroup, on_delete=models.CASCADE)
    # Local Permissions
    is_group_admin = models.BooleanField(default=False)
    can_manage_group_data = models.BooleanField(default=False)
    can_manage_members = models.BooleanField(default=False)
    can_view_members = models.BooleanField(default=True)
    can_manage_permissions = models.BooleanField(default=False)
    can_add_members = models.BooleanField(default=False)
    can_assign_works = models.BooleanField(default=False)
    can_examine_solutions = models.BooleanField(default=False)
    can_solve_works = models.BooleanField(default=True)



class LateremWork(models.Model):
    name = models.CharField(primary_key=True, unique=True, max_length=128)
    author = models.ForeignKey(LateremUser, on_delete=models.DO_NOTHING)

class LateremTask(models.Model):
    name = models.CharField(max_length=128)
    work = models.ForeignKey(LateremWork, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=128)
    
class LateremAssignment(models.Model):
    teacher = models.ForeignKey(LateremUser, on_delete=models.DO_NOTHING, related_name='assigner')
    user = models.ForeignKey(LateremUser, null=True, on_delete=models.CASCADE, related_name='assigned_to')
    group = models.ForeignKey(LateremGroup, null=True, on_delete=models.CASCADE)
    work = models.ForeignKey(LateremWork, on_delete=models.CASCADE)

class LateremSolution(models.Model):
    user = models.ForeignKey(LateremUser, on_delete=models.CASCADE)
    task = models.ForeignKey(LateremTask, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=2)
    timestamp = models.DateTimeField()
    teacher_comment = models.TextField()


