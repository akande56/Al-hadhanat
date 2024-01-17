from django.urls import path

from .views import (  # ViewTerm1,; pWA; offline,
    DeleteSubject,
    FommasterStudentListView,
    FormmasterAllSubjectsListView,
    FormmasterClassListView,
    FormmastStudentCreateView,
    # PrintStudentForm,
    # PrintStudentResultTerm1,
    # PrintStudentResultTerm2,
    # PrintStudentResultTerm3,
    StudentCreateView,
    StudentDetailView,
    StudentRatingTerm1CreateView,
    StudentRatingTerm1ListView,
    StudentRatingTerm1UpdateView,
    StudentRatingTerm2CreateView,
    StudentRatingTerm2ListView,
    StudentRatingTerm2UpdateView,
    StudentRatingTerm3CreateView,
    StudentRatingTerm3ListView,
    StudentRatingTerm3UpdateView,
    StudentSubjectTerm1ListView,
    StudentSubjectTerm2ListView,
    StudentSubjectTerm3ListView,
    StudentToSubjectsCreateView,
    StudentUpdateView,
    Term1SubjectBSModalUpdateView,
    Term2SubjectBSModalUpdateView,
    Term3SubjectBSModalUpdateView,
    compile_class_result,
    dashboard,
    get_position,
    load_lga,
    resultGetClass,
    resultGetSession,
    student_delete_view,
    student_single_addSubject,
    lesson_note_create_view,
    lesson_notes_list_view,
    edit_lesson_note_view,
    LessonNoteDeleteView,
)

urlpatterns = [
    # path("offlined", offline, name="offlined"),
    path("add_student", StudentCreateView, name="admit_student"),
    path("ajax/load-lga/", load_lga, name="ajax_load_lga"),
    path("dashboard", dashboard, name="dashboard"),
    # path("printStudentForm/<int:pk>", PrintStudentForm.as_view(), name="studentform"),
    path(
        "formmaster/class", FormmasterClassListView.as_view(), name="formmaster_class"
    ),
    path('formmaster/class/new_note/<int:class_id>', lesson_note_create_view, name='lesson_note_create'),
    path('lesson-notes/<int:class_id>/', lesson_notes_list_view, name='lesson_notes_list'),
    path('lesson-notes/<int:lesson_note_id>/edit/', edit_lesson_note_view, name='edit_lesson_notes'),
    path('lesson_note/<int:pk>/delete/', LessonNoteDeleteView.as_view(), name='delete_lesson_note'),
    path(
        "formmaster/class/subjects/<int:class_pk>",
        FormmasterAllSubjectsListView.as_view(),
        name="class_all_subjects",
    ),
    path(
        "formmaster/class/add_subject/<int:pk>",
        StudentToSubjectsCreateView.as_view(),
        name="add_class",
    ),
    path(
        "formmaster/class/students/<int:pk>/",
        FommasterStudentListView.as_view(),
        name="formmaster_students",
    ),
    path(
        "formmaster/class/students/subjects/records/term1/<int:pk>",
        StudentSubjectTerm1ListView.as_view(),
        name="student_subjects_term1",
    ),
    
    # new
    path(
       "formmaster/class/students/subjects/record/term1/editModal/<int:pk>",
       Term1SubjectBSModalUpdateView.as_view(),
       name="subject_record_term1Modal"
    ),
    path(
        "formmaster/class/students/term1/rating/<int:term>/<int:clss_id>/<int:stu_id>",
        StudentRatingTerm1CreateView.as_view(),
        name="student_term1_rating",
    ),  # new
    path(
        "formmaster/class/students/term1/rating/update/<int:pk>",
        StudentRatingTerm1UpdateView.as_view(),
        name="student_term1_rating_update",
    ),  # new
    path(
        "formmaster/class/students/term1/rating/list/<int:term>/<int:clss_id>/<int:stu_id>",
        StudentRatingTerm1ListView.as_view(),
        name="student_term1_rating_list",
    ),  # new
    path(
        "formmaster/class/students/subjects/records/term2/<int:pk>",
        StudentSubjectTerm2ListView.as_view(),
        name="student_subjects_term2",
    ),
    path(
        "formmaster/class/students/subjects/record/term2/editModal/<int:pk>",
        Term2SubjectBSModalUpdateView.as_view(),
        name="subject_record_term2Modal",
    ),
    path(
        "formmaster/class/students/term2/rating/<int:term>/<int:clss_id>/<int:stu_id>",
        StudentRatingTerm2CreateView.as_view(),
        name="student_term2_rating",
    ),  # new
    path(
        "formmaster/class/students/term2/rating/update/<int:pk>",
        StudentRatingTerm2UpdateView.as_view(),
        name="student_term2_rating_update",
    ),  # new
    path(
        "formmaster/class/students/term2/rating/list/<int:term>/<int:clss_id>/<int:stu_id>",
        StudentRatingTerm2ListView.as_view(),
        name="student_term2_rating_list",
    ),  # new
    path(
        "formmaster/class/students/subjects/records/term3/<int:pk>",
        StudentSubjectTerm3ListView.as_view(),
        name="student_subjects_term3",
    ),
    path(
        "formmaster/class/students/subjects/record/term3/editModal/<int:pk>",
        Term3SubjectBSModalUpdateView.as_view(),
        name="subject_record_term3Modal",
    ),
    path(
        "formmaster/class/students/term3/rating/<int:term>/<int:clss_id>/<int:stu_id>",
        StudentRatingTerm3CreateView.as_view(),
        name="student_term3_rating",
    ),  # new
    path(
        "formmaster/class/students/term3/rating/update/<int:pk>",
        StudentRatingTerm3UpdateView.as_view(),
        name="student_term3_rating_update",
    ),  # new
    path(
        "formmaster/class/students/term3/rating/list/<int:term>/<int:clss_id>/<int:stu_id>",
        StudentRatingTerm3ListView.as_view(),
        name="student_term3_rating_list",
    ),  # new
    path("resultGetSession/", resultGetSession, name="result_session"),
    path("resultGetClass/<int:pk>", resultGetClass.as_view(), name="result_class"),
    # path(
    #     "print_result/term1/<int:stu_id>/<int:class_id>",
    #     PrintStudentResultTerm1.as_view(),
    #     name="print_result_term1",
    # ),
    # path(
    #     "view_result/<int:class_id>/<int:stu_id>",
    #     ViewTerm1.as_view(),  # just opening the bracket solved the as_view() takes 1 postional argumemt
    #     name="view_result_term1",
    # ),
    # path(
    #     "print_result/term2/<int:stu_id>/<int:class_id>",
    #     PrintStudentResultTerm2.as_view(),
    #     name="print_result_term2",
    # ),
    # path(
    #     "print_result/term3/<int:stu_id>/<int:class_id>",
    #     PrintStudentResultTerm3.as_view(),
    #     name="print_result_term3",
    # ),
    path(
        "add_single_student_subject/<int:pk>",
        student_single_addSubject,
        name="add_single_student_subject",
    ),
    path(
        "formmaster/class/add_student/<int:pk>",
        FormmastStudentCreateView.as_view(),
        name="class_add_student",
    ),
    path(
        "student/details/<int:pk>", StudentDetailView.as_view(), name="student_detail"
    ),
    path(
        "student/delete/<int:pk>/<int:cl>", student_delete_view, name="student_delete"
    ),
    path("student/update/<int:pk>", StudentUpdateView.as_view(), name="student_update"),
    path(
        "compile/result/class/<int:clss_id>/<int:term_id>",
        compile_class_result,
        name="compile_result",
    ),
    path("positioning/<int:clss_id>/<int:term_id>", get_position, name="position"),
    path("subject/delete/<int:subjt_id>", DeleteSubject, name="delete_subject"),
]
