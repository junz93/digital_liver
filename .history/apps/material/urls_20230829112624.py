from django.urls import path
from rest_framework.authtoken import views as auth_views

from . import views


urlpatterns = [
    path('character/all', views.get_all_characters, name='get_all_characters'),
    path('character/<int:id>', views.get_character, name='get_character'),
    path('character/create', views.create_character, name='create_character'),
    path('character/<int:id>/update', views.update_character, name='update_character'),
    path('character/<int:id>/delete', views.delete_character, name='delete_character'),
    path('question/all', views.get_all_questions_in_library, name='get_all_questions_in_library'),
    path('question/<int:id>', views.get_question, name='get_question'),
    path('question/create', views.create_question, name='create_question'),
    path('question/<int:id>/delete', views.delete_question, name='delete_question'),
    path('speech/all', views.get_all_speeches_in_library, name='get_all_speeches_in_library'),
    path('speech/<int:id>', views.get_speech, name='get_speech'),
    path('speech/create', views.create_speech, name='create_speech'),
    path('speech/<int:id>/delete', views.delete_speech, name='delete_speech'),
    path('library/question/all', views.get_all_question_libraries, name='get_all_question_libraries'),
    path('library/question/create', views.create_question_library, name='create_question_library'),
    path('library/speech/all', views.get_all_speech_libraries, name='get_all_speech_libraries'),
    path('library/speech/create', views.create_speech_library, name='create_speech_library')
]