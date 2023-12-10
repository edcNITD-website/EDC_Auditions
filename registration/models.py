from django.contrib.auth.models import User
from django.db import models

class Inductees(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rollnumber = models.CharField(max_length=9, blank=False, default='000000000')
    department = models.CharField(max_length=50, blank=False, default='National Institute of Technology, Durgapur')
    is_club_member = models.BooleanField(default=False)
    profile_picture = models.URLField(blank=True)
    full_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username + " | " + self.rollnumber