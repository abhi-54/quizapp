from django.urls import path

from .views import (
    QuizListView,
    quiz_view,
    quiz_data_view,
    save_quiz_view,
    userShowResult,
    )


app_name = 'quizes'

urlpatterns = [ 
    path('',QuizListView.as_view(),name = 'main-view'),
    path('<pk>/',quiz_view,name = 'quiz-view'),
    path('<pk>/data/',quiz_data_view,name = 'quiz_data_view'),
    path('<pk>/save/',save_quiz_view,name = 'save-view'),
    
]
#konti link
