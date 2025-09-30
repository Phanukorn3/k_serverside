from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.db.models import Count,Value
from django.db.models.functions import Concat
from .studentform import StudentForm
from registration.models import Student, Professor, Course, Faculty, Section, StudentProfile

class StudentView(View):

    def get(self, request):
        search_txt = request.GET.get("search")
        filter_type = request.GET.get("filter")

        print(search_txt)
        print(filter_type)

        filters = {}

        if search_txt == None:
            search_txt = ""

        if filter_type == "name":
            filters["full_name__icontains"] = search_txt
        elif filter_type == "email":
            filters["studentprofile__email__icontains"] = search_txt
        elif filter_type == "faculty":
            filters["faculty__name__icontains"] = search_txt

        student_list = Student.objects.annotate(
            full_name = Concat("first_name", Value(" "), "last_name")
            ).filter(**filters)

        return render(request, "index.html", context={
            "total" : student_list.count(),
            "student_list": student_list,
            "filter" : filter_type,
            "search" : search_txt
        })
    
class ProfessorView(View):

    def get(self, request):
        search_txt = request.GET.get("search")
        filter_type = request.GET.get("filter")

        filters = {}

        if search_txt == None:
            search_txt = ""

        if filter_type == "name":
            filters["full_name__icontains"] = search_txt

        elif filter_type == "faculty":
            filters["faculty__name__icontains"] = search_txt

        professor_list = Professor.objects.annotate(
            full_name = Concat("first_name", Value(" "), "last_name")
            ).filter(**filters)
        return render(request, "professor.html", context={
            "total": professor_list.count(),
            "professor_list":professor_list,
            "search": search_txt,
            "filter": filter_type
        })

class CourseView(View):

    def get(self, request):
        search_txt = request.GET.get("search", '')

        filters = {}

        filters["course_name__icontains"] = search_txt

        course_list = Course.objects.all().filter(**filters)
        return render(request, "course.html", context={
            "total": course_list.count(),
            "course_list":course_list,
            "search": search_txt,
        })

class FacultyView(View):

    def get(self, request):
        search_txt = request.GET.get("search", '')

        filters = {}

        filters["name__icontains"] = search_txt

        faculty_list = Faculty.objects.annotate(
            professor_num = Count("professor", distinct=True),
            student_num = Count("student", distinct=True)
        ).filter(**filters)
        return render(request, "faculty.html", context={
            "total": faculty_list.count(),
            "faculty_list":faculty_list,
            "search": search_txt,
        })
    
class StudentCreateView(View):
    def get(self, request):
        form = StudentForm()
        return render(request, "create_student.html", {"form": form})
    
    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student-list")
        return render(request, "create_student.html", {"form": form})
    
class StudentEditView(View):
    def get(self, request, pk):
        student = Student.objects.get(pk=pk)
        profile = student.studentprofile
        form = StudentForm()
        return render(request, "edit_student.html", {"form": form, "student": student, "profile": profile})