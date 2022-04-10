from django.contrib import admin

# from .forms import TeacherSignUpForm
from .models import Teacher

# Register your models here.


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Admin View for Teacher"""

    # form = TeacherSignUpForm

    list_display = (
        "user",
        # "photo",
        "designation",
        # 'firstname',
        # 'surname',
        "date_of_birth",
        "edu_level",
        "course",
        "other_qual",
        "mobile",
        # 'email',
        "joining_date",
    )
    list_filter = ("designation", "edu_level")

    # readonly_fields = ('',)
    search_fields = ("firstname",)
    date_hierarchy = "joining_date"
    ordering = ("joining_date",)
