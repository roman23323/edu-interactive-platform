from django.http import JsonResponse
from django.views import View
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid

from .models import Quiz, QuizQuestion, TournamentTable
from .services import QuizEngineService
from .quiz_session import QuizSession
from .forms import GuestUserForm, QuizCreateForm, QuizQuestionForm
from config.decorators import non_guest_required
from config.giga_chat_generator import generate_quiz_from_gigachat
from .services import create_quiz_from_data


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


class QuizCreateView(LoginRequiredMixin, View):

    @non_guest_required
    def get(self, request):
        form = QuizCreateForm()

        return render(request, 'quizzes/create_quiz.html', {
            'form': form
        })

    @non_guest_required
    def post(self, request):
        form = QuizCreateForm(request.POST)

        if not form.is_valid():
            return render(request, 'quizzes/create_quiz.html', {
                'form': form
            })

        quiz = form.save(commit=False)
        quiz.author = request.user
        quiz.save()

        return redirect('quiz_add_questions', quiz.id)


class QuizAddQuestionsView(LoginRequiredMixin, View):

    @non_guest_required
    def get(self, request, quiz_id):
        form = QuizQuestionForm()

        quiz = Quiz.objects.get(id=quiz_id)

        questions = quiz.questions.all()

        return render(request, 'quizzes/add_questions.html', {
            'form': form,
            'quiz': quiz,
            'questions': questions
        })

    @non_guest_required
    def post(self, request, quiz_id):
        form = QuizQuestionForm(request.POST)

        quiz = Quiz.objects.get(id=quiz_id)

        if not form.is_valid():
            questions = quiz.questions.all()

            return render(request, 'quizzes/add_questions.html', {
                'form': form,
                'quiz': quiz,
                'questions': questions
            })

        question = form.save(commit=False)
        question.quiz = quiz

        raw_options = request.POST.get('other_options', '')

        options = [
            option.strip()
            for option in raw_options.split(',')
            if option.strip()
        ]

        if question.right_answer not in options:
            options.append(question.right_answer)

        question.other_options = options

        question.save()

        return redirect('quiz_add_questions', quiz.id)


@non_guest_required
def generate_quiz(request):
    if request.method == "POST":
        topic = request.POST.get("topic")

        data = generate_quiz_from_gigachat(topic)
        quiz = create_quiz_from_data(request.user, data)

        return redirect("quiz_detail", quiz_id=quiz.id)

    return render(request, "quizzes/generate.html")