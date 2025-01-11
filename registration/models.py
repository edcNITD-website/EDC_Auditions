from django.contrib.auth.models import User
from django.db import models
import json

GENDER_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other"),
]

COLOR_CHOICES = [
    (0, "Transparent"),
    (1, "Red"),
    (2, "Yellow"),
    (3, "Green"),
    (4, "Orange")
]

DOMAIN_CHOICES = [
    ("WEBD", "Web Development"),
    ("VIDEO", "Video Editing"),
    ("CONTENT", "Content Writing"),
    ("GRAPHIC", "Graphic Designing"),
    ("EVENT", "Event Management"),
]

QUESTION_TYPE_CHOICES = [
    ("text", "Text"),
    ("range", "Range"),
    ("options", "Options"),
]

DEPARTMENT_CHOICES = [
    ("CS", "Computer Science and Engineering"),
    ("EC", "Electronics and Communication Engineering"),
    ("EE", "Electrical Engineering"),
    ("ME", "Mechanical Engineering"),
    ("CE", "Civil Engineering"),
    ("CH", "Chemical Engineering"),
    ("MM", "Metallurgical and Materials Engineering"),
]

YEAR_CHOICES = [
    (1, "First Year"),
    (2, "Second Year"),
    (3, "Prefinal Year"),
    (4, "Final Year"),
]


class Inductees(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rollnumber = models.CharField(max_length=9, blank=False, default="")
    department = models.CharField(
        max_length=2, choices=DEPARTMENT_CHOICES, blank=False, default=""
    )
    is_club_member = models.BooleanField(default=False)
    profile_picture = models.URLField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    full_name = models.CharField(max_length=255, blank=False)
    phone_number = models.CharField(max_length=10, blank=True)
    year = models.IntegerField(choices=YEAR_CHOICES, blank=False, default=1)
    registration_no = models.CharField(max_length=15, blank=True, default="")
    place = models.CharField(max_length=50, blank=True)
    round = models.IntegerField(default=1)
    like = models.ManyToManyField(User, related_name="vote")
    color = models.IntegerField(choices=COLOR_CHOICES, default=0)
    # TODO: add mulitple domains
    domains = models.CharField(max_length=7, choices=DOMAIN_CHOICES, blank=True)

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
    year = models.IntegerField(choices=YEAR_CHOICES[1:], default=2)

    class Meta:
        ordering = ["-round", "-date"]

    def __str__(self):
        return self.user.full_name + " | " + self.comment[:50]


class Question(models.Model):
    question = models.CharField(max_length=100)
    type = models.CharField(
        max_length=10, choices=QUESTION_TYPE_CHOICES, default="text"
    )
    additional_data = models.JSONField(null=True, blank=True)

    def getData(self):
        return json.loads(self.additional_data)

    def __str__(self):
        return self.question


class Response(models.Model):
    student = models.ForeignKey(Inductees, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)

    class Meta:
        unique_together = ["student", "question"]

    def __str__(self):
        return f"{self.student} : {self.question.id} : {self.answer}"


class Result(models.Model):
    inductee = models.OneToOneField(
        Inductees, on_delete=models.CASCADE, blank=True, null=True
    )
    round = models.IntegerField(default=1)
    domain = models.CharField(max_length=25, choices=DOMAIN_CHOICES, blank=True)

    def __str__(self):
        return self.inductee.full_name + " | " + self.domain

    class Meta:
        ordering = ["-round"]
