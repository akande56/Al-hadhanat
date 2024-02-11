from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy as _
from django.utils.translation import gettext_lazy
from django.views.generic import CreateView

from hadanathighschool.users.models import User

from .forms import TeacherSignUpForm

# Create your views here.


class TeacherSignUpCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = "teacher_signup.html"
    success_message = gettext_lazy("Teacher Signed Up Successfully")
    success_url = _("teachers")
    
def gallery(request):
    return render(request, "gallery.html")
