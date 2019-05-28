from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .model.test import Test
from .model.question import Question
from .model.answer import Answer
from random import shuffle
import json
from django.http import JsonResponse
from django.core.serializers import serialize

@login_required
def index(request):
    try:
        ordered_tests = {}
        available_tests = Test.objects.all().values('id',
                                                    'test_category',
                                                    'test_name',
                                                    'test_description',
                                                    'test_tries',).order_by('-test_name')

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

    return render(request, 'quizz_app/home.html',{'available_tests': json_available_tests,})


def test_selection(request, test_id):

    try:
        test = Test.objects.get(id=test_id)
        ratio = test.test_ratio()

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
                print("==>",answer['id'])
                if answer['correct_answer']:
                    result_list[question['id']] = answer['id']
                full_test[question['id']]['answers'].update({answer['id']: answer['answer_text']})

        result_list=json.dumps(result_list)
        return render(request, 'quizz_app/test_page.html', {'test': test,
                                                            'full_test': full_test,
                                                            'result_list': result_list,
                                                            'num_questions': num_questions,
                                                            })
    else:
        total_questions =Question.objects.filter(question_test=test_id).values('id').count()
        print('-.--',total_questions )
        return render(request, 'quizz_app/test_selection.html', {'test': test,
                                                                 'ratio': ratio,
                                                                 'total_questions': total_questions,
                                                                 })

