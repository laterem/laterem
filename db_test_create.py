from django.db import models
from core_app.models import *

admin = LateremUser.objects.get(username='ADMIN@ADMIN.ADMIN')

catcat1 = LateremCategoryCategory.objects.create(name='Физика')

workcat1 = LateremWorkCategory.objects.create(name='Задания',
                                              root_category=catcat1)

work1 = LateremWork.objects.create(name='Work',
                                   author=admin,
                                   category=workcat1)

task1 = LateremTask.objects.create(name='Первое',
                                   work=work1,
                                   task_type='task2')
task2 = LateremTask.objects.create(name='Второе',
                                   work=work1,
                                   task_type='task2')

asg1 = LateremAssignment.objects.create(teacher=admin,
                                        user=admin,
                                        work=work1)

catcat1.save()
workcat1.save()
work1.save()
task1.save()
task2.save()
asg1.save()