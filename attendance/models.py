from django.db import models
from django.contrib.auth.models import User

# Create your models here.

choices = (
  ('Present', 'Present'),
  ('Absent', 'Absent')
)

class attendanceTable(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  course_name = models.CharField(max_length=50, null=True)
  date = models.DateField(null=True, help_text='Format: yyyy-mm-dd')
  attendance = models.CharField(max_length=15, null=True, choices=choices)

  def __str__(self):
    return f"{self.user}, {self.date}, {self.course_name}"
  


