from django.db import models

class ChangedLog(models.Model):
    instance = models.CharField()
    action = models.CharField()
    before = models.JSONField(null=True)
    after = models.JSONField(null=True)
    changed = models.CharField()