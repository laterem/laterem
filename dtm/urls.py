from django.urls import path
from question import *

from prototype.de_web.de_web.urls import *

urlpatterns.append([
    path('my_task/', task_render),
])
print('#######################################################')