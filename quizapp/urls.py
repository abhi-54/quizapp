"""quizapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from quizes.views import userShowResult
from quizes.views import all_links_view

urlpatterns = [
    #url(r'^admin/test/', TemplateView.as_view(template_name='admin/quizAllow.html')),
    path('admin/', admin.site.urls),
    path('question/',include('quizes.urls',namespace='quizes')),
    path('attendance/', include('attendance.urls')),
    path('',include('regester.urls')),
    path('result/',userShowResult),
    path('payment/', include('payment.urls')),
    path('all-links/', all_links_view, name='all-links-page'),
    path('panel/', include('questions.urls')),
    path('api/', include('api.urls'))
    #path('admin/test/', TemplateView.as_view(template_name='/admin/quizAllow.html')),
    
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL )
