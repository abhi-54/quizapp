from django.urls import path, include
from .views import *

# urls related to subjects1 model
urlpatterns_subjects = [
  path('overview/', subjects_api_overview, name='api-subjects-overview'),
  path('all/', list_all_subjects, name='api-all-subjects'),
  path('all/<str:std>/', subjects_of_std, name='api-all-subjects-std'),
  path('<int:id>/', one_subject, name='one-subject'),
  path('create/', create_subject, name='create-subject'),
  path('update/<int:id>/', update_subject, name='update-subject'),
  path('delete/<int:id>/', delete_subject, name='delete-subject'),
]

urlpatterns = [
  path('subjects/', include(urlpatterns_subjects))
]