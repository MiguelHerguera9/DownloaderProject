from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process-urls/', views.process_urls, name='process_urls'),
]