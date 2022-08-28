from django.urls import path, re_path
from quizes.views import *
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings


urlpatterns = [
    # path('',reges,name="reges"),
    path('reges/',reges,name='reges'),
    path('', landing_page, name='landing-view'),
    path('index/', landing_page, name='landing-view'),
    path('about/', about_page, name='about-page-view'),
    path('contact/', contact_page, name='contact-page-view'),
    path('login/',Login,name='Login'),
    path('question/', home_view, name = 'dashboard-view'),
    path('set_password/<int:id>', pass_set_view, name='set-password-page'),
    path('set_password/done/', done_setting_pass, name='done-set-password-page'),
    re_path(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]