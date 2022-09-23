from django.urls import path
from regester.views import profile_view

from .views import (
    QuizListView,
    chart_view,
    home_view,
    quiz_view,
    quiz_data_view,
    save_quiz_view,
    dashboard_view,
    chart_view,
    SubjectView,
    showSub,
    )

app_name = 'quizes'

urlpatterns = [ 
    path('', home_view, name = 'dashboard-view'),
    # Subjects
    path('subject/', SubjectView, name = 'subject-view'),
    # quiz list of that subject
    path('show/<pk>/', showSub, name = 'subject-quiz-view'),
    path('quizes/<pk>/',quiz_view,name = 'quiz-view'),
    path('quizes/<pk>/data/',quiz_data_view,name = 'quiz_data_view'),
    path('quizes/<pk>/save/',save_quiz_view,name = 'save-view'),

    path('profile/', profile_view, name = 'profile-view'),
    path('chart/',chart_view,name = 'chart-view'),
    path('quizes/',QuizListView.as_view(),name = 'main-view'),
    
    # dashboard 2nd theme:
    path('home/',dashboard_view,name = 'home-view'),
] 

handler404 = 'quizes.views.error404_view'
