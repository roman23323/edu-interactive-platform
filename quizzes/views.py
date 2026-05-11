from django.http import JsonResponse
from django.views import View
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, get_user_model
import uuid

from .models import Quiz, QuizQuestion, TournamentTable
from .services import QuizEngineService
from .quiz_session import QuizSession
from .forms import GuestUserForm


User = get_user_model()
service = QuizEngineService()


class StartQuizView(View):
    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)

        service = QuizEngineService()
        session = service.start_quiz(
            quiz,
            request.user if request.user.is_authenticated else None
        )

        request.session['quiz'] = session.__dict__

        return redirect('quiz_question')


class QuizQuestionView(View):
    def get(self, request):
        data = request.session.get('quiz')

        if not data:
            return redirect('/')

        session = QuizSession(**data)

        service = QuizEngineService()
        question = service.get_question(session)

        if question is None:
            return redirect('quiz_result')

        request.session['quiz'] = session.__dict__

        return render(request, 'quizzes/quiz_question.html', {
            'question': question
        })


@method_decorator(csrf_exempt, name='dispatch')
class AnswerView(View):
    def post(self, request, question_id):
        data = request.session.get('quiz')
        session = QuizSession(**data)

        answer = request.POST.get('answer')

        service = QuizEngineService()
        updated = service.submit_answer(session, question_id, answer)

        request.session['quiz'] = updated.__dict__

        return redirect('quiz_question')


class QuizResultView(View):
    def get(self, request):
        data = request.session.get('quiz')

        if not data:
            return redirect('/')

        session = QuizSession(**data)

        return render(request, 'quizzes/quiz_result.html', {
            'quiz_id': session.quiz_id,
            'score': session.score
        })


class QuizDetailView(View):
    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)

        leaderboard = None

        if quiz.tournament:
            table = TournamentTable.objects.filter(quiz=quiz).first()

            if table:
                leaderboard = table.rows.order_by('-points')

        return render(request, 'quizzes/quiz_detail.html', {
            'quiz': quiz,
            'leaderboard': leaderboard
        })


class CreateGuestUserView(View):
    def post(self, request, quiz_id):
        form = GuestUserForm(request.POST)

        if not form.is_valid():
            return redirect('quiz_detail', quiz_id=quiz_id)

        name = f"Гость {form.cleaned_data['name']}_{uuid.uuid4().hex[:8]}"

        user = User.objects.create(
            username=name,
            is_guest=True
        )

        user.set_unusable_password()
        user.save()

        login(request, user)

        return redirect('quiz_start', quiz_id=quiz_id)