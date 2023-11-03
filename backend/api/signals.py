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
        if sender == Booking:
            changes["before"]["start_date"] = str(changes["before"]["start_date"])
            changes["before"]["end_date"] = str(changes["before"]["end_date"])
    else:
        changes["before"] = None

def post_save_handler(sender, instance, created, *args, **kwargs):
    obj = sender.objects.filter(id=instance.id).values().first()
    changes["after"] = obj
    breakpoint()
    if sender == Booking:
        changes["after"]["start_date"] = str(changes["after"]["start_date"])
        changes["after"]["end_date"] = str(changes["after"]["end_date"])
    data = {
        "instance": sender,
        "action": "POST" if created else "PUT",
        "before": changes["before"],
        "after": changes["after"],
        "changed": _get_changes(changes) if changes["before"] else f"created - {obj}"
    }
    ChangedLog.objects.create(**data)

def prev_delete_handler(sender, instance, *args, **kwargs):
    obj = sender.objects.filter(id=instance.id).values().first()
    changes["before"] = obj
    data = {
        "instance": sender,
        "action": "DELETE",
        "before": changes["before"],
        "after": None,
        "changed": f"deleted - {obj}"
    }
    ChangedLog.objects.create(**data)

def _get_changes(changes):
    res = "Changes on - "
    for key, value in changes["before"].items():
        if changes["before"][key] != changes["after"][key]:
            res += f"{key}, with value from {value} into {changes['after'][key]} - "
    return res

for model in models_list:
    pre_save.connect(prev_save_handler, sender=model)
    post_save.connect(post_save_handler, sender=model)
    pre_delete.connect(prev_delete_handler, sender=model)
