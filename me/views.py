from datetime import datetime
from urllib.parse import quote

from django.db.models import Prefetch, F, When, Case
from django.db.models.functions import Coalesce, Least
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework import viewsets
from weasyprint import HTML

from me.models import Resume, Expression, Link, Skill, Career, Project, Others, ProjectUrl
from me.serializers import CareerDetailSerializer, ProjectDetailSerializer, SkillDetailSerializer


def index(request):
    resume = (Resume.objects.prefetch_related(
        Prefetch(
            'expressions',
            queryset=Expression.objects.annotate(
                effective_order=Least('resumeexpression__order', 'order')
            ).order_by('effective_order').distinct()
        ),
        Prefetch(
            'links',
            queryset=Link.objects.annotate(
                effective_order=Least('resumelink__order', 'order')
            ).order_by('effective_order').distinct()
        ),
        Prefetch(
            'skills',
            queryset=Skill.objects.annotate(
                effective_order=Least('resumeskill__order', 'order')
            ).filter(is_visible=True).order_by('effective_order').distinct()
        ),
        Prefetch('careers', queryset=Career.objects.all().prefetch_related("skills").annotate(
            exit_date=Coalesce("end_date", datetime.now().date()),
        ).order_by("-exit_date")),
        Prefetch(
            'projects',
            queryset=Project.objects.prefetch_related("skills").annotate(
                effective_order=Least('resumeproject__order', 'order')
            ).order_by('effective_order').distinct()
        ),
    ).get(is_represented=True))

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
        queryset = Project.objects.prefetch_related("skills", "projectfile_set",
                                                    Prefetch(
                                                        "projecturl_set",
                                                        ProjectUrl.objects.all().annotate(
                                                            keyword=Case(When(name="", then=F("url"))),
                                                            default=F("name")))
                                                    )
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProjectDetailSerializer
        return None


class SkillViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Skill.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SkillDetailSerializer
        return None


def create_pdf(request):
    resume = (Resume.objects.prefetch_related(
        Prefetch(
            'expressions',
            queryset=Expression.objects.annotate(
                effective_order=Least('resumeexpression__order', 'order')
            ).order_by('effective_order', "id").distinct()
        ),
        Prefetch(
            'links',
            queryset=Link.objects.annotate(
                effective_order=Least('resumelink__order', 'order')
            ).order_by('effective_order', "id").distinct()
        ),
        Prefetch(
            'skills',
            queryset=Skill.objects.annotate(
                effective_order=Least('resumeskill__order', 'order')
            ).filter(is_visible=True).order_by('effective_order', "id").distinct()
        ),
        Prefetch('careers', queryset=Career.objects.all().prefetch_related("skills", "careerproject_set").annotate(
            exit_date=Coalesce("end_date", datetime.now().date()),
        ).order_by("-exit_date")),
        Prefetch(
            'projects',
            queryset=Project.objects.prefetch_related(
                "skills",
                Prefetch(
                    "projecturl_set",
                    ProjectUrl.objects.all().annotate(
                        keyword=Case(When(name="", then=F("url"))), default=F("name")))
            ).annotate(
                effective_order=Least('resumeproject__order', 'order')
            ).order_by('effective_order', "id").distinct()
        ),
        Prefetch(
            'others',
            queryset=Others.objects.annotate(
                effective_order=Least('resumeothers__order', 'order')
            ).order_by('effective_order', "id").distinct()
        ),
    ).get(is_represented=True))

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

        filename = "유정훈_이력서"
        encoded = quote(filename, safe='')
        return HttpResponse(pdf, content_type='application/pdf',
                            headers={'Content-Disposition': f'attachment; filename="{encoded}.pdf"'})
    return render(request, 'pdf_template.html', context)
