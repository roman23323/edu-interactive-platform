from django.urls import path
from .views import (
    QuizDetailView,
    StartQuizView,
    QuizQuestionView,
    AnswerView,
    QuizResultView,
    CreateGuestUserView,
    QuizAddQuestionsView,
    QuizCreateView,
    generate_quiz
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
    path(
        'quiz/create/',
        QuizCreateView.as_view(),
        name='quiz_create'
    ),
    path(
        'quiz/<int:quiz_id>/questions/',
        QuizAddQuestionsView.as_view(),
        name='quiz_add_questions'
    ),
    path(
        "quiz/generate/",
        generate_quiz,
        name="quiz_generate",
    ),
]