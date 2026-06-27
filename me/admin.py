from django.contrib import admin
from django.db import transaction
from django.utils.html import format_html

from me.models import Project, Resume, Link, Expression, Skill, Career, ResumeExpression, ResumeLink, ResumeSkill, \
    ResumeCareer, ResumeProject, CareerProject, ResumeOthers, Others, CareerProjectFile, ProjectFile, ProjectUrl, \
    ResumeCoverLetter, CoverLetter


class ExpressionInline(admin.TabularInline):
    model = ResumeExpression
    show_change_link = True
    extra = 0
    raw_id_fields = ["expression"]
    ordering = ["order", "expression__order"]


class LinkInline(admin.TabularInline):
    model = ResumeLink
    show_change_link = True
    extra = 0
    ordering = ["order", "link__order", "id"]
    raw_id_fields = ["link"]


class SkillInline(admin.TabularInline):
    model = ResumeSkill
    show_change_link = True
    extra = 0
    ordering = ["order", "skill__order", "id"]
    raw_id_fields = ["skill"]


class CareerInline(admin.TabularInline):
    model = ResumeCareer
    extra = 0
    ordering = ["career__end_date", "id"]
    raw_id_fields = ["career"]


class ProjectInline(admin.TabularInline):
    model = ResumeProject
    show_change_link = True
    extra = 0
    ordering = ["order", "project__order", "id"]
    raw_id_fields = ["project"]


class OthersInline(admin.TabularInline):
    model = ResumeOthers
    show_change_link = True
    extra = 0
    raw_id_fields = ["others"]


class CoverLetterInline(admin.TabularInline):
    model = ResumeCoverLetter
    show_change_link = True
    extra = 0
    raw_id_fields = ["cover_letter"]


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "name", "is_represented", "field_created_at", "field_updated_at"]
    inlines = [ExpressionInline,
               CoverLetterInline,
               LinkInline,
               SkillInline,
               CareerInline,
               ProjectInline,
               OthersInline]
    exclude = ["is_represented", "links", "expressions", "skills", "careers", "projects"]
    actions = ["action_select_active", "action_copy_resume"]
    ordering = ["-is_represented", "-updated_at", "-created_at"]
    readonly_fields = ["field_check_resume"]
    radio_fields = {"is_blinded_email": admin.HORIZONTAL, "is_blinded_phone": admin.HORIZONTAL}

    def get_fields(self, request, obj=None):
        return ["field_check_resume"] + super().get_fields(request, obj)

    @staticmethod
    @admin.display(description="이력서 확인")
    def field_check_resume(instance):
        return format_html(f'<a href="/?resume_id={instance.pk}" target="_blank">이력서 확인</a>')

    @staticmethod
    @admin.display(description="생성일")
    def field_created_at(instance):
        return instance.created_at.strftime("%Y-%m-%d %H:%M")

    @staticmethod
    @admin.display(description="수정일")
    def field_updated_at(instance):
        return instance.updated_at.strftime("%Y-%m-%d %H:%M")

    @admin.display(description="이력서 활성화")
    def action_select_active(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "하나의 이력서만 활성화할 수 있습니다.", level="error")
            return

        resume = queryset.first()
        Resume.objects.update(is_represented=False)
        resume.is_represented = True
        resume.save()
        self.message_user(request, f"{resume.name} 이력서가 활성화되었습니다.")

    @admin.display(description="이력서 복제")
    def action_copy_resume(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "하나의 이력서만 복제할 수 있습니다.", level="error")
            return

        with transaction.atomic():
            resume = queryset.first()
            resume.title = f"{resume.title} (복제본)"
            resume.is_represented = False

            links = list(resume.resumelink_set.all())
            expressions = list(resume.resumeexpression_set.all())
            skills = list(resume.resumeskill_set.all())
            careers = list(resume.resumecareer_set.all())
            projects = list(resume.resumeproject_set.all())
            others = list(resume.resumeothers_set.all())
            cover_letters = list(resume.resumecoverletter_set.all())

            resume.pk = None
            resume.save()

            def copy_subset(subset):
                for x in subset:
                    x.pk = None
                    x.resume = resume
                    x.save()

            [copy_subset(subset) for subset in [links, expressions, careers, projects, others, cover_letters]]
            for x in skills:
                resume.skills.add(x.skill.pk)

        self.message_user(request, f"{resume.name} 이력서가 복제되었습니다.")


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "link"]


@admin.register(CoverLetter)
class CoverLetterAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "short_description", "order", "is_visible"]
    ordering = ["-is_visible", "order"]

    @admin.display(description="Description")
    def short_description(self, obj):
        return obj.description[:50] + "..." if len(obj.description) > 10 else obj.description


class CareerProjectInline(admin.StackedInline):
    model = CareerProject
    show_change_link = True
    ordering = ["order", "id"]
    extra = 0


class CareerProjectFileInline(admin.TabularInline):
    model = CareerProjectFile
    show_change_link = True
    extra = 0


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ["id", "company"]
    inlines = [CareerProjectInline]
    actions = ["action_copy_career"]

    @admin.display(description="경력 복제")
    def action_copy_career(self, request, queryset):
        for career in queryset:
            with transaction.atomic():
                career.company = f"{career.company} (복제본)"

                projects = list(career.careerproject_set.all())
                career_skills = list(career.skills.all())

                career.pk = None
                career.save()

                def copy_subset(subset):
                    for x in subset:
                        x.pk = None
                        x.career = career
                        x.save()

                [copy_subset(subset) for subset in [projects]]
                for x in career_skills:
                    career.skills.add(x.pk)

        self.message_user(request, f"경력이 복제되었습니다.")


@admin.register(CareerProject)
class CareerProjectAdmin(admin.ModelAdmin):
    inlines = [CareerProjectFileInline]


class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    show_change_link = True
    extra = 0


class ProjectUrlInline(admin.TabularInline):
    model = ProjectUrl
    show_change_link = True
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "introduction"]
    inlines = [ProjectFileInline, ProjectUrlInline]


@admin.register(Expression)
class ExpressionAdmin(admin.ModelAdmin):
    list_display = ["id", "keyword", "order"]
    ordering = ["order"]


@admin.register(Others)
class OthersAdmin(admin.ModelAdmin):
    pass
