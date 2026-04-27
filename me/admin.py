from django.contrib import admin

from me.models import Project, Resume, Link, Expression, Skill, Career, ResumeExpression, ResumeLink, ResumeSkill, \
    ResumeCareer, ResumeProject, CareerProject, ResumeOthers, Others, CareerProjectFile, ProjectFile


class ExpressionInline(admin.TabularInline):
    model = ResumeExpression
    show_change_link = True
    extra = 0
    raw_id_fields = ["expression"]


class LinkInline(admin.TabularInline):
    model = ResumeLink
    show_change_link = True
    extra = 0
    raw_id_fields = ["link"]


class SkillInline(admin.TabularInline):
    model = ResumeSkill
    show_change_link = True
    extra = 0
    raw_id_fields = ["skill"]


class CareerInline(admin.TabularInline):
    model = ResumeCareer
    show_change_link = True
    extra = 0
    raw_id_fields = ["career"]


class ProjectInline(admin.TabularInline):
    model = ResumeProject
    show_change_link = True
    extra = 0
    raw_id_fields = ["project"]


class OthersInline(admin.TabularInline):
    model = ResumeOthers
    show_change_link = True
    extra = 0
    raw_id_fields = ["others"]


@admin.register(Resume)
class MyInfoAdmin(admin.ModelAdmin):
    list_display = ["title", "name", "is_represented", "created_at"]
    inlines = [ExpressionInline,
               LinkInline,
               SkillInline,
               CareerInline,
               ProjectInline,
               OthersInline]
    exclude = ["is_represented", "links", "expressions", "skills", "careers", "projects"]
    actions = ["action_select_active"]

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


@admin.register(Link)
class MyInfoAdmin(admin.ModelAdmin):
    list_display = ["name", "link"]


@admin.register(Skill)
class MyInfoAdmin(admin.ModelAdmin):
    list_display = ["name", "short_description"]

    @admin.display(description="Description")
    def short_description(self, obj):
        return obj.description[:50] + "..." if len(obj.description) > 10 else obj.description


class CareerProjectInline(admin.StackedInline):
    model = CareerProject
    show_change_link = True
    extra = 0


class CareerProjectFileInline(admin.TabularInline):
    model = CareerProjectFile
    show_change_link = True
    extra = 0


class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    show_change_link = True
    extra = 0


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ["company"]
    inlines = [CareerProjectInline]


@admin.register(CareerProject)
class CareerProjectAdmin(admin.ModelAdmin):
    inlines = [CareerProjectFileInline]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "introduction"]
    inlines = [ProjectFileInline]


@admin.register(Expression)
class ExpressionAdmin(admin.ModelAdmin):
    pass


@admin.register(Others)
class OthersAdmin(admin.ModelAdmin):
    pass
