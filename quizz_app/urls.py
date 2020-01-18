from django.contrib import admin
from django.urls import path, include
from quizz_app import views
from django.conf import settings
from django.conf.urls.static import static
#template tag
app_name = 'quizz_app'

urlpatterns = [
    path('quiz_selection/<int:quiz_id>', views.quiz_selection, name='quiz_selection'),
    path('update_results/<int:quiz_id>', views.update_results, name='update_results'),
    path('show_stats', views.show_stats, name='show_stats'),

]
