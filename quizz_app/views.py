from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect

import json
import csv

from .model.test import Test, TestUser
from .model.question import Question, QuestionUser
from .model.answer import Answer

from .forms import ImportForm
from . import forms


@login_required
def index(request):
    ''' main view'''
    import_form = forms.ImportForm()
    if request.method == 'POST' :
        import_form = forms.ImportForm(request.POST)
        file = request.FILES['file']
        if (file.name).endswith('.csv'):
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            try:
                the_test = list(reader)
                print(the_test)
                print("..")
            except:
                pass
        return redirect('index')

    else:
        try:
            ordered_tests = {}
            available_tests = Test.objects.all().values('id',
                                                        'test_category',
                                                        'test_name',
                                                        'test_description',).order_by('-test_name')

            for test in available_tests:
                if test['test_category'] in ordered_tests:
                    ordered_tests[test['test_category']].append(test)
                else:
                    ordered_tests[test['test_category']] = []
                    ordered_tests[test['test_category']].append(test)

            json_available_tests = json.dumps(ordered_tests)

            #available_tests = serialize('json', Test.objects.all())

        except Test.DoesNotExist:
            print("NO TESTS")
            available_tests = {}

        return render(request, 'quizz_app/home.html',
                      {'available_tests': json_available_tests,
                       'import_form': import_form,
                       })


@login_required
def test_selection(request, test_id):

    try:
        test = Test.objects.get(id=test_id)


    except Test.DoesNotExist:
        test.test_name = "ERROR CARGANDO TEST"

    if request.method == "POST":
        max_questions = int(request.POST.get('num_questions', ''))

        test_questions = Question.objects.filter(question_test=test_id).values('id', 'question_text').order_by("?")[0:max_questions]
        full_test = {}
        result_list = {}
        num_questions = len(test_questions)
        for question in test_questions:
            full_test[question['id']] = {'question': question['question_text'],
                                         'answers': {}}


            test_answers = Answer.objects.filter(answer_question_id=question['id']).values('id',
                                                                                           'answer_question',
                                                                                           'answer_text',
                                                                                           'correct_answer',)
            for answer in test_answers:

                if answer['correct_answer']:
                    if question['id'] in result_list:
                        result_list[question['id']].append(answer['id'])
                    else:
                        result_list[question['id']] = [answer['id'],]
                full_test[question['id']]['answers'].update({answer['id']: answer['answer_text']})

        result_list = json.dumps(result_list)
        return render(request, 'quizz_app/test_page.html', {'test': test,
                                                            'full_test': full_test,
                                                            'result_list': result_list,
                                                            'num_questions': num_questions,
                                                            })
    else:
        total_questions = Question.objects.filter(question_test=test_id).values('id').count()
        return render(request, 'quizz_app/test_selection.html', {'test': test,

                                                                 'total_questions': total_questions,
                                                                 })


@login_required
def update_results(request, test_id):
    if request.method == "POST":

        grade = json.loads(request.POST.get('grade', None))
        print(grade)
        results = json.loads(request.POST.get('results', None))
        print(results['1'])

        te = Test.objects.get(id=test_id)
        try:
            test = TestUser.objects.get(test_test_id=test_id, test_user=request.user)

        except TestUser.DoesNotExist:
           test = TestUser.objects.create(test_test=te, test_user=request.user)
        if int(grade) > 50:
            test.test_ok += 1
        else:
            test.test_fails += 1
        test.save()

        questions = Question.objects.filter(question_test=te)
        for question in questions:
            try:
                que = QuestionUser.objects.get(question_question=question, question_user=request.user)
            except QuestionUser.DoesNotExist:
                que = QuestionUser.objects.create(question_question=question, question_user=request.user)

            if results[str(question.id)] == 0:
                que.question_fails += 1
                print("FAIL")
            else:
                que.question_ok += 1
            que.save()
        return HttpResponse()
    else:
        return  HttpResponse()


@login_required
def import_test(request, **kwargs):
    pass