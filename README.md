Для запуска локально:


1. Заполнить .env по .env.example: указать данные подключения к БД и ключ GigaChat API (https://developers.sber.ru/docs/ru/gigachat/individuals-quickstart)
2. Создать и активировать виртуальное окружение:

   Linux/MacOS:
     > python3 -m venv venv
     
     > source venv/bin/activate

   Windows:

     > python -m venv venv

     > venv\Scripts\activate.bat
3. Установить в окружение сертификат Минцифры:
     > curl -k "https://gu-st.ru/content/lending/russian_trusted_root_ca_pem.crt" -w "\n" >> $(python -m certifi)
     
     (https://developers.sber.ru/docs/ru/gigachat/certificates)
4. Поднять сервис db из docker-compose.yml: docker compose up
5. Применить миграции:

   Linux/MacOS:

     > python3 manage.py migrate

   Windows:

     > python manage.py migrate
6. Запустить сервер:

   Linux/MacOS:

     > python3 manage.py runserver

   Windows:

     > python manage.py runserver

Сайт запустится по адресу localhost:8000
