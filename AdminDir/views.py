# from django.shortcuts import render
# Create your views here.

# from django.db.models.query_utils import subclasses
# from typing import List

from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django_filters import FilterSet

from Students.forms import SessionForm
from Students.models import Class, FormMaster, Result, Session, Student
from Teachers.models import Teacher

from .forms import AdminStudentForm
from .models import QA

# from Students.models import Rating


class AdminSessionCreateView(CreateView):
    model = Session
    form_class = SessionForm
    template_name = "admin_add_session.html"
    success_url = reverse_lazy("dashboard")


class AdminSessionListView(ListView):
    model = Session
    template_name = "admin_session_list.html"
    context_object_name = "sessions"


# for session Class
class AdminAllClassListView(ListView):
    model = Class
    template_name = "admin_all_class.html"
    context_object_name = "classes"
    paginate_by = 10

    def get_queryset(self):
        session_id = self.kwargs.get("session_id")
        queryset = Class.objects.filter(session_id=session_id)
        return queryset


class AdminClassStudentListView(ListView):
    model = Student
    template_name = "admin_session_class_students.html"
    context_object_name = "students"
    paginate_by = 10

    def get_queryset(self):
        class_id = self.kwargs.get("class_id")
        queryset1 = Result.objects.filter(result_class_id=class_id).values_list(
            "student", flat=True
        )
        queryset1 = Student.objects.filter(id__in=queryset1).order_by(
            "registration_number"
        )
        if len(queryset1) == 0:

            queryset = Student.objects.filter(c_class__id=class_id)
        else:
            queryset = queryset1
        return queryset


class AdminStudentUpdateView(SuccessMessageMixin, UpdateView):
    model = Student
    template_name = "update_student.html"
    form_class = AdminStudentForm
    context_object_name = "form"
    success_message = "student profile updated"
    success_url = reverse_lazy("dashboard")


class AdminTeacherListView(ListView):
    model = Teacher
    template_name = "admin_all_teachers.html"
    context_object_name = "teachers"
    paginate_by = 10


# NOrmal ALl class
class AdminClassListView(ListView):
    model = Class
    template_name = "all_class.html"
    context_object_name = "classes"
    paginate_by = 10


class AdminAllstudentListView(ListView):
    model = Student
    template_name = "all_student.html"
    context_object_name = "students"
    paginate_by = 10


class AdminStudentCreateView(SuccessMessageMixin, CreateView):
    model = Student
    template_name = "admin_add_student.html"
    form_class = AdminStudentForm
    success_message = "Student created!"

    def get_success_url(self):
        return reverse_lazy("dashboard")


# filter
class AdminStudentFilter(FilterSet):
    class Meta:
        model = Student
        fields = ["admitted", "sex", "c_class"]


def AdminStudentfilterView(request):
    f = AdminStudentFilter(request.GET, queryset=Student.objects.all())
    return render(request, "all_student.html", {"filter": f})


# end filter


class AdminFormMasterCreateView(SuccessMessageMixin, CreateView):
    model = FormMaster
    template_name = "admin_add_formmaster.html"
    fields = "__all__"
    success_url = reverse_lazy("add_formmaster")
    success_message = "Form Master Added To Class!"


class AdminFormMasterListView(ListView):
    model = FormMaster
    template_name = "admin_formmaster_list.html"
    context_object_name = "formmaster"
    paginate_by = 10


# request information


class QACreateView(SuccessMessageMixin, CreateView):
    model = QA
    fields = "__all__"
    success_message = "Enquiry submitted, you will be contacted soon..."
    success_url = reverse_lazy("home")


class QAListView(ListView):
    model = QA
    template_name = "enquiries.html"
    context_object_name = "enquiries"


# principal rating

# class RatingUpdateView(SuccessMessageMixin,UpdateView):
#     model = Rating
#     template_name = "result_rating.html"
#     success_url = "session_list"
#     success_message = "Student Rating updated!"
