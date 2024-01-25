from django.urls import path

from .views import (
    AdminAllClassListView,
    AdminAllstudentListView,
    AdminClassListView,
    AdminClassStudentListView,
    AdminFormMasterCreateView,
    AdminFormMasterListView,
    AdminSessionCreateView,
    AdminSessionListView,
    AdminStudentCreateView,
    AdminStudentfilterView,
    AdminStudentUpdateView,
    AdminTeacherListView,
    QACreateView,
    QAListView,
    admin_lesson_notes_list_view,
)

urlpatterns = [
    path("session/add_session/", AdminSessionCreateView.as_view(), name="add_session"),
    path("session/list", AdminSessionListView.as_view(), name="session_list"),
    path(
        "session/list/session_class/<int:session_id>",
        AdminAllClassListView.as_view(),
        name="session_class",
    ),
    path(
        "session/students/<int:class_id>/",
        AdminClassStudentListView.as_view(),
        name="admin_class_students",
    ),
    path("techers", AdminTeacherListView.as_view(), name="teachers"),
    path("all_class/list", AdminClassListView.as_view(), name="all_class"),
    path("all_student", AdminAllstudentListView.as_view(), name="all_student"),
    path("add_student", AdminStudentCreateView.as_view(), name="add_new_student"),
    path("all_student/filter", AdminStudentfilterView, name="student_filter_list"),
    path("add_formmaster", AdminFormMasterCreateView.as_view(), name="add_formmaster"),
    path("formmaster/list", AdminFormMasterListView.as_view(), name="formmaster_list"),
    path(
        "update/student/<int:pk>",
        AdminStudentUpdateView.as_view(),
        name="admin_update_student",
    ),
    path("make_enquiry", QACreateView.as_view(), name="make_enquiry"),
    path("enquiries", QAListView.as_view(), name="enquiries"),
    path("lesson_notes/", admin_lesson_notes_list_view, name='admin_lesson_notees_list'),
]
