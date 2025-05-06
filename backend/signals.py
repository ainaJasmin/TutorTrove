from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Tutor
from django.contrib.auth.models import Group


def tutor_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='tutor')
        instance.groups.add(group)

        Tutor.objects.create(
                user = instance,
                name=instance.username,
                email=instance.email,
                )
        
        print(instance.username + 'Profile created')
        
post_save.connect(tutor_profile, sender=User)

