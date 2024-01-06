from django.contrib.auth.models import User
from django.db import models
import json

class Inductees(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rollnumber = models.CharField(max_length=9, blank=False, default='000000000')
    department = models.CharField(max_length=50, blank=False, default='National Institute of Technology, Durgapur')
    is_club_member = models.BooleanField(default=False)
    profile_picture = models.URLField(blank=True)
    gender = models.CharField(max_length=10, choices=[('M','M'),('F','F'),('O','O'),],blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    year = models.IntegerField(default=1)
    registration_no = models.CharField(max_length=15,blank=True)
    place = models.CharField(max_length=50,blank=True)
    round = models.IntegerField(default=1)
    like = models.ManyToManyField(User, related_name='vote')
    color=models.IntegerField(choices=[(1,'red'),(2,'yellow'),(3,'green'),(4,'transparent')],default=4)

    def total_likes(self):
        return self.like.count()


    def __str__(self):
        return self.user.username + " | " + self.rollnumber
    
class Posts(models.Model):
    user = models.ForeignKey(Inductees, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)
    round = models.IntegerField(default=1)
    by = models.CharField(max_length=255, blank=True)
    year = models.IntegerField(default=2)
    class Meta:
        ordering = ['-round','-date']
    def __str__(self):
        return self.user.full_name + " | " + self.comment[:50]

class Question(models.Model):
    question = models.CharField(max_length=100)
    types = [
        ('text', 'text'),
        ('range', 'range'),
        ('options', 'options'),
    ]
    type = models.CharField(max_length=10, choices=types, default='text')
    additional_data = models.JSONField(null = True, blank = True)
    def getData(self):
        return json.loads(self.additional_data)
    

    def __str__(self):
        return self.question

class Response(models.Model):
    student = models.ForeignKey(Inductees, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    class Meta:
        unique_together = ('student', 'question')
    def __str__(self):
        return f"{self.student} : {self.question.id} : {self.answer}"