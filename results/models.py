from django.db import models
from quizes.models import Quiz
from django.contrib.auth.models import User

# Create your models here.

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField(null = True, blank = True)
    date  = models.DateTimeField( auto_now_add=True,null = True , blank = True)
    date1 = models.CharField(max_length = 150,null = True , blank = True)
    
    def __str__(self):
        return str(self.pk)


class userResult(models.Model):
    user = models.CharField(max_length=120)
    question = models.CharField(max_length=120)
    answer = models.CharField(max_length=120)
    topic = models.CharField(max_length=120,null=True, blank=True)