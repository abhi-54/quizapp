from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import render
from payment.models import quizAccessTable
from django.contrib.admin.views.decorators import staff_member_required
from regester.models import profile1
from .models import Quiz,Subjects1
from django.views.generic import ListView
from django.http import JsonResponse, request
from questions.models import Answer, Question
from results.models import Result
import datetime
from django.contrib.auth.decorators import login_required


# Create your views here.

# custom error 404 page (works only when DEBUG = False)
def error404_view(request, exception):
    return render(request, '404.html', status=404)

# for displaying all the links associated with website
@staff_member_required
def all_links_view(request):
    return render(request, 'all_links.html')

@login_required
def SubjectView(request):
    user = request.user
    profile = profile1.objects.filter(user=user)
    l = profile[0]
    std = l.std
    #print('std', std)
    print(request.user)
    subjectslist = []
    try:
        quizAccess = quizAccessTable.objects.get(user = request.user)
        subjects = quizAccess.subjects.split(', ')
        for sub in subjects:
            if sub == None or sub == '':
                subjects.remove(sub)
        # print(type(subjects), subjects)
    except:
        return render(request, 'showWarning.html') 
    # print(quizAccess)
    sub = Subjects1.objects.filter(std = std)
    # i = Subjects1.objects.get(pk = sub)
    # print("id: ",i)
    allowedSub = []
    for j in sub:
        for d in subjects:
            if str(j) == d:
                print("OK",type(j))
                allowedSub.append(j)
    notAllowedSub = []
    for i in list(sub):
        if i in allowedSub:
            pass
        else:
            notAllowedSub.append(i)
    """""
    username: usertoday
    pass: S7WckwaWD_KTgQ.
    """
    context = {
        "sub":sub,
        "allowedSub":allowedSub,
        "notAllowedSub": notAllowedSub,
    }
    return render(request,'subjects.html',context)

# similar to quiz view
@login_required
def showSub(request,pk):
    quiz = Quiz.objects.filter(subject = pk)
    context = {
        "quiz": quiz,
    }
    return render(request,'showsub.html',context)

  
@login_required
def home_view(request):
    user = request.user
    profile = profile1.objects.get(user = user)
    standard = f"{user}-{profile.get_std()}"
    #print('home std: ', standard)
    # filtering result model according to user
    result = Result.objects.filter(user=user)   # required for chart display

    details = []
    result_top = Result.objects.filter(std = profile.get_std()) # required for top scorers
    print('--resultTop: ', result_top)
    top_users = []
    top_scores = []
    top_users_quizname = []
    for i in result_top.order_by('-score'):
        if i.user not in top_users:
            print('-user: ', i.user, i.score, i.quiz)
            top_users.append(i.user)
            top_scores.append(i.score)
            top_users_quizname.append(i.quiz)
    for num, i in enumerate(top_users):
        temp = User.objects.filter(username = i)
        for j in temp:
            msg = f"#{num+1} {j.first_name} {j.last_name} ({j.username})"
            #print('j: ', msg)
            details.append(msg)
    #print('users: ', details)
    score = []
    Quizname = []
    count = 0
    for index, i  in enumerate(reversed(result)):
        if count == 10:
            break
        scoreRound = round(i.score, 2)
        score.append(scoreRound)
        Quizname.append(str(i.quiz))
        count = count + 1
    context = {
        'x':score,
        'y':Quizname, 
        'top_scores': top_scores,
        'details': details,
        'top_users_quizname': top_users_quizname,
    }
    return render(request, 'home.html',context=context)
    
class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'

@login_required
def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    dictionary = {'obj': quiz}
    return render(request, 'quizes/quiz.html', dictionary)


def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    #print('here:', quiz.number_of_questions)
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
        # if resultuser != 0:
        #   print("already given test")
        # else:
        #print('data', data)
        for k in data_.keys():
            question = Question.objects.get(text=k)
            
            questions.append(question)
        

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

                results.append(
                    {str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        score_ = score * multiplier
        date1 = datetime.datetime.now().strftime(' %Y-%m-%d %H:%M:%S')
        profile = profile1.objects.get(user = user)
        standard = profile.get_std()
        Result.objects.create(quiz=quiz, user=user, score=score_, date1=date1, std = standard)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})

@login_required
def userShowResult(request):
    user = request.user
    result = Result.objects.filter(user=user)
    topics = []
    score = []
    numberlist = []
    date = []
    Quizname = []

    for index, i in enumerate(reversed(result)):
        topics.append(i.quiz)
        scoreRound = round(i.score, 2)

        score.append(scoreRound)
        date.append(i.date1)
        # print(index+1)
        numberlist.append(index+1)
        Quizname.append(str(i.quiz))

    # for chart.js
    score_chart = []
    Quizname_chart = []
    for n, m  in enumerate(reversed(result)):
        if n == 9:
            break
        scoreRound_chart = round(m.score, 2)
        score_chart.append(scoreRound_chart)
        Quizname_chart.append(str(m.quiz))

    context = {
        'user': user,
        'result': result,
        'topics': topics,
        'score': score,
        'date': date,
        'numberlist': numberlist,
        #'chart': chart,
        'x':score_chart,
        'y':Quizname_chart, 
    }
    return render(request, 'result.html', context)


def chart_view(request):
    user = request.user
    result = Result.objects.filter(user=user)
    score = []
    Quizname = []
    count = 0
    for index, i  in enumerate(reversed(result)):
        if count == 10:
            break
        scoreRound = round(i.score, 2)
        score.append(scoreRound)
        Quizname.append(str(i.quiz))
        count = count + 1

    context = {
        'x':score,
        'y':Quizname, 
    }
    return render(request, 'chart.html', context)

def dashboard_view(request):
    return render(request, 'home.html')

