from django.utils import timezone
from .models import Quiz, QuizQuestion, TableUser, TournamentTable
from .quiz_session import QuizSession


class QuizEngineService:

    def start_quiz(self, quiz: Quiz, user=None):
        session = QuizSession(
            quiz_id=quiz.id,
            user_id=user.id if user else None,
            lives=3 if quiz.life_system else 999,
            started_at=timezone.now().timestamp(),
            question_started_at=timezone.now().timestamp(),
        )
        return session


    def get_question(self, session: QuizSession):
        questions = QuizQuestion.objects.filter(quiz_id=session.quiz_id).order_by('id')

        if session.current_index >= len(questions):
            return None

        return questions[session.current_index]


    def submit_answer(self, session: QuizSession, question_id: int, answer: str):
        question = QuizQuestion.objects.get(id=question_id)
        quiz = Quiz.objects.get(id=session.quiz_id)

        elapsed = timezone.now().timestamp() - session.question_started_at

        if quiz.seconds_for_answer:
            if elapsed > quiz.seconds_for_answer:
                correct = False
            else:
                correct = (answer == question.right_answer)
        else:
            correct = (answer == question.right_answer)

        # начисление баллов
        if correct:
            session.score += question.get_points()
        else:
            if quiz.life_system:
                session.lives -= 1

        # конец по жизням
        if session.lives <= 0:
            return self.finish(session)

        # переход к следующему вопросу
        session.current_index += 1

        questions_count = QuizQuestion.objects.filter(
            quiz_id=session.quiz_id
        ).count()

        # конец по вопросам
        if session.current_index >= questions_count:
            return self.finish(session)

        session.question_started_at = timezone.now().timestamp()

        return session


    def finish(self, session: QuizSession):
        quiz = Quiz.objects.get(id=session.quiz_id)

        if quiz.tournament:
            table, _ = TournamentTable.objects.get_or_create(quiz=quiz)

            TableUser.objects.create(
                table=table,
                user_id=session.user_id,
                points=session.score
            )

        session.finished = True
        return session


def create_quiz_from_data(user, data: dict) -> Quiz:
    quiz = Quiz.objects.create(
        author=user,
        title=data.get("title", "Generated Quiz"),
    )


    for q in data["questions"]:
        QuizQuestion.objects.create(
            quiz=quiz,
            text=q["text"],
            right_answer=q["right_answer"],
            other_options=q["other_options"],
        )

    return quiz