from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from .models import Inductees

@receiver(post_save, sender=SocialAccount)
def create_inductees_profile(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        inductees_profile, created = Inductees.objects.get_or_create(user=user)
        google_account = user.socialaccount_set.filter(provider='google').first()
        if google_account:
            inductees_profile.profile_picture = google_account.get_avatar_url()
            inductees_profile.full_name = google_account.extra_data.get('name', '')
            inductees_profile.save()
