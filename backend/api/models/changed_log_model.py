from django.db import models

class ChangedLog(models.Model):
    model = models.CharField()
    model_id = models.IntegerField(null=True)
    action = models.CharField()
    changes = models.JSONField(null=True)