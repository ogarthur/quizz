from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.db.models import F

import json
import csv

from .model.quiz import Quiz, QuizUser, CategoryQuiz
from .model.question import Question, QuestionUser
from .model.answer import Answer


from .forms import ImportForm
from . import forms


@login_required
def index(request):
    """
    main view
    """
    import_form = forms.ImportForm()
    if request.method == 'POST':
        import_form = forms.ImportForm(request.POST)
        file = request.FILES['file']
        if file.name.endswith('.csv'):
            #decoded_file = file.read().decode('utf-8').splitlines().encode('UTF-8')
            decoded_file = file.read().decode('UTF-8').splitlines()

            reader = csv.reader(decoded_file)
            try:
                the_quiz = list(reader)

                if len(the_quiz[0]) >= 3:
                    print("DESCRIPTION")
                    n_desc = the_quiz[0][2]
                else:
                    print(" NO DESCRIPTION")
                    n_desc = ""

                is_random = False
                if len(the_quiz[0]) >= 4:
                    if the_quiz[0][3] == "1":
                        is_random = True
                print(is_random)
                n_quiz = Quiz.objects.create(quiz_name=the_quiz[0][1],
                                              quiz_category=the_quiz[0][0],
                                              quiz_description=n_desc,
                                              quiz_randomizable=is_random)
                n_quiz.save()
                print("S")
                bulk_questions = []
                bulk_answers = []
                for question in range(1, len(the_quiz)):
                    print(question)
                    n_question = Question()
                    n_question.question_text = the_quiz[question][0]
                    n_question.question_quiz = n_quiz
                    bulk_questions.append(n_question)
                Question.objects.bulk_create(bulk_questions)
                new_questions = Question.objects.filter(question_quiz=n_quiz)
                n_q = -1
                for question in range(1, len(the_quiz)):
                    n_q += 1
                    print("INSERTED QUESTION", )
                    for answer in range(1, len(the_quiz[question])):
                        print("1    =========>", the_quiz[question][answer])
                        if the_quiz[question][answer] != '0' and the_quiz[question][answer] != '1' and the_quiz[question][answer] != "":
                            print("==========>", the_quiz[question][answer] )
                            n_answer = Answer()
                            n_answer.answer_text = the_quiz[question][answer]
                            n_answer.correct_answer = the_quiz[question][answer+1]
                            n_answer.answer_question = new_questions[n_q]
                            bulk_answers.append(n_answer)

                        else:
                            continue
                Answer.objects.bulk_create(bulk_answers)
            except:
                pass
        return redirect('index')

    else:
        try:
            ordered_quizs = {}
            available_quizs = Quiz.objects.all().values('id',
                                                        'quiz_category',
                                                        'quiz_name',
                                                        'quiz_description', ).order_by('-quiz_name')

            for quiz in available_quizs:
                if quiz['quiz_category'] in ordered_quizs:
                    ordered_quizs[quiz['quiz_category']].append(quiz)
                else:
                    ordered_quizs[quiz['quiz_category']] = []
                    #ordered_quizs[quiz['quiz_category']] = quiz.quiz_category

                    ordered_quizs[quiz['quiz_category']].append(quiz)

            json_available_quizs = json.dumps(ordered_quizs)

        except Quiz.DoesNotExist:
            print("NO quizS")
            available_quizs = {}

        return render(request, 'quizz_app/home.html',
                      {'available_quizs': json_available_quizs,
                       'import_form': import_form,
                       })


@login_required
def quiz_selection(request, quiz_id):

    try:
        quiz = Quiz.objects.get(id=quiz_id)

    except Quiz.DoesNotExist:
        quiz.quiz_name = "ERROR CARGANDO quiz"

    if request.method == "POST":
        max_questions = int(request.POST.get('num_questions', ''))
        if quiz.quiz_randomizable:
            quiz_questions = Question.objects.filter(question_quiz=quiz_id).values('id', 'question_text').order_by("?")[0:max_questions]
        else:
            quiz_questions = Question.objects.filter(question_quiz=quiz_id).values('id', 'question_text')[0:max_questions]

        full_quiz = {}
        result_list = {}
        num_questions = len(quiz_questions)
        for question in quiz_questions:
            full_quiz[question['id']] = {'question': question['question_text'],
                                         'answers': {}}
            quiz_answers = Answer.objects.filter(answer_question_id=question['id']).values('id',
                                                                                           'answer_question',
                                                                                           'answer_text',
                                                                                           'correct_answer',)
            for answer in quiz_answers:
                if answer['correct_answer']:
                    if question['id'] in result_list:
                        result_list[question['id']].append(answer['id'])
                    else:
                        result_list[question['id']] = [answer['id'],]
                full_quiz[question['id']]['answers'].update({answer['id']: answer['answer_text']})
        result_list = json.dumps(result_list)
        return render(request, 'quizz_app/quiz_page.html', {'quiz': quiz,
                                                            'full_quiz': full_quiz,
                                                            'result_list': result_list,
                                                            'num_questions': num_questions,
                                                            })
    else:
        total_questions = Question.objects.filter(question_quiz=quiz_id).values('id').count()
        return render(request, 'quizz_app/quiz_selection.html', {'quiz': quiz,

                                                                 'total_questions': total_questions,
                                                                 })


@login_required
def update_results(request, quiz_id):

    if request.method == "POST":
        grade = json.loads(request.POST.get('grade', None))
        results = json.loads(request.POST.get('results', None))
        quiz = Quiz.objects.get(id=quiz_id)

        try:
            quiz_user = QuizUser.objects.get(quiz_quiz_id=quiz_id, quiz_user=request.user)

        except QuizUser.DoesNotExist:
            quiz_user = QuizUser.objects.create(quiz_quiz=quiz, quiz_user=request.user)
        quiz_user.quiz_attempts += 1

        if quiz_user.quiz_avg_result == 0:
            quiz_user.quiz_avg_result = grade
        else:
            quiz_user.quiz_avg_result = (quiz_user.quiz_avg_result + grade)/2
        quiz_user.save()

        for result in results:
            n_question = Question.objects.get(id=result)

            if results[result] == 0:
                fail = 1
                hit = 0
            else:
                fail = 0
                hit = 1
            try:
                question_user = QuestionUser.objects.get(question_question=n_question, question_user=request.user)
            except QuestionUser.DoesNotExist:
                question_user = QuestionUser.objects.create(question_question=n_question, question_user=request.user)
            question_user.question_fails = question_user.question_fails + fail
            question_user.question_hits = question_user.question_hits + hit
            question_user.save()

        '''
        questions = Question.objects.filter(question_quiz=te)
       
        for question in questions:
            try:
                que = QuestionUser.objects.get(question_question=question, question_user=request.user)
            except QuestionUser.DoesNotExist:
                que = QuestionUser.objects.create(question_question=question, question_user=request.user)
            print(str(question.id))
            if str(question.id) not in results:
                continue
            else:
                if results[str(question.id)] == 0:
                    que.question_fails += 1
                    print("FAIL")
                else:
                    que.question_ok += 1
                que.save()
        '''
        return HttpResponse()
    else:
        return HttpResponse()


@login_required
def import_quiz(request, **kwargs):
    pass