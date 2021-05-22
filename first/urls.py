from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='first-home'),
    path('about/', views.about, name='first-about')
]
