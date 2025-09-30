from django import forms
from .models import *
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms.widgets import *


# class StudentForm(forms.Form):
#     student_id = forms.CharField(max_length=10)
#     first_name = forms.CharField(max_length=100)
#     last_name = forms.CharField(max_length=100)
#     faculty = forms.ModelChoiceField(
#         queryset=Faculty.objects.all(),
#         empty_label="Select an option",widget=forms.RadioSelect,
#         required=False
#     )
#     enrolled_sections = forms.ModelMultipleChoiceField(
#         queryset=Section.objects.all(),widget=forms.Textarea,
#         required=False,
#     )
#     email = forms.EmailField()
#     phone_number = forms.CharField(max_length=10, required=False)
#     address = forms.CharField(max_length=100, required=False)
    
class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ["student_id", "first_name", "last_name", "faculty", "enrolled_sections"]
        widgets = {
            "faculty": forms.RadioSelect(),
        }
        
class StudentProfileForm(ModelForm):
    class Meta:
        model = StudentProfile
        fields = ["email", "phone_number", "address"]
        widgets = {
            "address": forms.Textarea(),
        }
    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        if not email.endswith("@kmitl.ac.th"):
            print(email)
            raise ValidationError(
                    "Error @kmitl.ac.th"
                )
        return  cleaned_data

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'credits']

class SectionForm(ModelForm):
    class Meta:
        model = Section
        # fields = ['section_number', 'semester', 'professor', 'day_of_week', 'start_time', 'end_time', 'capacity']
        fields = "__all__"
        widgets = {
            'start_time' : forms.TimeInput(attrs={'type':'time'}),
            'end_time' : forms.TimeInput(attrs={'type':'time'})
        }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     room = cleaned_data.get("room")
    #     start_time = cleaned_data.get("start_time")
    #     end_time = cleaned_data.get("end_time")

    #     if start_time and end_time and end_time < start_time:
    #         raise ValidationError(
    #                 "End time cannot be before start time"
    #             )
    #     bookings = Booking.objects.filter(
    #         start_time__lte=end_time, 
    #         end_time__gte=start_time, 
    #         room=room
    #     )
    #     if bookings.count() > 0:
    #         raise ValidationError(
    #                 "This room has already been booked for the selected time"
    #             )

    #     return cleaned_data