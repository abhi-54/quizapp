from django.db import models
import random
from regester.models import profile1
# Create your models here.

DIFF_CHOICES = (
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard'),
)
stdchoice = (
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'), 
    ('CET', 'CET'), 
    ('JEE', 'JEE'), 
    ('NEET', 'NEET'),
    ('Navodaya Vidyalaya', 'Navodaya Vidyalaya') ,
    ('12 COMBO', '12 COMBO'),

)

class Subjects1(models.Model):
    name = models.CharField(max_length=120)
    std =models.CharField(max_length=20, choices=stdchoice, default='')

    def get_subject_name(self):
        return str(self.name)

    def __str__(self):
        return f"{self.name}-{self.std}"

class Quiz(models.Model):
    subject = models.ForeignKey(Subjects1,on_delete=models.CASCADE,null=True,blank = True)
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="Duration of the Quiz in minutes")
    required_score_to_pass = models.IntegerField(help_text="Required Score in %")
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        question = list(self.question_set.all())
        random.shuffle(question)
        return question[:self.number_of_questions]

    class Meta:
        verbose_name_plural = 'Quizes'
