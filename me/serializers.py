import re

import markdown
from django.utils.safestring import mark_safe
from rest_framework import serializers

from me.models import Career, Skill, CareerProject, Project, ProjectFile, CareerProjectFile, ProjectUrl


class MarkdownField(serializers.CharField):
    def to_representation(self, value):
        value = value.replace('\r\n', '\n')
        value = re.sub(r'\n{3,}', '\n\n<br>\n\n', value)
        converted_text = mark_safe(markdown.markdown(value))
        return converted_text


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        model = kwargs.pop('model', None)
        fields = kwargs.pop('fields', None)  # fields 인자 꺼내기
        exclude = kwargs.pop('exclude', None)
        self.model = model

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            for field_name in exclude:
                self.fields.pop(field_name, None)


class CareerProjectFileSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='file.url', read_only=True)

    class Meta:
        model = CareerProjectFile
        fields = ["url"]


class SkillSerializer(DynamicFieldsModelSerializer):
    content = MarkdownField()

    class Meta:
        model = Skill
        fields = "__all__"


class CareerProjectSerializer(serializers.ModelSerializer):
    files = CareerProjectFileSerializer(many=True, source="careerprojectfile_set")

    content = MarkdownField()
    result = MarkdownField()

    class Meta:
        model = CareerProject
        fields = ["title", "introduction", "period", "content", "result", "files"]


class CareerDetailSerializer(serializers.ModelSerializer):
    period = serializers.SerializerMethodField()
    skills = SkillSerializer(fields=["name"], many=True)
    projects = CareerProjectSerializer(many=True, source="careerproject_set")

    class Meta:
        model = Career
        fields = ["company", "position", "note", "period", "introduction", "summary", "skills", "projects"]

    @staticmethod
    def get_period(obj):
        end = obj.end_date.strftime("%Y. %m. %d") if obj.end_date else "재직중"
        return f"{obj.start_date.strftime('%Y. %m. %d')} ~ {end}"


class ProjectFileSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='file.url', read_only=True)

    class Meta:
        model = ProjectFile
        fields = ["url"]


class ProjectUrlSerializer(serializers.ModelSerializer):
    keyword = serializers.CharField(read_only=True)

    class Meta:
        model = ProjectUrl
        fields = ["keyword", "url"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(fields=["name"], many=True)
    files = ProjectFileSerializer(many=True, source="projectfile_set")
    urls = ProjectUrlSerializer(many=True, source="projecturl_set")

    content = MarkdownField()
    result = MarkdownField()

    class Meta:
        model = Project
        fields = ["title", "introduction", "content", "result", "skills", "files", "urls"]


class SkillDetailSerializer(serializers.ModelSerializer):
    description = MarkdownField()

    class Meta:
        model = Skill
        fields = ["name", "description"]
