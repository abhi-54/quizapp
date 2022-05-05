from django.db import models
from quizes.models import Quiz
from regester.forms import FormRegestration

# Create your models here.

questionType_CHOICES = (
    ('MCQ', 'MCQ'),
    ('Fill in the blanks', 'Fill in the blanks'), 
)


class Question(models.Model):
    text = models.CharField(max_length=200, unique=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    type_of_question = models.CharField(max_length=20, choices=questionType_CHOICES, default=questionType_CHOICES[0])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question: {self.question.text}, Answer: {self.text}, Correct: {self.correct}"
