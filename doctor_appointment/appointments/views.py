from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from appointments.models import Doctor, Patient, Appointment
from appointments.serializers import PatientSerializer, DoctorSerializer, AppointmentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404

# Create your views here.
class DoctorList(APIView):
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

class PatientList(APIView):
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

class AppointmentList(APIView):
    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # data = JSONParser().parse(request)
        # serializer = AppointmentSerializer(data=data)
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AppointmentDetail(APIView):
    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        Appointment = self.get_object(pk)
        serializer = AppointmentSerializer(Appointment)
        return Response(serializer.data)
    
    def put(self, request, pk):
        Appointment = self.get_object(pk)
        serializer = AppointmentSerializer(Appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        Appointment = self.get_object(pk)
        Appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)