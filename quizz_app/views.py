from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect

import json
import csv

from .model.test import Test, TestUser, CATEGORY_CHOICES
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
            decoded_file = file.read().decode('ISO-8859-1').splitlines()
            reader = csv.reader(decoded_file)
            try:
                the_test = list(reader)
                print(the_test)
                print(".s.")
                categories = dict(CATEGORY_CHOICES)
                print(categories)
                print("====")
                print(the_test[0][0])

                if the_test[0][0] in categories.keys():
                    n_category = categories[the_test[0][0]]
                else:
                    n_category = 0

                if len(the_test[0]) >= 3:
                    print("DESCRIPTION")
                    n_desc = the_test[0][2]
                else:
                    print(" NO DESCRIPTION")
                    n_desc = ""

                n_test = Test.objects.create(test_name=the_test[0][1],
                                           test_category=n_category,
                                           test_description=n_desc)
                n_test.save()
                print("==============o==================")
                bulk_questions = []
                bulk_answers = []
                for question in range(1, len(the_test)):
                    print(question)
                    n_question = Question()
                    n_question.question_text = the_test[question][0]
                    n_question.question_test = n_test
                    bulk_questions.append(n_question)
                Question.objects.bulk_create(bulk_questions)
                new_questions = Question.objects.filter(question_test=n_test)
                n_q = -1
                for question in range(1, len(the_test)):
                    n_q+=1
                    print("INSERTED QUESTION", )
                    for answer in range(1, len(the_test[question])):

                        if the_test[question][answer] != '0' and the_test[question][answer] != '1' and the_test[question][answer] != "":
                            n_answer = Answer()
                            n_answer.answer_text = the_test[question][answer]
                            n_answer.correct_answer = the_test[question][answer+1]
                            n_answer.answer_question = new_questions[n_q]
                            bulk_answers.append(n_answer)

                        else:
                            continue
                Answer.objects.bulk_create(bulk_answers)
                print("==============p==================")
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