import io
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError, PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy as _
from django.urls.base import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.views.generic.edit import FormView
# from django_xhtml2pdf.utils import generate_pdf
from PyPDF2 import PdfFileMerger
from bootstrap_modal_forms.generic import BSModalUpdateView
from Teachers.models import Teacher
from .decorators import teacher_required
from .forms import (
    FormMasterStudentForm,
    RatingStudentTermForm,
    ResultClassForm,
    ResultSessionForm,
    StudentForm,
    SubjectsForm,
    SubjectTerm1UpdateBSModalForm,
    SubjectTerm2UpdateBSModalForm,
    SubjectTerm3UpdateBSModalForm,
    LessonNoteForm,
    LessonNoteFilterForm,
    SimpleStudentForm,
)

from .models import (
    LGA, 
    Class, 
    FormMaster, 
    Rating, 
    Result, 
    Session, 
    Student, 
    Subject,
    LessonNote,
    Tribe,
    State,
)
# from io import BytesIO
# from typing import KeysView


# from xhtml2pdf import pisa


# from django.http.request import HttpRequest


def StudentCreateView(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.INFO, gettext_lazy("Form submitted!")
            )
            return redirect("studentform", pk=form.instance.pk)
    else:
        form = StudentForm()
    return render(request, "add_student.html", {"form": form})


def simple_add_student(request):
    if request.method == 'POST':
        form = SimpleStudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.guardian_name = 'nill'
            student.tribe = Tribe.objects.first()
            student.state = State.objects.first()
            student.lga =  LGA.objects.first()
            student.nationality = 'Nigeria'
            student.address = 'nill'
            student.email = 'nill@gmail.com'
            student.previous_school = 'nill'
            student.physical_disability = 'none'
            student.allergy = 'none'
            student.registration_number = form.cleaned_data.get('roll_number')
            
            # Set values for fields not in the form
            student.admitted = True
            
            student.save()
            return redirect('home') 
    form = SimpleStudentForm()

    return render(request, 'simple_add_student.html', {'form': form})


class StudentDetailView(DetailView):
    model = Student
    template_name = "student_detail.html"
    context_object_name = "student"


class StudentUpdateView(SuccessMessageMixin, UpdateView):
    model = Student
    template_name = "update_student.html"
    form_class = FormMasterStudentForm
    context_object_name = "form"
    success_message = "student profile updated"

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        stu = Student.objects.get(pk=pk)
        return reverse_lazy("formmaster_students", kwargs={"pk": stu.c_class.pk})


@login_required
@teacher_required
def student_delete_view(request, pk, cl):
    student = Student.objects.get(pk=pk)
    student.delete()
    messages.add_message(request, messages.INFO, gettext_lazy("Student Deleted!"))
    return redirect("formmaster_students", pk=cl)


def load_lga(request):
    state_id = request.GET.get("state")
    lgas = LGA.objects.filter(state_id=state_id).order_by("name")
    return render(request, "lga_dropdown_list_options.html", {"lgas": lgas})


@method_decorator([login_required, teacher_required], name="dispatch")
class FormmasterClassListView(ListView):
    model = Class
    template_name = "formmaster_class.html"
    context_object_name = "class"

    def get_queryset(self):
        # teacher = Teacher.objects.get(user=self.request.user)
        # queryset = FormMaster.objects.filter(Teacher=teacher)
        current_session = Session.objects.get(active=True)
        classes = Class.objects.filter(session=current_session).order_by('name')
        queryset = classes
        return queryset


@method_decorator([login_required, teacher_required], name="dispatch")
class FommasterStudentListView(ListView):
    model = Student
    template_name = "formmaster_student.html"
    context_object_name = "students"
    paginate_by = 10

    def get_queryset(self):
        pk = self.kwargs.get("pk")  # class primary key
        cl = Class.objects.get(pk=pk)
        queryset = Student.objects.filter(c_class=cl).order_by("firstname")
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(FommasterStudentListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get("pk")  # class primary key
        cl = Class.objects.get(pk=pk)
        classname = cl.name
        context["classname"] = classname
        return context


@method_decorator([login_required, teacher_required], name="dispatch")
class StudentToSubjectsCreateView(SuccessMessageMixin, CreateView):
    model = Subject
    form_class = SubjectsForm
    template_name = "formmaster_student_subject.html"
    success_message = gettext_lazy("New subject added!")
    success_url = _("formmaster_class")

    def form_valid(self, form):
        subjt_name = form.instance.title
        real_t = subjt_name
        form.instance.real_title = real_t  # actual subject title

        clss_id = self.kwargs.get("pk")
        clss = Class.objects.get(id=clss_id)

        # checking if subject already exist for the class
        clss_name = clss.name
        subjt_name = "{}_{}".format(
            subjt_name, clss_name
        )  # changing title, for easy database verification
        test = Subject.objects.filter(title=subjt_name, r_class=clss)
        print(test)
        if len(test) != 0:
            print("here")
            return render(
                self.request, template_name="subject_already_exist_class.html"
            )
        else:
            form.instance.title = subjt_name
            form.instance.r_class = clss  # needed the actual class for checking

        # creating subject for all student in the class
        all_stu = Student.objects.filter(c_class=clss)
        for student in all_stu:
            Subject.objects.create(
                title=subjt_name, r_class=clss, student=student, real_title=real_t
            )

        return super().form_valid(form)


@login_required
@teacher_required
def student_single_addSubject(request, pk):
    stu_id = pk
    stu = Student.objects.get(pk=stu_id)
    stu_clss = stu.c_class

    # get all previously created subjects
    all_subj = Subject.objects.filter(student=None, r_class=stu_clss.id)

    for sub in all_subj:
        title = sub.title
        real_title = sub.real_title

        try:
            Subject.objects.get(student=stu, title=title, r_class=stu_clss)
        except Subject.DoesNotExist:
            Subject.objects.create(
                student=stu, title=title, real_title=real_title, r_class=stu_clss
            )

    return redirect("formmaster_students", pk=stu_clss.pk)


class FormmasterAllSubjectsListView(ListView):
    model = Subject
    template_name = "formmaster_all_subjects.html"
    context_object_name = "subjects"
    paginate_by = 10

    def get_queryset(self):
        class_pk = self.kwargs.get("class_pk")
        queryset = Subject.objects.filter(r_class_id=class_pk, student=None).order_by(
            "title"
        )
        return queryset




@login_required
@teacher_required
def DeleteSubject(request, subjt_id):
    subj = Subject.objects.get(id=subjt_id)
    subj_title = subj.title
    # subj_rtitle = subj.real_title
    class_id = subj.r_class.pk
    all_subj_instance = Subject.objects.filter(title=subj_title)
    all_subj_instance.delete()
    messages.add_message(
        request,
        messages.INFO,
        gettext_lazy("Subject {} Deleted for all Student!".format(subj_title)),
    )
    return redirect("formmaster_students", pk=class_id)


class FormmastStudentCreateView(SuccessMessageMixin, CreateView):
    model = Student
    template_name = "formmaster_add_student.html"
    form_class = FormMasterStudentForm
    success_message = "New Student added to class"
    def form_valid(self, form):
        clss_id = self.kwargs.get("pk")
        clss = Class.objects.get(id=clss_id)
        form.instance.c_class = clss
        form.instance.admitted = True
        return super().form_valid(form)
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    def get_success_url(self):
        return _("formmaster_students", kwargs={"pk": self.kwargs.get("pk")})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs.get("pk")
        return context


# Term 1
@method_decorator([login_required, teacher_required], name="dispatch")
class StudentSubjectTerm1ListView(ListView):
    model = Subject
    template_name = "student_term1_record.html"
    context_object_name = "subjects"
    paginate_by = 10

    def get_queryset(self):
        pk = self.kwargs.get("pk")  # student primary key
        stu = Student.objects.get(pk=pk)
        stu_clss = stu.c_class
        queryset = Subject.objects.filter(student=stu, r_class=stu_clss).order_by(
            "real_title"
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StudentSubjectTerm1ListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get("pk")  # student primary key
        stu = Student.objects.get(pk=pk)
        name = "{} {} {}".format(stu.surname, stu.firstname, stu.lastname)
        context["name"] = name
        context["back_key"] = int(stu.c_class.id)  # redirection to formmaster class
        return context


@method_decorator([login_required, teacher_required], name="dispatch")
class StudentRatingTerm1CreateView(SuccessMessageMixin, CreateView):
    model = Rating
    form_class = RatingStudentTermForm
    template_name = "student_term1_rating.html"
    success_message = "Rating submitted"

    def form_valid(self, form):
        term = self.kwargs["term"]
        stu_id = self.kwargs["stu_id"]
        clss_id = self.kwargs["clss_id"]

        student = Student.objects.get(id=stu_id)
        r_class = Class.objects.get(id=clss_id)
        if Rating.objects.filter(student=student, r_class=r_class, term=1):
            return ValidationError("Rating already existed for student, edit instead!")
        else:
            pass

        user = self.request.user
        teacher = Teacher.objects.get(user=user)
        clss = Class.objects.get(id=clss_id)
        try:
            FormMaster.objects.get(Teacher=teacher, f_class=clss)
        except ObjectDoesNotExist:
            raise PermissionDenied
        else:
            pass

        form.instance.student = student
        form.instance.r_class = r_class
        form.instance.term = term
        return super().form_valid(form)

    def get_success_url(self):
        return _("student_subjects_term1", kwargs={"pk": self.kwargs["stu_id"]})


@method_decorator([login_required, teacher_required], name="dispatch")
class StudentRatingTerm1UpdateView(SuccessMessageMixin, UpdateView):
    model = Rating
    form_class = RatingStudentTermForm
    template_name = "student_term1_update.html"
    success_message = "Rating Updated!"

    def get_success_url(self):
        rating_id = self.kwargs["pk"]
        student = Rating.objects.get(pk=rating_id).student.id
        return _("student_subjects_term1", kwargs={"pk": student})


@method_decorator([login_required, teacher_required], name="dispatch")
class StudentRatingTerm1ListView(ListView):
    model = Rating
    template_name = "student_term1_update.html"
    context_object_name = "ratings"

    def get_queryset(self):
        queryset = super(StudentRatingTerm1ListView, self).get_queryset()
        term = self.kwargs["term"]
        stu_id = self.kwargs["stu_id"]
        clss_id = self.kwargs["clss_id"]

        student = Student.objects.get(id=stu_id)
        r_class = Class.objects.get(id=clss_id)
        queryset = Rating.objects.filter(student=student, r_class=r_class, term=term)
        return queryset

'''
@login_required
@teacher_required
def studentSubjectTerm1Record(request, pk):
    context = {}
    obj = get_object_or_404(Subject, pk=pk)
    stu_id = obj.student.id
    form = SubjectTerm1UpdateForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save(commit=False)
        total = (
            form.instance.test1_term1
            + form.instance.test2_term1
            + form.instance.assignment1_term1
            + form.instance.assignment2_term1
            + form.instance.Exam_term1
        )
        form.instance.total_term1 = total
        if total >= 70 and total <= 100:
            form.instance.grade_term1 = "A"
        elif total >= 60 and total <= 70:
            form.instance.grade_term1 = "B"
        elif total >= 50 and total <= 59:
            form.instance.grade_term1 = "C"
        elif total >= 40 and total <= 49:
            form.instance.grade_term1 = "D"
        else:
            form.instance.grade_term1 = "E"

        form.save()
        return redirect("student_subjects_term1", pk=stu_id)
    context["form"] = form
    context["real_title"] = obj.real_title
    context["name"] = "{} {} {}".format(
        obj.student.surname, obj.student.firstname, obj.student.lastname
    )
    return render(request, "student_term1_record.html", context)
'''

@method_decorator([login_required, teacher_required], name="dispatch")
class Term1SubjectBSModalUpdateView(BSModalUpdateView):
    model = Subject
    form_class = SubjectTerm1UpdateBSModalForm
    template_name = 'partialTerm1SubjectUpdate.html'
    success_message = gettext_lazy('Subject score updated')

    def form_valid(self, form):
        total = (
            form.instance.test1_term1
            + form.instance.test2_term1
            + form.instance.assignment1_term1
            + form.instance.assignment2_term1
            + form.instance.Exam_term1
        )
        form.instance.total_term1 = total
        if total >= 70 and total <= 100:
            form.instance.grade_term1 = "A"
        elif total >= 60 and total <= 70:
            form.instance.grade_term1 = "B"
        elif total >= 50 and total <= 59:
            form.instance.grade_term1 = "C"
        elif total >= 40 and total <= 49:
            form.instance.grade_term1 = "D"
        else:
            form.instance.grade_term1 = "E"
        return super().form_valid(form)
    
    
    def get_context_data(self, **kwargs):
        context = super(Term1SubjectBSModalUpdateView, self).get_context_data(**kwargs)
        context['real_title'] = self.object.real_title
        context["name"] = "{} {} {}".format(
        self.object.student.surname, 
        self.object.student.firstname, 
        self.object.student.lastname)
        return context
    
    def get_success_url(self):
        stu_id = self.object.student.id
        return reverse_lazy("student_subjects_term1", kwargs={'pk':stu_id})
    

# Tearm 2


@method_decorator([login_required, teacher_required], name="dispatch")
class StudentSubjectTerm2ListView(ListView):
    model = Subject
    template_name = "student_term2_record.html"
    context_object_name = "subjects"
    paginate_by = 10

    def get_queryset(self):
        pk = self.kwargs.get("pk")  # student primary key
        stu = Student.objects.get(pk=pk)
        stu_clss = stu.c_class
        queryset = Subject.objects.filter(student=stu, r_class=stu_clss).order_by(
            "real_title"
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StudentSubjectTerm2ListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get("pk")  # student primary key
        stu = Student.objects.get(pk=pk)
        name = "{} {} {}".format(stu.surname, stu.firstname, stu.lastname)
        context["name"] = name
        context["back_key"] = int(stu.c_class.id)
        return context


@method_decorator([login_required, teacher_required], name="dispatch")
class StudentRatingTerm2CreateView(SuccessMessageMixin, CreateView):
    model = Rating
    form_class = RatingStudentTermForm
    template_name = "student_term2_rating.html"
    success_message = "Rating submitted"

    def form_valid(self, form):
        term = self.kwargs["term"]
        stu_id = self.kwargs["stu_id"]
        clss_id = self.kwargs["clss_id"]

        student = Student.objects.get(id=stu_id)
        r_class = Class.objects.get(id=clss_id)
        if Rating.objects.filter(student=student, r_class=r_class, term=2):
            return ValidationError("Rating already existed for student, edit instead!")
        else:
            pass
        
        user = self.request.user
        teacher = Teacher.objects.get(user=user)
        clss = Class.objects.get(id=clss_id)
        try:
            FormMaster.objects.get(Teacher=teacher, f_class=clss)
        except ObjectDoesNotExist:
            raise PermissionDenied
        else:
            pass

        form.instance.student = student
        form.instance.r_class = r_class
        form.instance.term = term
        return super().form_valid(form)

    def get_success_url(self):
        return _("student_subjects_term1", kwargs={"pk": self.kwargs["stu_id"]})


@method_decorator([login_required, teacher_required], name="dispatch")
class StudentRatingTerm2UpdateView(SuccessMessageMixin, UpdateView):
    model = Rating
    form_class = RatingStudentTermForm
    template_name = "student_term2_update.html"
    success_message = "Rating Updated!"

    def get_success_url(self):
        rating_id = self.kwargs["pk"]
        student = Rating.objects.get(pk=rating_id).student.id
        return _("student_subjects_term2", kwargs={"pk": student})


@method_decorator([login_required, teacher_required], name="dispatch")
class StudentRatingTerm2ListView(ListView):
    model = Rating
    template_name = "student_term2_update.html"
    context_object_name = "ratings"

    def get_queryset(self):
        queryset = super(StudentRatingTerm2ListView, self).get_queryset()
        term = self.kwargs["term"]
        stu_id = self.kwargs["stu_id"]
        clss_id = self.kwargs["clss_id"]

        student = Student.objects.get(id=stu_id)
        r_class = Class.objects.get(id=clss_id)
        queryset = Rating.objects.filter(student=student, r_class=r_class, term=term)
        return queryset

'''
@login_required
@teacher_required
def studentSubjectTerm2Record(request, pk):
    context = {}

    obj = get_object_or_404(Subject, pk=pk)
    stu_id = obj.student.id
    form = SubjectTerm2UpdateForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save(commit=False)
        total = (
            form.instance.test1_term2
            + form.instance.test2_term2
            + form.instance.assignment1_term2
            + form.instance.assignment2_term2
            + form.instance.Exam_term2
        )
        form.instance.total_term2 = total
        if total >= 70 and total <= 100:
            form.instance.grade_term2 = "A"
        elif total >= 60 and total <= 70:
            form.instance.grade_term2 = "B"
        elif total >= 50 and total <= 59:
            form.instance.grade_term2 = "C"
        elif total >= 40 and total <= 49:
            form.instance.grade_term2 = "D"
        else:
            form.instance.grade_term2 = "E"
        form.save()
        return redirect("student_subjects_term2", pk=stu_id)
    context["form"] = form
    context["real_title"] = obj.real_title
    context["name"] = "{} {} {}".format(
        obj.student.surname, obj.student.firstname, obj.student.lastname
    )
    return render(request, "student_term2_record.html", context)
'''


@method_decorator([login_required, teacher_required], name="dispatch")
class Term2SubjectBSModalUpdateView(BSModalUpdateView):
    model = Subject
    form_class = SubjectTerm2UpdateBSModalForm
    template_name = 'partialTerm2SubjectUpdate.html'
    success_message = gettext_lazy('Subject score updated')

    def form_valid(self, form):
        total = (
            form.instance.test1_term2
            + form.instance.test2_term2
            + form.instance.assignment1_term2
            + form.instance.assignment2_term2
            + form.instance.Exam_term2
        )
        form.instance.total_term2 = total
        if total >= 70 and total <= 100:
            form.instance.grade_term2 = "A"
        elif total >= 60 and total <= 70:
            form.instance.grade_term2 = "B"
        elif total >= 50 and total <= 59:
            form.instance.grade_term2 = "C"
        elif total >= 40 and total <= 49:
            form.instance.grade_term2 = "D"
        else:
            form.instance.grade_term1 = "E"
        return super().form_valid(form)
    
    
    def get_context_data(self, **kwargs):
        context = super(Term2SubjectBSModalUpdateView, self).get_context_data(**kwargs)
        context['real_title'] = self.object.real_title
        context["name"] = "{} {} {}".format(
        self.object.student.surname, 
        self.object.student.firstname, 
        self.object.student.lastname)
        return context
    
    def get_success_url(self):
        stu_id = self.object.student.id
        return reverse_lazy("student_subjects_term2", kwargs={'pk':stu_id})

# Term3


@method_decorator([login_required, teacher_required], name="dispatch")
class StudentSubjectTerm3ListView(ListView):
    model = Subject
    template_name = "student_term3_record.html"
    context_object_name = "subjects"
    paginate_by = 10

    def get_queryset(self):
        pk = self.kwargs.get("pk")  # student primary key
        stu = Student.objects.get(pk=pk)
        stu_clss = stu.c_class
        queryset = Subject.objects.filter(student=stu, r_class=stu_clss).order_by(
            "real_title"
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StudentSubjectTerm3ListView, self).get_context_data(**kwargs)
        pk = self.kwargs.get("pk")  # student primary key
        stu = Student.objects.get(pk=pk)
        name = "{} {} {}".format(stu.surname, stu.firstname, stu.lastname)
        context["name"] = name
        context["back_key"] = int(stu.c_class.id)
        return context


@method_decorator([login_required, teacher_required], name="dispatch")
class StudentRatingTerm3CreateView(SuccessMessageMixin, CreateView):
    model = Rating
    form_class = RatingStudentTermForm
    template_name = "student_term3_rating.html"
    success_message = "Rating submitted"

    def form_valid(self, form):
        term = self.kwargs["term"]
        stu_id = self.kwargs["stu_id"]
        clss_id = self.kwargs["clss_id"]

        student = Student.objects.get(id=stu_id)
        r_class = Class.objects.get(id=clss_id)
        if Rating.objects.filter(student=student, r_class=r_class, term=3):
            return ValidationError("Rating already existed for student, edit instead!")
        else:
            pass

        user = self.request.user
        teacher = Teacher.objects.get(user=user)
        clss = Class.objects.get(id=clss_id)
        try:
            FormMaster.objects.get(Teacher=teacher, f_class=clss)
        except ObjectDoesNotExist:
            raise PermissionDenied
        else:
            pass

        form.instance.student = student
        form.instance.r_class = r_class
        form.instance.term = term
        return super().form_valid(form)

    def get_success_url(self):
        return _("student_subjects_term1", kwargs={"pk": self.kwargs["stu_id"]})


@method_decorator([login_required, teacher_required], name="dispatch")
class StudentRatingTerm3UpdateView(SuccessMessageMixin, UpdateView):
    model = Rating
    form_class = RatingStudentTermForm
    template_name = "student_term3_update.html"
    success_message = "Rating Updated!"
    
    def get_success_url(self):
        rating_id = self.kwargs["pk"]
        student = Rating.objects.get(pk=rating_id).student.id
        return _("student_subjects_term3", kwargs={"pk": student})


@method_decorator([login_required, teacher_required], name="dispatch")
class StudentRatingTerm3ListView(ListView):
    model = Rating
    template_name = "student_term3_update.html"
    context_object_name = "ratings"

    def get_queryset(self):
        queryset = super(StudentRatingTerm3ListView, self).get_queryset()
        term = self.kwargs["term"]
        stu_id = self.kwargs["stu_id"]
        clss_id = self.kwargs["clss_id"]

        student = Student.objects.get(id=stu_id)
        r_class = Class.objects.get(id=clss_id)
        queryset = Rating.objects.filter(student=student, r_class=r_class, term=term)
        return queryset

'''
@login_required
@teacher_required
def studentSubjectTerm3Record(request, pk):
    context = {}

    obj = get_object_or_404(Subject, pk=pk)
    stu_id = obj.student.id
    form = SubjectTerm3UpdateForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save(commit=False)
        total = (
            form.instance.test1_term3
            + form.instance.test2_term3
            + form.instance.assignment1_term3
            + form.instance.assignment2_term3
            + form.instance.Exam_term3
        )
        form.instance.total_term3 = total
        if total >= 70 and total <= 100:
            form.instance.grade_term3 = "A"
        elif total >= 60 and total <= 70:
            form.instance.grade_term3 = "B"
        elif total >= 50 and total <= 59:
            form.instance.grade_term3 = "C"
        elif total >= 40 and total <= 49:
            form.instance.grade_term3 = "D"
        else:
            form.instance.grade_term3 = "E"
        form.save()
        return redirect("student_subjects_term3", pk=stu_id)
    context["form"] = form
    context["real_title"] = obj.real_title
    context["name"] = "{} {} {}".format(
        obj.student.surname, obj.student.firstname, obj.student.lastname
    )

    return render(request, "student_term3_record.html", context)
'''

@method_decorator([login_required, teacher_required], name="dispatch")
class Term3SubjectBSModalUpdateView(BSModalUpdateView):
    model = Subject
    form_class = SubjectTerm3UpdateBSModalForm
    template_name = 'partialTerm3SubjectUpdate.html'
    success_message = gettext_lazy('Subject score updated')

    def form_valid(self, form):
        total = (
            form.instance.test1_term3
            + form.instance.test2_term3
            + form.instance.assignment1_term3
            + form.instance.assignment2_term3
            + form.instance.Exam_term3
        )
        form.instance.total_term3 = total
        if total >= 70 and total <= 100:
            form.instance.grade_term3 = "A"
        elif total >= 60 and total <= 70:
            form.instance.grade_term3 = "B"
        elif total >= 50 and total <= 59:
            form.instance.grade_term3 = "C"
        elif total >= 40 and total <= 49:
            form.instance.grade_term3 = "D"
        else:
            form.instance.grade_term3 = "E"
        return super().form_valid(form)
    
    
    def get_context_data(self, **kwargs):
        context = super(Term3SubjectBSModalUpdateView, self).get_context_data(**kwargs)
        context['real_title'] = self.object.real_title
        context["name"] = "{} {} {}".format(
        self.object.student.surname, 
        self.object.student.firstname, 
        self.object.student.lastname)
        return context
    
    def get_success_url(self):
        stu_id = self.object.student.id
        return reverse_lazy("student_subjects_term3", kwargs={'pk':stu_id})
# End term

# Start Result


def compile_class_result(request, clss_id, term_id):
    user = request.user
    teacher = Teacher.objects.get(user=user)
    clss = Class.objects.get(id=clss_id)
    try:
        FormMaster.objects.get(Teacher=teacher, f_class=clss)
    except ObjectDoesNotExist:
        raise PermissionDenied
    else:
        pass

    term = term_id

    # if result model exist update scores
    if Result.objects.filter(result_class=clss, result_term=term):
        res = Result.objects.filter(result_class=clss).values_list("student", flat=True)
        res_stu = Student.objects.filter(id__in=res)
        # all_stu = clss.student_class.all()
        all_stu = res_stu
        totall_stu = len(all_stu)
        for student in all_stu:
            totall = 0
            all_subj = Subject.objects.filter(student=student, r_class=clss)
            total_subj = len(all_subj)
            for subj in all_subj:
                if term == 1:
                    totall += subj.total_term1
                if term == 2:
                    totall += subj.total_term2
                if term == 3:
                    totall += subj.total_term3
            if(student.category =='science'):
                average = totall/13
            elif(student.category == 'social'):
                average = totall/14
            else:
                average = totall / total_subj
            average = round(average, 2)
            if term == 1:
                result = Result.objects.get(
                    student=student, result_class=clss, result_term=1
                )
                result.overrall_totall = totall
                result.average = average
                if totall_stu != 0:
                    result.totall_student = totall_stu
                result.save()
            if term == 2:
                result = Result.objects.get(
                    student=student, result_class=clss, result_term=2
                )
                result.overrall_totall = totall
                result.average = average
                # if session has ended and no studen in the class anymore
                if totall_stu != 0:
                    result.totall_student = totall_stu
                result.save()
            if term == 3:
                result = Result.objects.get(
                    student=student, result_class=clss, result_term=3
                )
                result.overrall_totall = totall
                result.average = average
                if totall_stu != 0:
                    result.totall_student = totall_stu
                result.save()
        messages.add_message(
            request,
            messages.INFO,
            gettext_lazy(
                "Updated! compiled successfull. Click (Distribute position) to redistribute positions in your class."
            ),
        )
    else:

        all_stu = clss.student_class.all()
        totall_stu = len(all_stu)
        for student in all_stu:
            totall = 0
            all_subj = Subject.objects.filter(student=student, r_class=clss)
            for subj in all_subj:
                if term == 1:
                    totall += subj.total_term1
                if term == 2:
                    totall += subj.total_term2
                if term == 3:
                    totall += subj.total_term3
            total_subj = len(all_subj)
            if(student.category =='science'):
                average = totall/13
            elif(student.category == 'social'):
                average = totall/14
            else:
                average = totall / total_subj
            average = round(average, 2)
            if term == 1:
                Result.objects.create(
                    student=student,
                    result_class=clss,
                    overrall_totall=totall,
                    result_term=1,
                    average=average,
                    totall_student=totall_stu,
                )
            if term == 2:
                Result.objects.create(
                    student=student,
                    result_class=clss,
                    overrall_totall=totall,
                    result_term=2,
                    average=average,
                    totall_student=totall_stu,
                )
            if term == 3:
                Result.objects.create(
                    student=student,
                    result_class=clss,
                    overrall_totall=totall,
                    result_term=3,
                    average=average,
                    totall_student=totall_stu,
                )
        messages.add_message(
            request,
            messages.INFO,
            gettext_lazy(
                "All student scores compiled. Click (Distribute Position) to distribute position in your class."
            ),
        )
    return redirect("formmaster_class")


def get_position(request, clss_id, term_id):
    user = request.user
    teacher = Teacher.objects.get(user=user)
    clss = Class.objects.get(id=clss_id)
    try:
        FormMaster.objects.get(Teacher=teacher, f_class=clss)
    except ObjectDoesNotExist:
        raise PermissionDenied
    else:
        pass

    # clss = Class.objects.get(id=clss_id)
    term = term_id
    result_instances = Result.objects.filter(
        result_class=clss, result_term=term
    ).order_by("-average")
    position = 1
    previous_student = ''
    for student in result_instances:
        if(previous_student!=''):
            if(previous_student.average == student.average):
                student.position = previous_student.position
                student.save()
                continue
        student.position = position
        student.save()
        position += 1
        previous_student = student
    messages.add_message(
        request, messages.INFO, gettext_lazy("Positions distributed successfully!")
    )
    return redirect("formmaster_class")


def resultGetSession(request):
    if request.method == "POST":
        form = ResultSessionForm(request.POST)
        if form.is_valid():
            # session = form['session']
            c_session = get_object_or_404(Session, pk=request.POST.get("session"))
            return HttpResponseRedirect(
                reverse("result_class", kwargs={"pk": c_session.pk})
            )  # to get class and registration number

    else:
        form = ResultSessionForm()
    return render(request, "get_result_details.html", {"form": form})


class resultGetClass(FormView):
    form_class = ResultClassForm
    template_name = "get_result_details.html"

    def get_form_kwargs(self):
        kwargs = super(resultGetClass, self).get_form_kwargs()
        kwargs["initial"]["pk"] = self.kwargs["pk"]
        return kwargs

    def form_valid(self, form):
        reg_no = form.cleaned_data["registration_number"]
        # check if student is registered
        try:
            stu = Student.objects.get(registration_number=reg_no)
        except Student.DoesNotExist:
            return render(self.request, template_name="student_not_exist.html")

        c_class = form.cleaned_data["r_class"]
        # check if student belongs to a class

        if stu in c_class.student_class.all():
            pass
        else:
            return render(
                self.request,
                template_name="student_not_in_class.html",
                context={"stu_id": stu.id, "class_id": c_class.id},
            )

        self.stu_id = stu.id
        self.class_id = c_class.id

        self.term = form.cleaned_data["term"]
        return super().form_valid(form)

    def get_success_url(self):

        if int(self.term) == 1:
            return reverse_lazy(
                "print_result_term1",
                kwargs={"class_id": self.class_id, "stu_id": self.stu_id},
            )  # " " treat those kwargs errors
        elif int(self.term) == 2:
            return reverse_lazy(
                "print_result_term2",
                kwargs={"class_id": self.class_id, "stu_id": self.stu_id},
            )
        else:
            return reverse_lazy(
                "print_result_term3",
                kwargs={"class_id": self.class_id, "stu_id": self.stu_id},
            )


# class PdfResponseMixin(
#     object,
# ):
#     def write_pdf(
#         self,
#         file_object,
#     ):
#         context = self.get_context_data()
#         template = self.get_template_names()[0]
#         generate_pdf(template, file_object=file_object, context=context)

#     def render_to_response(self, context, **response_kwargs):
#         resp = HttpResponse(content_type="application/pdf")
#         self.write_pdf(resp)
#         return resp


# class CoverPdfResponseMixin(
#     PdfResponseMixin,
# ):
#     cover_pdf = None

#     def render_to_response(self, context, **response_kwargs):
#         merger = PdfFileMerger()
#         merger.append(open(self.cover_pdf, "rb"))

#         pdf_fo = io.BytesIO()
#         self.write_pdf(pdf_fo)
#         merger.append(pdf_fo)

#         resp = HttpResponse(content_type="application/pdf")
#         merger.write(resp)
#         return resp


# class PrintStudentForm(SuccessMessageMixin, PdfResponseMixin, DetailView):
#     model = Student
#     template_name = "form_pdf.html"
#     context_object_name = "student"
#     success_message = _("form submitted, check your downloaded file")


# class PrintStudentResultTerm1(ListView):
#     model = Subject
#     template_name = "print_result_term1.html"
#     context_object_name = "subjects"

#     def get_queryset(self):
#         queryset = super(PrintStudentResultTerm1, self).get_queryset()
#         stud_id = self.kwargs.get("stu_id")
#         clss_id = self.kwargs.get("class_id")
#         student = Student.objects.get(id=stud_id)
#         c_class = Class.objects.get(id=clss_id)
#         queryset = Subject.objects.filter(student=student, r_class=c_class).order_by(
#             "real_title"
#         )
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super(PrintStudentResultTerm1, self).get_context_data(**kwargs)
#         stud_id = self.kwargs.get("stu_id")
#         clss_id = self.kwargs.get("class_id")
#         student = Student.objects.get(id=stud_id)
#         c_class = Class.objects.get(id=clss_id)
#         totall = Result.objects.get(
#             student=student, result_class=c_class, result_term=1
#         )
#         try:
#             rating = Rating.objects.get(student=student, r_class=c_class, term=1)
#             context["rating"] = rating
#         except Rating.DoesNotExist:
#             pass

#         context["totall_score"] = totall.overrall_totall
#         context["position"] = totall.position
#         context["average"] = totall.average
#         context["totall_student"] = totall.totall_student
#         context["student"] = student
#         context["class"] = c_class
#         return context


# class PrintStudentResultTerm2(ListView):
#     model = Subject
#     template_name = "print_result_term2.html"
#     context_object_name = "subjects"

#     def get_queryset(self):
#         queryset = super(PrintStudentResultTerm2, self).get_queryset()
#         stud_id = self.kwargs.get("stu_id")
#         clss_id = self.kwargs.get("class_id")
#         student = Student.objects.get(id=stud_id)
#         c_class = Class.objects.get(id=clss_id)
#         queryset = Subject.objects.filter(student=student, r_class=c_class)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super(PrintStudentResultTerm2, self).get_context_data(**kwargs)
#         stud_id = self.kwargs.get("stu_id")
#         clss_id = self.kwargs.get("class_id")
#         student = Student.objects.get(id=stud_id)
#         c_class = Class.objects.get(id=clss_id)
#         totall = Result.objects.get(
#             student=student, result_class=c_class, result_term=2
#         )
#         try:
#             rating = Rating.objects.get(student=student, r_class=c_class, term=2)
#             context["rating"] = rating
#         except Rating.DoesNotExist:
#             pass

#         context["totall_score"] = totall.overrall_totall
#         context["position"] = totall.position
#         context["average"] = totall.average
#         context["totall_student"] = totall.totall_student
#         context["student"] = student
#         context["class"] = c_class
#         return context


# class PrintStudentResultTerm3(ListView):
#     model = Subject
#     template_name = "print_result_term3.html"
#     context_object_name = "subjects"

#     def get_queryset(self):
#         queryset = super(PrintStudentResultTerm3, self).get_queryset()
#         stud_id = self.kwargs.get("stu_id")
#         clss_id = self.kwargs.get("class_id")
#         student = Student.objects.get(id=stud_id)
#         c_class = Class.objects.get(id=clss_id)
#         queryset = Subject.objects.filter(student=student, r_class=c_class)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super(PrintStudentResultTerm3, self).get_context_data(**kwargs)
#         stud_id = self.kwargs.get("stu_id")
#         clss_id = self.kwargs.get("class_id")
#         student = Student.objects.get(id=stud_id)
#         c_class = Class.objects.get(id=clss_id)
#         totall = Result.objects.get(
#             student=student, result_class=c_class, result_term=3
#         )
#         try:
#             rating = Rating.objects.get(student=student, r_class=c_class, term=3)
#             context["rating"] = rating
#         except Rating.DoesNotExist:
#             pass

#         context["totall_score"] = totall.overrall_totall
#         context["position"] = totall.position
#         context["average"] = totall.average
#         context["totall_student"] = totall.totall_student
#         context["student"] = student
#         context["class"] = c_class
#         return context


def dashboard(request):
    return render(request, "dashboard2.html")


# PWA
def offlined(request):
    return render(request, "offlined.html")



# LESSONNOTE

@login_required
def lesson_note_create_view(request, class_id):
    class_instance = get_object_or_404(Class, pk=class_id)

    if request.method == 'POST':
        form = LessonNoteForm(request.POST)
        if form.is_valid():
            lesson_note = form.save(commit=False)
            lesson_note.class_level = class_instance  
            lesson_note.teacher = Teacher.objects.get(user = request.user)
            lesson_note.session = class_instance.session
            lesson_note.save()
            return redirect('lesson_notes_list', class_id=class_id)
        else:
            print(form.errors)  
    else:
        form = LessonNoteForm()

    return render(request, 'create_lesson_note.html', {'form': form, 'class_instance': class_instance})



@login_required
def lesson_notes_list_view(request, class_id):
    class_instance = get_object_or_404(Class, pk=class_id)
    lesson_notes = LessonNote.objects.filter(class_level=class_instance)
    form = LessonNoteForm()
    filter_form = LessonNoteFilterForm(request.GET)

    if filter_form.is_valid():
        teacher = filter_form.cleaned_data.get('teacher')
        class_level = filter_form.cleaned_data.get('class_level')
        session = filter_form.cleaned_data.get('session')
        subject = filter_form.cleaned_data.get('subject')

        if teacher:
            lesson_notes = lesson_notes.filter(teacher=teacher)
        # if class_level:
        #     lesson_notes = lesson_notes.filter(class_level=class_level)
        # if session:
        #     lesson_notes = lesson_notes.filter(session=session)
        # if subject:
        #     lesson_notes = lesson_notes.filter(subject=subject)
    
    return render(request, 'lesson_notes_list.html', {'class_instance': class_instance, 'lesson_notes': lesson_notes,'form':form, 'filter_form': filter_form})


@login_required
def edit_lesson_note_view(request, lesson_note_id):
    lesson_note = get_object_or_404(LessonNote, pk=lesson_note_id)

    if request.method == 'POST':
        form = LessonNoteForm(request.POST, instance=lesson_note)
        if form.is_valid():
            form.save()
            return redirect('lesson_notes_list', class_id=lesson_note.class_level.pk)
    else:
        form = LessonNoteForm(instance=lesson_note)

    return render(request, 'edit_lesson_note.html', {'form': form, 'lesson_note': lesson_note})


class LessonNoteDeleteView(DeleteView):
    model = LessonNote
    template_name = 'delete_lesson_note.html'
    def get_success_url(self):
        class_id = self.object.class_level.pk  # Assuming your LessonNote model has a class_id field
        return reverse_lazy('lesson_notes_list', kwargs={'class_id': class_id})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson_note'] = self.get_object()
        return context