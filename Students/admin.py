from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .forms import SessionForm
from .models import (
    LGA,
    Class,
    FormMaster,
    Result,
    Session,
    State,
    Student,
    Subject,
    Tribe,
)

# Register your models here.


class SubjectInline(admin.TabularInline):
    """Tabular Inline View for Student"""

    model = Subject
    min_num = 0
    max_num = 50
    extra = 1
    fields = (
        "title",
        # 'Average',
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin View for Student"""

    list_display = (
        "firstname",
        "surname",
        "lastname",
        "admitted",
        "c_class",
        "registration_number",
        "sex",
        "date_of_birth",
        "guardian_name",
        "phone",
    )
    list_filter = (
        "admitted",
        "c_class",
        )
    inlines = [SubjectInline]
    # readonly_fields = ('',)
    search_fields = ("firstname",)
    # date_hierarchy = ''
    ordering = ("create_date",)
    fieldsets = (
        (
            _("Bio Data"),
            {
                "fields": (
                    "firstname",
                    "surname",
                    "lastname",
                    "date_of_birth",
                    "sex",
                    "nationality",
                    "tribe",
                    "state",
                    "lga",
                    "address",
                    "previous_school",
                )
            },
        ),
        (
            _("Guardian"),
            {
                "fields": (
                    "guardian_name",
                    "phone",
                    "email",
                )
            },
        ),
        (_("Medical"), {"fields": ("physical_disability", "allergy")}),
        (
            _("Admin"),
            {
                "fields": (
                    "admitted",
                    "admitted_date",
                    "roll_number",
                    "registration_number",
                )
            },
        ),
        (
            _("Class"),
            {
                "fields": (
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
                    "c_class",
                    "category",
                )
            },
        ),
    )
    # def save_model(self, request, obj, form, change):
    #     clss = obj.c_class
    #     # check if student already was once a member of a class
    #     # if Class.objects.get(student = obj):

    #     return super().save_model(request, obj, form, change)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    """Admin View for State"""


@admin.register(LGA)
class LGAAdmin(admin.ModelAdmin):
    """Admin View for LGA"""


@admin.register(Tribe)
class TribeAdmin(admin.ModelAdmin):
    """Admin View for Tribe"""


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """Admin View for Session"""
    form = SessionForm
    list_display = [
        'session',
        'active',
        'create_date',
    ]
    


@admin.register(FormMaster)
class FormMasterAdmin(admin.ModelAdmin):
    """Admin View for FormMaster"""


class StudentInline(admin.TabularInline):
    """Tabular Inline View for Student"""

    model = Student
    min_num = 0
    max_num = 50
    extra = 1
    fields = (
        "firstname",
        "surname",
        "roll_number",
        "registration_number",
        "sex",
    )


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    """Admin View for Class"""

    list_display = ["name"]
    list_filter = ["name"]
    inlines = [
        StudentInline,
    ]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin View for Subject"""
    list_display = (
        "title",
        "student"
    )
    list_filter = [
        "r_class"
    ]



@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    """Admin View for Result"""

    list_display = (
        "result_class",
        "result_term",
        "student",
        "overrall_totall",
        "average",
        "position",
    )
    list_filter = (
    "result_class",
    "result_term",
    )
    # readonly_fields = ('',)
    search_fields = ["student"]
    # date_hierarchy = ''
    ordering = (
        "result_class",
        "position",
        "result_term"
    )
