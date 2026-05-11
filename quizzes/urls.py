from django.urls import path
from .views import (
    QuizDetailView,
    StartQuizView,
    QuizQuestionView,
    AnswerView,
    QuizResultView,
    CreateGuestUserView
)

urlpatterns = [
    path('quiz/<int:quiz_id>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('quiz/<int:quiz_id>/start/', StartQuizView.as_view(), name='quiz_start'),
    path(
        'quiz/<int:quiz_id>/guest/',
        CreateGuestUserView.as_view(),
        name='quiz_guest'
    ),
    path('quiz/question/', QuizQuestionView.as_view(), name='quiz_question'),
    path('quiz/answer/<int:question_id>/', AnswerView.as_view(), name='quiz_answer'),
    path('quiz/result/', QuizResultView.as_view(), name='quiz_result'),
]