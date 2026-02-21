from rest_framework import serializers

from .models import Assessment, Comparison, Location


class AssessmentSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name")

    class Meta:
        model = Assessment
        fields = ["id", "project_name", "overall_score", "rubric_version", "notes", "created_at"]


class ComparisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comparison
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class PinDetailSerializer(serializers.Serializer):
    score = serializers.FloatField(allow_null=True)
    address = serializers.CharField(allow_null=True)
    name = serializers.CharField(allow_null=True)
    source = serializers.CharField(allow_null=True)
    passes = serializers.ListField()
    fails = serializers.ListField()
