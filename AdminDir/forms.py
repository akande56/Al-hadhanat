from django import forms

from Students.models import (
    LGA, 
    Student, 
    Session, 
    Class, 
    Subject,
    Teacher
)


class AdminStudentForm(forms.ModelForm):
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
            "admitted",
            "c_class",
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


class AdminLessonNoteFilterForm(forms.Form):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), required=False)
    class_level = forms.ModelChoiceField(queryset=Class.objects.all(), required=False)
    session = forms.ModelChoiceField(queryset=Session.objects.all(), required=False)
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), required=False)