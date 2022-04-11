# import datetime
from django import forms
from django.core.exceptions import ValidationError

# from django.db.models import fields
# from crispy_forms.helper import FormHelper
# from crispy_forms.bootstrap import Tab, TabHolder
# from crispy_forms.layout import (Layout, Field, ButtonHolder, Submit,Row,Column)
from .models import LGA, Class, Rating, Session, Student, Subject

# from django.db import models


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "firstname",
            "surname",
            "lastname",
            "guardian_name",
            "date_of_birth",
            "sex",
            "tribe",
            "state",
            "lga",
            "nationality",
            "address",
            "phone",
            "email",
            "previous_school",
            "physical_disability",
            "allergy",
            "pp",
            "nus1",
            "nus2",
            "nus3",
            "primary1",
            "primary2",
            "primary3",
            "primary4",
            "primary5",
            "jss1",
            "jss2",
            "jss3",
            "ss1",
            "ss2",
            "ss3",
        ]
        widgets = {
            "date_of_birth": forms.TextInput({"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["lga"].queryset = LGA.objects.none()

        if "state" in self.data:
            try:
                state_id = int(self.data.get("state"))
                self.fields["lga"].queryset = LGA.objects.filter(
                    state_id=state_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields["lga"].queryset = self.instance.state.lga_set.order_by("name")


class FormMasterStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "registration_number",
            "firstname",
            "surname",
            "lastname",
            "guardian_name",
            "date_of_birth",
            "sex",
            "tribe",
            "state",
            "lga",
            "nationality",
            "address",
            "phone",
            "email",
            "previous_school",
            "physical_disability",
            "allergy",
            "pp",
            "nus1",
            "nus2",
            "nus3",
            "primary1",
            "primary2",
            "primary3",
            "primary4",
            "primary5",
            "jss1",
            "jss2",
            "jss3",
            "ss1",
            "ss2",
            "ss3",
            "category",
            # "c_class",
        ]
        widgets = {
            "date_of_birth": forms.TextInput({"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["lga"].queryset = LGA.objects.none()

        if "state" in self.data:
            try:
                state_id = int(self.data.get("state"))
                self.fields["lga"].queryset = LGA.objects.filter(
                    state_id=state_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields["lga"].queryset = self.instance.state.lga_set.order_by("name")


classes = [
    "pp",
    "nus1",
    "nus2",
    "nus3",
    "primary1",
    "primary2",
    "primary3",
    "primary4",
    "primary5",
    "jss1",
    "jss2",
    "jss3",
    "ss1",
    "ss2",
    "ss3",
]


class SessionForm(forms.ModelForm):
    """Form definition for administration."""

    class Meta:
        """Meta definition for Sessionform."""

        model = Session
        fields = "__all__"

    def clean_session(self):
        session = self.cleaned_data.get("session")

        # TODO Validation

        if Session.objects.filter(session=session).exists():
            raise ValidationError(
                "So sorry, this session already exist in the database"
            )

        return session

    def save(self, commit=True, *args, **kwargs):
        m = super(SessionForm, self).save(commit=False, *args, **kwargs)
        m.save()
        session = self.cleaned_data.get("session")
        for c in classes:
            Class.objects.create(name="{}({})".format(c, session), session=m)

        # adding students to classes and creating subjects for each class
        all_student = Student.objects.filter(admitted=True)
        for s in all_student:
            if s.pp:
                cl_name = "pp({})".format(session)
                cl = Class.objects.get(name=cl_name)
                s.c_class = cl
                s.save()
            if s.nus1:
                cl_name = "nus1({})".format(session)
                cl = Class.objects.get(name=cl_name)
                s.c_class = cl
                s.save()
            if s.nus2:
                cl_name = "nus2({})".format(session)
                cl = Class.objects.get(name=cl_name)
                s.c_class = cl
                s.save()
            if s.nus3:
                cl_name = "nus3({})".format(session)
                cl = Class.objects.get(name=cl_name)
                s.c_class = cl
                s.save()
            if s.primary1:
                cl_name = "primary1({})".format(session)
                cl = Class.objects.get(name=cl_name)
                s.c_class = cl
                s.save()
            if s.primary2:
                cl_name = "primary2({})".format(session)
                cl = Class.objects.get(name=cl_name)
                s.c_class = cl
                s.save()
            if s.primary3:
                cl_name = "primary3({})".format(session)
                cl = Class.objects.get(name=cl_name)
                s.c_class = cl
                s.save()
            if s.primary4:
                cl_name = "primary4({})".format(session)
                cl = Class.objects.get(name=cl_name)
                s.c_class = cl
                s.save()
            if s.primary5:
                cl_name = "primary5({})".format(session)
                cl = Class.objects.get(name=cl_name)
                s.c_class = cl
                s.save()
            if s.jss1:
                cl_name = "jss1({})".format(session)
                cl = Class.objects.get(name=cl_name)
                s.c_class = cl
                s.save()
            if s.jss2:
                cl_name = "jss2({})".format(session)
                cl = Class.objects.get(name=cl_name)
                s.c_class = cl
                s.save()
            if s.jss3:
                cl_name = "jss3({})".format(session)
                cl = Class.objects.get(name=cl_name)
                s.c_class = cl
                s.save()
            if s.ss1:
                cl_name = "ss1({})".format(session)
                cl = Class.objects.get(name=cl_name)
                s.c_class = cl
                s.save()
            if s.ss2:
                cl_name = "ss2({})".format(session)
                cl = Class.objects.get(name=cl_name)
                s.c_class = cl
                s.save()
            if s.ss3:
                cl_name = "ss3({})".format(session)
                cl = Class.objects.get(name=cl_name)
                s.c_class = cl
                s.save()
        return m


class SubjectsForm(forms.ModelForm):
    """Form definition for StudentToSubjectForm."""

    class Meta:
        """Meta definition for StudentToSubjectsform."""

        model = Subject
        fields = ["title"]


class SubjectTerm1UpdateForm(forms.ModelForm):
    """Form definition for SubjectUpdate."""

    class Meta:
        """Meta definition for SubjectUpdateform."""

        model = Subject
        fields = (
            "test1_term1",
            "test2_term1",
            "assignment1_term1",
            "assignment2_term1",
            "Exam_term1",
        )


class SubjectTerm2UpdateForm(forms.ModelForm):
    """Form definition for SubjectUpdate."""

    class Meta:
        """Meta definition for SubjectUpdateform."""

        model = Subject
        fields = (
            "test1_term2",
            "test2_term2",
            "assignment1_term2",
            "assignment2_term2",
            "Exam_term2",
        )


class SubjectTerm3UpdateForm(forms.ModelForm):
    """Form definition for SubjectUpdate."""

    class Meta:
        """Meta definition for SubjectUpdateform."""

        model = Subject
        fields = (
            "test1_term3",
            "test2_term3",
            "assignment1_term3",
            "assignment2_term3",
            "Exam_term3",
        )


class ResultSessionForm(forms.ModelForm):
    """Form definition for ResultSession."""

    class Meta:
        """Meta definition for ResultSessionform."""

        model = Class
        fields = ["session"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["session"].queryset = Session.objects.all()


term = (
    (1, "term1"),
    (2, "term2"),
    (3, "term3"),
)


class ResultClassForm(forms.ModelForm):
    """Form definition for ResultClass."""

    registration_number = forms.CharField()
    term = forms.ChoiceField(choices=term)

    class Meta:
        """Meta definition for ResultClassform."""

        model = Subject  # subject has class, hence; just filter all similar subject for the class
        fields = ["r_class"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["r_class"].queryset = Class.objects.filter(
            session_id=kwargs["initial"]["pk"]
        )


# Student Ratings


class RatingStudentTermForm(forms.ModelForm):
    """Form definition for RatingStudentTerm1."""

    class Meta:
        """Meta definition for RatingStudentTerm1form."""

        model = Rating
        fields = (
            "attendance",
            "attentiveness_in_class",
            "ralationship_with_others",
            "neatness",
            "physical_participation",
            "class_participation",
            "class_teacher_remark",
            "principal_remark",
        )
