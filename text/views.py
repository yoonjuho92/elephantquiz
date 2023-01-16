from django.shortcuts import render, redirect
from .models import Text, Question, UserChoice, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserForm, UserProfileForm

def index(request):
    user = request.user
    if not user.is_authenticated and request.method == 'GET':
        return render(request, 'index.html')

    if request.method == 'POST':
        id = request.POST.get('id')
        password = request.POST.get('password')
        user = authenticate(request, username=id, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')

    user = request.user
    userChoiceSet = user.userchoice_set.all()
    userTextSet = []
    for userChoice in userChoiceSet:
        if userChoice.question.text not in userTextSet:
            userTextSet.append(userChoice.question.text)

    for newText in Text.objects.all():
        if newText not in userTextSet:
            text = newText
            context = {'text_id': text.id}
            return render(request, 'index.html', context)
        else:
            pass
    return render(request, 'allClear.html')



def textPage(request, id):
    text = Text.objects.get(pk=id)
    context = {'text_subject' : text.subject,
               'text_content' : text.content,
               'text_id' : text.id}
    return render(request, 'text.html', context)

def quiz(request,id):

    quizes = Question.objects.filter(text__pk = id)
    user = request.user

    # 퀴즈 결과 저장
    if request.method == 'POST':
        chosen = request.POST.get('chosen')
        quiz_id = request.POST.get('quiz_id')
        quiz = Question.objects.get(pk=quiz_id)
        quiz_choices = [quiz.choice1, quiz.choice2, quiz.choice3, quiz.choice4, quiz.choice5]
        if chosen == quiz_choices[quiz.answer-1]:
            correct = True
        else:
            correct = False
        UserChoice.objects.create(
            user = user,
            correct = correct,
            question = quiz,
            choice = chosen
        )

    # 안 푼 퀴즈 찾아서 보여주기
    userChosenList = []
    for quiz in quizes:
        try:
            tmp = user.userchoice_set.get(question = quiz)
            userChosenList.append(quiz)
        except:
            pass

    for quiz in quizes:
        if quiz not in userChosenList:
            context = {'quiz_question': quiz.question,
                       'quiz_choices' : [quiz.choice1, quiz.choice2, quiz.choice3, quiz.choice4, quiz.choice5],
                       'quiz_id' : quiz.id
                       }
            return render(request, 'quiz.html', context)
        pass

    try:
        quiz_id = request.POST.get('quiz_id')
        question = Question.objects.get(pk=quiz_id)
        text = question.text
    except:
        text = Text.objects.get(pk=id)
    quizList = []
    for quiz in quizes:
        userQuestion = quiz.userchoice_set.get(user=user)
        quizList.append((quiz, userQuestion.choice, userQuestion.correct))

    context = {
        'text' : text,
        'quizList' : quizList
    }
    return render(request, 'answer.html', context)

def myPage(request):
    user = request.user
    userChoiceSet = user.userchoice_set.all()
    userTextSet = []
    for userChoice in userChoiceSet:
        if userChoice.question.text not in userTextSet:
            userTextSet.append(userChoice.question.text)

    context = {
        'userTextSet' : userTextSet
    }
    return render(request, 'myPage.html', context)

def register(request):
    if request.method == "POST":
        userForm = UserForm(request.POST)
        userProfileForm = UserProfileForm(request.POST)
        if userForm.is_valid():
            user = userForm.save()
            if userProfileForm.is_valid():
                userProfile = userProfileForm.save(commit=False)
                userProfile.user = user
                userProfile.save()


            username = userForm.cleaned_data.get('username')
            raw_password = userForm.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')

    userForm = UserForm()
    userProfileForm = UserProfileForm()
    context = {
        'userForm' : userForm,
        'userProfileForm' : userProfileForm
    }

    return render(request, 'register.html')



