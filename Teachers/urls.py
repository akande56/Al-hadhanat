from django.urls import path

from .views import TeacherSignUpCreateView, gallery

urlpatterns = [
    path("add_teacher/", TeacherSignUpCreateView.as_view(), name="add_teacher"),
    path("school-gallery", gallery, name="gallery"),
]
