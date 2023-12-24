from django.contrib.auth.models import User
from django.db import models

class Inductees(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rollnumber = models.CharField(max_length=9, blank=False, default='000000000')
    department = models.CharField(max_length=50, blank=False, default='National Institute of Technology, Durgapur')
    is_club_member = models.BooleanField(default=False)
    profile_picture = models.URLField(blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    year = models.IntegerField(default=1)
    def __str__(self):
        return self.user.username + " | " + self.rollnumber
    
class Posts(models.Model):
    user = models.ForeignKey(Inductees, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    round = models.IntegerField(default=1)
    by = models.CharField(max_length=255, blank=True)
    year = models.IntegerField(default=2)
    class Meta:
        ordering = ['-round','-date']

    def __str__(self):
        return self.user.username + " | " + self.comment[:50]
    
