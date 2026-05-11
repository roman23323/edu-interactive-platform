import json
from gigachat import GigaChat

from django.conf import settings



giga = GigaChat(
    credentials=settings.GIGACHAT_API_KEY,
    scope='GIGACHAT_API_PERS',
    model='GigaChat-2',
)


def generate_quiz_from_gigachat(topic: str) -> dict:
    
    prompt = f"""
    Сгенерируй вопросы для викторины в формате JSON.

    Описание: {topic}

    Требования:
    - В качестве ответа возвращай ТОЛЬКО валидный JSON (твой ответ будет парситься как JSON)
    - Никаких дополнительных текстов - только JSON в ответе
    - Никаких дополнительных знаков, в том числе никакой markdown-разметки
    - Для каждого вопроса: 4 варината ответа, один из правильных

    Формат выходного JSON:
    {{
      "title": "Тема",
      "questions": [
        {{
          "text": "Вопрос",
          "other_options": ["Вариант1", "Вариант2", "Вариант3", "Вариант4"],
          "right_answer": "Вариант3"
        }}
      ]
    }}
    """
    response = giga.chat(prompt)

    content = response.choices[0].message.content
    if content.startswith('json'):
        content = content[7:-3]

    return json.loads(content)