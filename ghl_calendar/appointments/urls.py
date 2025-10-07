from django.urls import path
from .views import AppointmentCreateView, AppointmentListView

urlpatterns = [
    path('api/appointments/', AppointmentCreateView.as_view(), name='create-appointment'),
    path('api/appointments/list/', AppointmentListView.as_view(), name='list-appointments'),
]
