from django.db.models.signals import pre_save, post_save, pre_delete
from api.models import Booking, Guest, Room, ChangedLog
import json

models_list = [
    Room,
    Guest,
    Booking
]

changes = {}

def prev_save_handler(sender, instance, **kwargs):
    obj = sender.objects.filter(id=instance.id).values().first()
    if obj:
        changes["before"] = obj
        if isinstance(instance, Booking):
            changes["before"]["start_date"] = str(changes["before"]["start_date"])
            changes["before"]["end_date"] = str(changes["before"]["end_date"])
    else:
        changes["before"] = None

def post_save_handler(sender, instance, created, *args, **kwargs):
    obj = sender.objects.filter(id=instance.id).values().first()
    changes["after"] = obj
    if isinstance(instance, Booking) and obj:
        changes["after"]["start_date"] = str(changes["after"]["start_date"])
        changes["after"]["end_date"] = str(changes["after"]["end_date"])
    
    data = {
        "model": sender.__name__,
        "model_id": obj["id"] if obj else changes["before"]["id"],
        "action": "CREATE" if created else "UPDATE" if not obj else "DELETE",
        "changes": _get_changes(changes)
    }
    ChangedLog.objects.create(**data)

def prev_delete_handler(sender, instance, *args, **kwargs):
    obj = sender.objects.filter(id=instance.id).values().first()
    changes["before"] = obj
    changes["after"] = None
    data = {
        "model": sender.__name__,
        "model_id": obj["id"],
        "action": "DELETE",
        "changes": _get_changes(changes)
    }
    ChangedLog.objects.create(**data)

def _get_changes(changes):
    res = {"before": {}, "after": {}}
    d = changes["before"] if changes["before"] != None else changes["after"]
    for key, value in d.items():
        if not changes["before"]:
            res["before"] = None
            res["after"] = d
        elif not changes["after"]:
            res["before"] = d
            res["after"] = None
        else:
            if changes["before"][key] != changes["after"][key]:
                res["before"][key] = changes["before"][key]
                res["after"][key] = changes["after"][key]
    return res

for model in models_list:
    pre_save.connect(prev_save_handler, sender=model)
    post_save.connect(post_save_handler, sender=model)
    pre_delete.connect(prev_delete_handler, sender=model)
