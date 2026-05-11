from django.db import models
from django.conf import settings


class Quiz(models.Model):
    TYPE_CHOICES = [
        ('single', 'Single'),
        ('multi', 'Multi'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=100, null=True, blank=True)
    seconds_for_answer = models.IntegerField(default=30)
    life_system = models.BooleanField(default=False)
    tournament = models.BooleanField(default=False)

    def __str__(self):
        return f"Quiz {self.id}"


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    other_options = models.JSONField(null=True, blank=True)
    right_answer = models.TextField()

    points = models.IntegerField(null=True, blank=True)

    def get_points(self):
        return self.points if self.points is not None else 1


class TournamentTable(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='tables')
    created_at = models.DateTimeField(auto_now_add=True)


class TableUser(models.Model):
    table = models.ForeignKey(TournamentTable, on_delete=models.CASCADE, related_name='rows')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    guest_name = models.CharField(max_length=100, null=True, blank=True)
    points = models.IntegerField(default=0)