from django.urls import path
from quizes.views import *
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings
from .views import *
from attendance.views import select_class_view

urlpatterns = [
  path('', payment_dashboard_view, name='payment-dashboard-page'),
  path('users/', paymentTemp, name='show-users-all'),
  path('quizAllow/', quizAllow, name='quiz-allow'),
  #path('submitted/', afterSubmit, name='submitted'),
  path('class/', select_class_view, name='select-class-payment'),
]