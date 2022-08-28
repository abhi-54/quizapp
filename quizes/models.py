from django.db import models
import random
from regester.utils import stdchoice, DIFF_CHOICES

class Subjects1(models.Model):
    name = models.CharField(max_length=120)
    std =models.CharField(max_length=20, choices=stdchoice, default='')

    def get_subject_name(self):
        return str(self.name)

    def __str__(self):
        return f"{self.name}-{self.std}"

class Quiz(models.Model):
    subject = models.ForeignKey(Subjects1, on_delete=models.CASCADE, null=True, blank = True, verbose_name='Subject-Class')
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
