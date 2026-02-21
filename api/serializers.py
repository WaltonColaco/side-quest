from rest_framework import serializers

from .models import Assessment, Comparison


class AssessmentSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name")

    class Meta:
        model = Assessment
        fields = ["id", "project_name", "overall_score", "rubric_version", "notes", "created_at"]


class ComparisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comparison
        fields = "__all__"
