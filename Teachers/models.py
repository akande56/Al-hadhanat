from django.db import models

from hadanathighschool.users.models import User

designation = (("Mr", "Mr"), ("Mrs", "Mrs"))
edu = (
    ("Btech", "Bachelor of technology"),
    ("Bsc", "Bachelor of science"),
    ("Phd", "Phd"),
    ("Dr", "Doctor"),
)
# Create your models here.


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50, blank=True, null=True)
    # photo = models.ImageField(upload_to="teachers", default=None, blank=True, null=True)
    date_of_birth = models.DateField()
    designation = models.CharField(max_length=5, choices=designation)
    edu_level = models.CharField(max_length=20, choices=edu, blank=True)
    course = models.CharField(max_length=20)
    other_qual = models.CharField(max_length=50, help_text="separate with comma")
    mobile = models.CharField(max_length=11, blank=True, null=True)
    joining_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ["joining_date", "firstname"]
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def __str__(self):
        return "{} ({})".format(self.designation, self.firstname)
