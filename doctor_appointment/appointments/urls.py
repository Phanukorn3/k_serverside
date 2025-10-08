from django.urls import path
from appointments.views import DoctorList, PatientList, AppointmentList, AppointmentDetail

urlpatterns = [
    path('doctors/', DoctorList.as_view(), name='doctor-list'),
    path('patients/', PatientList.as_view(), name='patient-list'),
    path('appointment/', AppointmentList.as_view(), name='appointment-list'),
    path('appointment/<int:pk>', AppointmentDetail.as_view(), name='appointment-detail'),
]