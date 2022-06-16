from django import forms
from questions.models import Answer, Question

class QuestionForm(forms.ModelForm):
  class Meta:
    model = Question
    fields = '__all__'

class AnswerForm(forms.ModelForm):
  class Meta:
    model = Answer
    fields = '__all__'
    extra = 4

""" class ModifyQuestionForm(forms.ModelForm):
  # qModel --> Question Model
  def __init__(self, qModel, *args, **kwargs):
    super(ModifyQuestionForm, self).__init__(*args, **kwargs)
    if type(qModel) == 'questions.models.Question':
      print(qModel, type(qModel))
      helper = self.helper = FormHelper()
      # Moving field labels into placeholders
      layout = helper.layout = Layout()
      for field_name, field in self.fields.items():
        if field_name == 'text':
          layout.append(Field(field_name, value=qModel.text))
        else:
          layout.append(Field(field_name))

  class Meta:
    model = Question
    fields = '__all__' """
    