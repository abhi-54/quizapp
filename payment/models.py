from django.contrib.auth.models import User
from django.db import models

from regester.models import profile1

# Create your models here.

class quizAccessTable(models.Model):
  user = models.CharField(max_length=50, unique=True)
  subjects = models.CharField(max_length=150)
  std = models.CharField(max_length=50)

  def __str__(self):
      return f"{self.user}"
