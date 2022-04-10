from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import widgets

from hadanathighschool.users.models import User

from .models import Teacher, designation, edu


class TeacherSignUpForm(UserCreationForm):
    """FarmerSignUpForm definition."""

    firstname = forms.CharField(max_length=50)
    middlename = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    # photo = forms.ImageField(required=False)
    # date_of_birth = forms.DateField()
    designation = forms.ChoiceField(choices=designation)
    edu_level = forms.ChoiceField(choices=edu)
    course = forms.CharField(max_length=20)
    other_qual = forms.CharField(max_length=50, help_text="separate with comma")
    mobile = forms.CharField(max_length=11)
    # email = forms.EmailField(max_length=255)
    date_of_birth = forms.DateField(
        widget=widgets.NumberInput(attrs={"type": "date", "class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        # fields = "__all__"

    @transaction.atomic
    def save(self, commit=True):
        user = super(TeacherSignUpForm, self).save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        fname = self.cleaned_data["firstname"]
        sname = self.cleaned_data["surname"]
        lname = self.cleaned_data["middlename"]
        # ph = self.cleaned_data["photo"]
        dt = self.cleaned_data["date_of_birth"]
        des = self.cleaned_data["designation"]
        educ = self.cleaned_data["edu_level"]
        cous = self.cleaned_data["course"]
        other = self.cleaned_data["other_qual"]
        mob = self.cleaned_data["mobile"]

        teacher = Teacher.objects.create(
            user=user,
            firstname=fname,
            surname=sname,
            middlename=lname,
            # photo=ph,
            date_of_birth=dt,
            designation=des,
            edu_level=educ,
            course=cous,
            other_qual=other,
            mobile=mob,
        )
        teacher.save()
        return user
