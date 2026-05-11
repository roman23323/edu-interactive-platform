from django.contrib import admin

from .models import Quiz, QuizQuestion, TournamentTable, TableUser

admin.site.register([Quiz, QuizQuestion, TournamentTable, TableUser])