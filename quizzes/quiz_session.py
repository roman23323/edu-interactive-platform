from dataclasses import dataclass


@dataclass
class QuizSession:
    quiz_id: int
    user_id: int | None

    current_index: int = 0
    score: int = 0
    lives: int = 3

    started_at: float = None
    question_started_at: float = None

    finished: bool = False