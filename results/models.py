from django.db import models
from quizes.models import Quiz
from django.contrib.auth.models import User


# Create your models here.

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    score = models.FloatField(null = True, blank = True, editable=False)
    date  = models.DateTimeField( auto_now_add=True,null = True , blank = True, editable=False)
    date1 = models.CharField(max_length = 150,null = True , blank = True, editable=False)
    std = models.CharField(max_length=30, null=True, blank=True, editable=False)
    result_summary = models.TextField(null=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.user}-{self.quiz}"