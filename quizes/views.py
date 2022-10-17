from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from payment.models import quizAccessTable
from django.contrib.admin.views.decorators import staff_member_required
from regester.models import profile1
from .models import Quiz,Subjects1
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Answer, Question
from results.models import Result
import datetime, json
from django.contrib.auth.decorators import login_required
import datetime

class doubleQuote_dict(dict):
    def __str__(self):
        return json.dumps(self)

def get_subjects(username):
    """Returns the subjects' lists associated with the user

    :param username: Username of the user
    :type username: string
    :return: returns list of allowed subjects, class subjects, not allowed subjects and message list
    :rtype: 4 lists
    """
    msg_list, subjects_allowed, std_subjects, not_allowed_subjects = [], [], [], []
    e = datetime.datetime.now()
    day=(e.strftime("%a"))
    username = str(username)
    profile = profile1.objects.get(user = username)
    std = profile.std   # get the 'std' from profile1 table
    std_subjects = list(Subjects1.objects.filter(std = std))
    users_list = [i.user.username for i in quizAccessTable.objects.filter(std = std)]    # create users list for checking if user exits in quizAccessTable
    if day=="Sat" or day=="Sun":
        if username in users_list:
            subjects_allowed = quizAccessTable.objects.get(user = username).subjects.split(', ')    # subjects which are allowed for the user
            subjects_allowed = [s for s in subjects_allowed if s != '']
            if len(std_subjects) != 0:
                subjects_allowed = [subject for subject in std_subjects if subject.__str__() in subjects_allowed]   # as Subjects1 model has to be passed and not just its name
                not_allowed_subjects = [s for s in std_subjects if s not in subjects_allowed]
            else:
                msg_list.append(f"Alert! Subjects are not yet created for class {std}!")
        else:
            msg_list.append("Alert! Subjects are not yet allowed! Please contact Admin!")
    else:
        msg_list.append(f"Please note that quiz is only allowed on Saturday and Sunday!")
    return subjects_allowed, std_subjects, not_allowed_subjects, msg_list

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
    subjects_allowed, std_subjects, not_allowed_subjects, msg_list = get_subjects(user)
    """""
    username: usertoday
    pass: S7WckwaWD_KTgQ.
    """
    context = {
        "sub":std_subjects,
        "allowedSub":subjects_allowed,
        "notAllowedSub": not_allowed_subjects,
        "msg_list": msg_list,
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
    subjects_allowed, std_subjects, not_allowed_subjects, msg_list = get_subjects(user)
    profile = profile1.objects.get(user = user)
    # filtering result model according to user
    result = Result.objects.filter(user=user)   # required for chart display

    details = []
    result_top = Result.objects.filter(std = profile.get_std()) # required for top scorers
    #print('--resultTop: ', result_top)
    top_users = []
    top_scores = []
    top_users_quizname = []
    for i in result_top.order_by('-score'):
        if i.user not in top_users:
            #print('-user: ', i.user, i.score, i.quiz)
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
    for index, i  in enumerate(reversed(result)):
        if index == 10:
            break
        scoreRound = round(i.score, 2)
        score.append(scoreRound)
        Quizname.append(str(i.quiz))
    context = {
        'x':score,
        'y':Quizname, 
        'top_scores': top_scores,
        'details': details,
        'top_users_quizname': top_users_quizname,
        "sub":std_subjects,
        "allowedSub":subjects_allowed,
        "notAllowedSub": not_allowed_subjects,
        "msg_list": msg_list,
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

# request.is_ajax() is now deprecated
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

""" def ajax_test(request):
    if is_ajax(request=request):
        message = "This is ajax"
    else:
        message = "Not ajax"
    return HttpResponse(message) """

def save_quiz_view(request, pk):
    if is_ajax(request=request):
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        topic = data_.pop('topic')
        topic = ' '.join(map(str, topic))
        data_.pop('csrfmiddlewaretoken')
        user = request.user
        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None
        result_details = {}
        for q in questions:
            a_selected = request.POST.get(q.text)
            question_answers = Answer.objects.filter(question=q)
            for a in question_answers:
                if a_selected == a.text:
                    if a.correct:
                        score += 1
                        correct_answer = a.text
                else:
                    if a.correct:
                        correct_answer = a.text
                    if a_selected == "":
                        a_selected = 'Not Answered'
                        continue
            result_details[str(q)] = {'correct_answer': correct_answer, 'answered': a_selected}
            results.append(
                {str(q): {'correct_answer': correct_answer, 'answered': a_selected}})

        score_ = score * multiplier
        date1 = datetime.datetime.now().strftime(' %Y-%m-%d %H:%M:%S')
        profile = profile1.objects.get(user = user)
        standard = profile.get_std()
        result_summary = doubleQuote_dict(result_details)   # as JSON uses double quotes
        Result.objects.create(quiz=quiz, user=user, score=score_, date1=date1, std = standard, result_summary = result_summary)

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
