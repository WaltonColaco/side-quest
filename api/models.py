from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.TextField(blank=True, default="")
    location = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.user.username} profile"


class Project(models.Model):
    name = models.TextField()
    building_type = models.TextField()
    address = models.TextField(null=True)
    created_at = models.TextField()

    class Meta:
        managed = False
        db_table = "projects"


class Assessment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    overall_score = models.FloatField()
    rubric_version = models.TextField()
    notes = models.TextField(null=True)
    created_at = models.TextField()

    class Meta:
        managed = False
        db_table = "assessments"


class Comparison(models.Model):
    rubric_document_id = models.IntegerField()
    candidate_document_id = models.IntegerField()
    mode = models.TextField()
    model = models.TextField()
    threshold_strong = models.FloatField()
    threshold_partial = models.FloatField()
    strong_count = models.IntegerField()
    partial_count = models.IntegerField()
    missing_count = models.IntegerField()
    overall_score = models.FloatField()
    created_at = models.TextField()

    class Meta:
        managed = False
        db_table = "comparisons"


class Location(models.Model):
    name = models.TextField(null=True)
    address = models.TextField(null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    source_doc = models.TextField(null=True)
    score = models.FloatField(null=True)
    comparison_id = models.IntegerField(null=True)
    report_path = models.TextField(null=True)
    user_id = models.IntegerField(null=True)
    created_at = models.TextField()

    class Meta:
        managed = False
        db_table = "locations"


class ChunkMatch(models.Model):
    comparison_id = models.IntegerField()
    rubric_chunk_id = models.IntegerField()
    candidate_chunk_id = models.IntegerField(null=True)
    similarity = models.FloatField()
    status = models.TextField()
    rubric_path = models.TextField(null=True)
    candidate_path = models.TextField(null=True)
    rubric_excerpt = models.TextField(null=True)
    candidate_excerpt = models.TextField(null=True)

    class Meta:
        managed = False
        db_table = "chunk_matches"
