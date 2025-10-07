from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('metrics/', views.appointments_metrics, name='appointments_metrics'),
]
