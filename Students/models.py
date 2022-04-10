from django.db import models

from Teachers.models import Teacher


class Session(models.Model):
    """Model definition for Session."""

    session = models.CharField(max_length=30)
    create_date = models.DateField(auto_now=True)

    class Meta:
        """Meta definition for Session."""

        verbose_name = "Session"
        verbose_name_plural = "Sessions"

    def __str__(self):
        """Unicode representation of Session."""
        return str(self.session)


class Class(models.Model):
    """Model definition for Class."""

    name = models.CharField(max_length=50, help_text="class title")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    # subjects = models.ManyToManyField(Subject, related_name='class_subjects',through="StudentToSubjects")
    create_date = models.DateField(auto_now=True)

    class Meta:
        """Meta definition for Class."""

        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def __str__(self):
        """Unicode representation of Class."""
        return str(self.name)


class FormMaster(models.Model):
    """Model definition for FromMaster."""

    Teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    f_class = models.OneToOneField(Class, on_delete=models.SET_NULL, null=True)
    # TODO: Define fields here

    class Meta:
        """Meta definition for FromMaster."""

        verbose_name = "FromMaster"
        verbose_name_plural = "FromMasters"

    def __str__(self):
        """Unicode representation of FromMaster."""
        return str(self.Teacher.firstname)


sex = (("m", "male"), ("f", "female"))
grad = (("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"), ("E", "E"), ("F", "F"))


class Tribe(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Tribe"
        verbose_name_plural = "Tribes"


class State(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"


class LGA(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "LGA"
        verbose_name_plural = "LGA's"


class Student(models.Model):
    """Model definition for Student."""

    # Personal Data
    # photo = models.ImageField(upload_to="students", default=None, null=True)
    firstname = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50, blank=True)
    guardian_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=50, choices=sex)
    tribe = models.ForeignKey(Tribe, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    lga = models.ForeignKey(LGA, on_delete=models.SET_NULL, null=True)
    nationality = models.CharField(max_length=50)
    address = models.CharField(max_length=120)
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=50, null=True)
    previous_school = models.CharField(
        max_length=50, blank=True, null=True, help_text="previous school"
    )

    # Medical Data
    physical_disability = models.CharField(max_length=50, blank=True, null=True)
    allergy = models.CharField(max_length=50, blank=True, null=True)
    # checkbox

    # admin
    admitted = models.BooleanField(blank=True, default=False)
    admitted_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    roll_number = models.CharField(max_length=6, unique=True, blank=True, null=True)
    registration_number = models.CharField(
        max_length=6, unique=True, blank=True, null=True
    )
    create_date = models.DateField(auto_now_add=True)

    # class bool
    pp = models.BooleanField(blank=True, default=False)
    nus1 = models.BooleanField(blank=True, default=False)
    nus2 = models.BooleanField(blank=True, default=False)
    nus3 = models.BooleanField(blank=True, default=False)

    primary1 = models.BooleanField(blank=True, default=False)
    primary2 = models.BooleanField(blank=True, default=False)
    primary3 = models.BooleanField(blank=True, default=False)
    primary4 = models.BooleanField(blank=True, default=False)
    primary5 = models.BooleanField(blank=True, default=False)

    jss1 = models.BooleanField(blank=True, default=False)
    jss2 = models.BooleanField(blank=True, default=False)
    jss3 = models.BooleanField(blank=True, default=False)

    ss1 = models.BooleanField(blank=True, default=False)
    ss2 = models.BooleanField(blank=True, default=False)
    ss3 = models.BooleanField(blank=True, default=False)

    # Academics
    c_class = models.ForeignKey(
        Class, on_delete=models.SET_NULL, related_name="student_class", null=True
    )

    class Meta:
        """Meta definition for Student."""

        verbose_name = "Student"
        verbose_name_plural = "Students"
        # ordering = ['roll', 'registration_number']

    def __str__(self):
        """Unicode representation of Student."""
        return str("{} {} {}".format(self.surname, self.firstname, self.lastname))


class Subject(models.Model):
    """Model definition for Subject."""

    # first Term
    title = models.CharField(max_length=50)
    real_title = models.CharField(max_length=50, blank=True)
    test1_term1 = models.PositiveIntegerField(blank=True, default="0")
    test2_term1 = models.PositiveIntegerField(blank=True, default="0")
    assignment1_term1 = models.PositiveIntegerField(blank=True, default="0")
    assignment2_term1 = models.PositiveIntegerField(blank=True, default="0")
    Exam_term1 = models.PositiveIntegerField(blank=True, default="0")
    total_term1 = models.PositiveIntegerField(blank=True, default="0")
    grade_term1 = models.CharField(max_length=2, blank=True, choices=grad)

    # second Term
    test1_term2 = models.PositiveIntegerField(blank=True, default="0")
    test2_term2 = models.PositiveIntegerField(blank=True, default="0")
    assignment1_term2 = models.PositiveIntegerField(blank=True, default="0")
    assignment2_term2 = models.PositiveIntegerField(blank=True, default="0")
    Exam_term2 = models.PositiveIntegerField(blank=True, default="0")
    total_term2 = models.PositiveIntegerField(blank=True, default="0")
    grade_term2 = models.CharField(max_length=2, blank=True, choices=grad)

    # third Term
    test1_term3 = models.PositiveIntegerField(blank=True, default="0")
    test2_term3 = models.PositiveIntegerField(blank=True, default="0")
    assignment1_term3 = models.PositiveIntegerField(blank=True, default="0")
    assignment2_term3 = models.PositiveIntegerField(blank=True, default="0")
    Exam_term3 = models.PositiveIntegerField(blank=True, default="0")
    total_term3 = models.PositiveIntegerField(blank=True, default="0")
    grade_term3 = models.CharField(max_length=2, blank=True, choices=grad)
    # Average = models.FloatField(blank=True,default='0')
    r_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        """Meta definition for Subject."""

        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        """Unicode representation of Subject."""
        return str(self.title)


term = (
    (1, "term1"),
    (2, "term2"),
    (3, "term3"),
)


class Result(models.Model):
    """Model definition for Total."""

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="student_result"
    )
    result_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="result_class"
    )
    overrall_totall = models.PositiveIntegerField()
    position = models.PositiveIntegerField(blank=True, default=0)
    result_term = models.CharField(choices=term, max_length=10)
    average = models.FloatField(null=True, max_length=2)
    totall_student = models.IntegerField(default=0)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Result."""

        verbose_name = "Result"
        verbose_name_plural = "Results"

    def __str__(self):
        """Unicode representation of Total."""
        return str(self.student.firstname)


rating = (("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"), ("E", "E"))


class Rating(models.Model):
    """Model definition for Rating."""

    # TODO: Define fields here
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="student_rating"
    )
    r_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="student_class_rating"
    )
    attendance = models.CharField(max_length=1, choices=rating)
    attentiveness_in_class = models.CharField(max_length=1, choices=rating)
    ralationship_with_others = models.CharField(
        max_length=10, choices=rating, default="B"
    )
    neatness = models.CharField(max_length=1, choices=rating)
    physical_participation = models.CharField(
        max_length=10, choices=rating, default="B"
    )
    class_participation = models.CharField(max_length=1, choices=rating)
    term = models.CharField(max_length=10, choices=term)
    class_teacher_remark = models.CharField(max_length=50, blank=True, default="NONE")
    principal_remark = models.CharField(max_length=50, blank=True, default="NONE")

    class Meta:
        """Meta definition for Rating."""

        verbose_name = "Rating"
        verbose_name_plural = "Ratings"

    def __str__(self):
        """Unicode representation of Rating."""
        return str(self.student.firstname)
