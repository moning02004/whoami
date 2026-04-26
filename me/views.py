from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework import viewsets
from weasyprint import HTML

from me.models import Resume, Career, Project
from me.serializers import CareerDetailSerializer, ProjectDetailSerializer


def index(request):
    resume = Resume.objects.prefetch_related("expressions", "links", "skills", "careers", "projects").get(
        is_represented=True)

    return render(request, "index.html", {
        "resume": resume,
    })


class CareerDetailViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Career.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CareerDetailSerializer
        return None


class ProjectDetailViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Project.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProjectDetailSerializer
        return None


def create_pdf(request):
    resume = Resume.objects.prefetch_related(
        "expressions", "links", "skills", "careers", "projects"
    ).get(is_represented=True)
    print(resume.profile_image.url)
    context = {
        "resume": resume,
        "links": resume.links.all(),
        "expressions": resume.expressions.all(),
        "careers": resume.careers.all(),
        "skills": resume.skills.all(),
        "projects": resume.projects.all(),
        "others": resume.others.all(),
    }

    if request.method == "POST":
        html_str = render_to_string('pdf_template.html', context)
        pdf = HTML(string=html_str).write_pdf()

        return HttpResponse(pdf, content_type='application/pdf',
                            headers={'Content-Disposition': 'attachment; filename="resume.pdf"'})
    return render(request, 'pdf_template.html', context)
