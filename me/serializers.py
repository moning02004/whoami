from rest_framework import serializers

from me.models import Career, Skill, CareerProject, Project


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["name"]


class CareerProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerProject
        fields = ["title", "period", "content", "result"]


class CareerDetailSerializer(serializers.ModelSerializer):
    period = serializers.SerializerMethodField()
    skills = SkillSerializer(many=True)
    projects = CareerProjectSerializer(many=True, source="careerproject_set")

    class Meta:
        model = Career
        fields = ["company", "position", "period", "introduction", "summary", "skills", "projects"]

    @staticmethod
    def get_period(obj):
        end = obj.end_date or "현재"
        return f"{obj.start_date} - {end}"


class ProjectDetailSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = Project
        fields = ["title", "introduction", "content", "result", "skills"]
