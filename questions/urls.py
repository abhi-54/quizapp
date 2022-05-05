from unicodedata import name
from django.urls import path
from .views import *

urlpatterns = [
  path('', custom_admin, name='admin-panel-page'),
  path('add-subject/', add_subject_view, name='add-subject-page'),
]
