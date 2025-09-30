from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.db.models import Count,Value
from django.db.models.functions import Concat
from .studentform import *
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
        faculties = Faculty.objects.all()
        sections = Section.objects.all()
        form = StudentForm()
        forms = StudentProfileForm()
        return render(request, "create_student.html", {
            "faculties": faculties,
            "sections" : sections,
            'form' : form,
            'forms' : forms
        })
    def post(self, request):
        form = StudentForm(request.POST)
        forms = StudentProfileForm(request.POST)
        if form.is_valid() and forms.is_valid():
            f = form.save()
            profile = forms.save(commit=False)
            profile.student = f
            profile.save()
            print(profile.student)
            return redirect("student-list")
        
        print(forms.errors)
        
        return render(request, "create_student.html", {
            'form' : form,
            'forms' : forms
        })

        # student_id = request.POST.get("student_id")
        # first_name = request.POST.get("first_name")
        # last_name = request.POST.get("last_name")
        # email = request.POST.get("email")
        # phone_number = request.POST.get("phone_number")
        # address = request.POST.get("address")
        # faculty_id = request.POST.get("faculty")
        # section_ids = request.POST.getlist("enrolled_sections")

        # student = Student.objects.create(
        #     student_id=student_id,
        #     first_name=first_name,
        #     last_name=last_name,
        #     faculty_id=faculty_id
        # )

        # StudentProfile.objects.create(
        #     student=student,
        #     email=email,
        #     phone_number=phone_number,
        #     address=address
        # )
        # student.enrolled_sections.add(*section_ids)

    
class StudentEditView(View):
    def get(self, request, id):
        student = Student.objects.get(pk=id)
        profile = StudentProfile.objects.get(pk=id)
        initail_data = {
            'student_id' : student.student_id,
            'first_name' : student.first_name,
            'last_name' : student.last_name,
            'email' : profile.email,
            'phone_number': profile.phone_number,
            'address' : profile.address,
            'faculty' : student.faculty,
            'enrolled_sections': student.enrolled_sections.all(),
        }
        form = StudentForm(initial=initail_data)
        return render(request, "edit_student.html", {"form": form})
    def post(self, request, id):
        student = Student.objects.get(pk=id)
        profile = StudentProfile.objects.get(pk=id)
        form = StudentForm(request.POST)

        if form.is_valid():
            student.student_id = form.cleaned_data["student_id"]
            student.first_name = form.cleaned_data["first_name"]
            student.last_name = form.cleaned_data["last_name"]
            student.faculty = form.cleaned_data["faculty"]
            student.save()

            # update M2M
            student.enrolled_sections.set(form.cleaned_data["enrolled_sections"])

            profile.email = form.cleaned_data["email"]
            profile.phone_number = form.cleaned_data["phone_number"]
            profile.address = form.cleaned_data["address"]
            profile.save()

            return redirect("student-list")

        return render(request, "edit_student.html", {"form": form, "student": student})

class CourseCreateView(View):
    def get(self, request):
        course = CourseForm()
        section = SectionForm()
        return render(request, "create_course.html", {
            'course' : course,
            'section' : section
        })
    # def post(self, request):
    #     course = CourseForm(request.POST)
    #     section = SectionForm(request.POST)
    #     if course.is_valid() and section.is_valid():
    #         f = course.save()
    #         section = forms.save(commit=False)
    #         section.course = f
    #         f.save()
    #         section.save()
    #         print(section.student)
    #         return redirect("course_list")
        
    #     return render(request, "create_course.html", {
    #         'course' : course,
    #         'section' : section
    #     })
    def post(self, request):
        data = request.POST.copy()
        course = CourseForm(data)
        section = SectionForm(data)
        if course.is_valid():
            # f = course.save()
            f = Course.objects.get(id=1)

            data["course"] = f

            section = SectionForm(data)
            if section.is_valid():
                course.save()
                section.save()
                return redirect("course_list")
            
        print(course.errors, section.errors)
        return render(request, "create_course.html", {
            'course' : course,
            'section' : section
        })
    
class CourseEditView(View):
    def get(self, request, id):
        course = Course.objects.get(pk=id)
        section = Section.objects.filter(course=course)
        form = CourseForm(request.POST, instance=(course))
        return render(request, "course_edit.html", {"form": form})