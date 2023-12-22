from django.urls import path, include
from .views import *
from attendance.views import select_class_view

urls_add = [
  path('add-subject/', add_subject_view, name='add-subject-page'),
  path('add-quiz/', add_quiz_view, name='add-quiz-page'),
  path('add-question/', add_question_view, name='add-question&answer-page'),
  path('add-answer/', add_answer_view, name='add-answer-page'),
]

urls_view = [
  path('view-subjects/', display_subjects_view, name='view-subjects-page'),
  path('view-subjects/modify/', modify_subject_view, name='modify-subject-page'),
  path('view-quizes/', display_quizes_view, name='view-quizes-page'),
  path('view-quizes/modify/', modify_quiz_view, name='modify-quiz-page'),
  path('view-questions/', display_questions_view, name='view-questions-page'),
  path('view-questions/all/', display_Allquestions_view, name='view-Allquestions-page'),
  path('view-questions/modify/', modify_question_view, name='modify-question-page'),
]

urls_student_overview = [
  path('', students_view, name='students-page'),
  path('class/', select_class_view, name='students-class-page'),
  path('class/select-student/', select_student_view, name='select-student-page'),
  path('class/select-student/<int:id>', show_student_info_view, name='student-info-page'),
]

urlpatterns = [
  path('', custom_admin, name='admin-panel-page'),
  path('', include(urls_add)),
  path('', include(urls_view)),
  path('student/', include(urls_student_overview)),
  path('api-subject/', api_subjects, name='api-subject')
]
