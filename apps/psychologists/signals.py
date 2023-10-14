from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.psychologists.models import ProfilePsychologist
from apps.psychologists.threads import PsychoActivationEmailThread


@receiver(post_save, sender=ProfilePsychologist)
def send_psycho_email(sender, instance, created, update_fields, **kwargs):
    if not created and update_fields is not None:
        if ("is_verified" in update_fields) and (instance.is_verified is True):
            PsychoActivationEmailThread(instance).start()
            print("Письмо отправлено")
