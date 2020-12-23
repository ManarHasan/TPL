from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('parent-profile', views.parent_profile),
    path('teacher-profile', views.teacher_profile),
    path('details', views.details),
    path('home', views.home)
]
