from django.shortcuts import render

from quizzes.models import Quiz
from cards.models import CardCollection


def home(request):
    recent_quizzes = Quiz.objects.order_by('-id')[:5]
    recent_collections = CardCollection.objects.order_by('-id')[:5]

    return render(
        request,
        'home.html',
        {
            'recent_quizzes': recent_quizzes,
            'recent_collections': recent_collections,
        }
    )