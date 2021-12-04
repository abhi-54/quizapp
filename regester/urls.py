from django.urls import path
from quizes.views import *
from .views import *
urlpatterns = [
    # path('',reges,name="reges"),
    path('reges/',reges,name="reges"),
    path('',Login,name="Login"),
    path('question',QuizListView.as_view(),name = 'main-view')
]