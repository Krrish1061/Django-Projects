from userprofile.models import Profile
from django.contrib.auth.models import User


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def createprofile(sender, instance, created, **kwargs):
    if created:
        user = instance
        Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
