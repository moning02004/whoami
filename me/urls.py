from django.urls import path

from me import views

urlpatterns = [
    path("", views.index, name="index"),

    path("careers/<int:pk>", views.CareerDetailViewSet.as_view({"get": "retrieve"}), name="career-detail"),
    path("projects/<int:pk>", views.ProjectDetailViewSet.as_view({"get": "retrieve"}), name="career-detail"),
    path("pdf", views.create_pdf, name="create_pdf"),
]