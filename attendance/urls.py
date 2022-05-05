from django.urls import path
from quizes.views import *
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings
from .views import *

urlpatterns = [
  path('class/', select_class_view, name='select-class-page'),
  path('class/subject/', select_subject_view, name='select-subject-page'),
  path('class/subject/user/', mark_attendance_view, name='mark-attendance-page'),
  path('class/subject/user/marked/', attendace_marked_view, name='attendance-marked-page'),
]