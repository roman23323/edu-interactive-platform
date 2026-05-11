from django import forms

from .models import Quiz, QuizQuestion


class GuestUserForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Your name'
    )


class QuizCreateForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = [
            'type',
            'seconds_for_answer',
            'life_system',
            'tournament'
        ]


class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = [
            'text',
            'right_answer',
            'points'
        ]