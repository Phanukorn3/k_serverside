from django.urls import path

from . import views

urlpatterns = [
    path("student/", views.StudentView.as_view(), name='student-list'),
    path("professor/", views.ProfessorView.as_view(), name='professor-list'),
    path("course/", views.CourseView.as_view(), name='course_list'),
    path("faculty/", views.FacultyView.as_view(), name='faculty_list'),
    path("course/create/", views.CourseCreateView.as_view(), name='create_course'),
    path("course/edit/<int:id>", views.CourseEditView.as_view(), name='course_edit'),
    path("student/create/", views.StudentCreateView.as_view(), name='student_create'),
    path("student/edit/<int:id>", views.StudentEditView.as_view(), name='student_edit'),
]