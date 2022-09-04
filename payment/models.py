from django.db import models
from regester.models import profile1

class quizAccessTable(models.Model):
  #user = models.ForeignKey(profile1, on_delete=models.CASCADE, to_field='user')
  user = models.CharField(max_length=50, unique=True)
  subjects = models.CharField(max_length=150)
  std = models.CharField(max_length=50)
  
  def __str__(self):
      return f"{self.user}"
