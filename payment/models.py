from django.db import models
from django.contrib.auth.models import User

class quizAccessTable(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
  subjects = models.CharField(max_length=150)
  std = models.CharField(max_length=50)
  
  def __str__(self):
      return f"{self.user}"
