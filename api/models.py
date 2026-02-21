from django.db import models


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
