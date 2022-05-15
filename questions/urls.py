from unicodedata import name
from django.urls import path
from .views import *

urlpatterns = [
  path('', custom_admin, name='admin-panel-page'),
  path('add-subject/', add_subject_view, name='add-subject-page'),
  path('add-quiz/', add_quiz_view, name='add-quiz-page'),
  path('add-question/', add_question_view, name='add-question&answer-page'),
  path('add-answer/', add_answer_view, name='add-answer-page'),
]
