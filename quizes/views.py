from django.db import models
from django.shortcuts import render
from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Answer, Question
from results.models import Result
from results.models import userResult
import datetime
# Create your views here.
class QuizListView(ListView):
  model = Quiz
  template_name = 'quizes/main.html'

def quiz_view(request, pk):
  quiz = Quiz.objects.get(pk = pk)
  dictionary = {'obj': quiz}
  return render(request, 'quizes/quiz.html', dictionary)


def quiz_data_view(request,pk):
  quiz = Quiz.objects.get(pk = pk)
  questions = []
  for q in quiz.get_questions():
    answers = []
    for a in q.get_answers():
      answers.append(a.text)

    questions.append({str(q): answers})

  return JsonResponse({
    'data': questions,
    'time': quiz.time,
    'topic': quiz.topic,

  })


def save_quiz_view(request, pk):
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        topic = data_.pop('topic')
        topic = ' '.join(map(str, topic))
        data_.pop('csrfmiddlewaretoken')
        user = request.user
        resultuser = userResult.objects.filter(user = user)
        # if resultuser != 0:
        #   print("already given test")
        # else:
        for i in data_:
          save = userResult()
          save.question = i
          answer_user = data_[i]
          if answer_user == ['']:
            answer_user = 0
          else:
            answer_user = answer_user[0]
          save.answer = answer_user

          save.user = request.user
          save.topic = topic
          save.save()
        for k in data_.keys():
            question = Question.objects.get(text=k)
            #print('here q: ', question, 'here k:', k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})
            
        score_ = score * multiplier
        date1 =  datetime.datetime.now().strftime(' %Y-%m-%d %H:%M:%S')
        Result.objects.create(quiz=quiz, user=user, score=score_,date1 = date1)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})

def userShowResult(request):
  user = request.user
  result = Result.objects.filter(user = user)
  topics = []
  score = []
  numberlist = []
  date = []

  for index, i in enumerate(reversed(result)):
    topics.append(i.quiz)
    scoreRound = round(i.score, 2)
    score.append(scoreRound)
    date.append(i.date1)
    numberlist.append(index+1)
  context = {
    'user': user,
    'result': result,
    'topics': topics,
    'score': score,
    'date':date,
    'numberlist':numberlist,
  }
  return render(request,'result.html',context)
  
def userShowResultS(request):
  user = request.user
  result = Result.objects.filter(user = user)
  topics = []
  score = []
  for index, i in enumerate(result):
    topics.append(i.quiz)
    score.append(i.score)
    print(i.date)
  context = {
    'user': user,
    'result': result,
    'topics': topics,
    'score': score,
  }
  return render(request,'resultS.html',context)
 








