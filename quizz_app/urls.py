from django.contrib import admin
from django.urls import path, include
from  quizz_app import views
from django.conf import settings
from django.conf.urls.static import static
#template tag
app_name = 'quizz_app'

urlpatterns = [
    path('test_selection/<int:test_id>', views.test_selection, name='test_selection'),
    path('update_results/<int:test_id>', views.update_results, name='update_results'),
]
