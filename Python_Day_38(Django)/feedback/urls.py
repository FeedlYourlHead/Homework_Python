from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('feedback/', views.feedback_form, name='feedback_form'),
    path('all-feedback/', views.all_feedback, name='all_feedback')
]

