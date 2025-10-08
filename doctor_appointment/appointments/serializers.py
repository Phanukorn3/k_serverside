from appointments.models import Doctor, Patient, Appointment
from rest_framework import serializers
from django.utils import timezone


class DoctorSerializer(serializers.ModelSerializer):
    # appointment_set = AppointmentSerializer(many=True, read_only=True)
    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "specialization",
            "phone_number",
            "email",
            # "appointment_set"
        ]


class PatientSerializer(serializers.ModelSerializer):
    # appointment_set = AppointmentSerializer(many=True, read_only=True)
    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "phone_number",
            "email",
            "address",
            # "appointment_set"
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    # doctor = DoctorSerializer()
    # patient = PatientSerializer()
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    # doctor = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # patient = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Appointment
        fields = ["id", "doctor", "patient", "date", "at_time", "details"]

    def validate(self, data):
        now = timezone.localtime()

        if data["date"] < now.date():
            raise serializers.ValidationError("The appointment date must be in the future.")
        
        elif data["date"] == now.date() and data["at_time"] < now.time():
            raise serializers.ValidationError("The appointment time must be in the future.")

        return data

        # date = data["date"]
        # at_time = data["at_time"]

        # appointment_datetime = timezone.datetime.combine(date, at_time)
        
        # if appointment_datetime < timezone.now():
        #     raise serializers.ValidationError("The appointment date or time must be in the future.")
        # return data
