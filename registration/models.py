from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, null=True, blank=False ,on_delete= models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=[('M','M'),('F','F'),('O','O'),])
    registration_no = models.CharField(max_length=15)
    roll_no = models.CharField(max_length=15)
    branch = models.CharField(max_length=15)
    place = models.CharField(max_length=50)

    def __str__(self):
        return self.name

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
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    class Meta:
        unique_together = ('student', 'question')
    def __str__(self):
        return f"{self.student} : {self.question.id} : {self.answer}"
       