# Napkin Tools: Lkeep (Links Keeper)

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/proDreams/lkeep/lint.yaml)
[![Код на салфетке](https://img.shields.io/badge/Telegram-Код_на_салфетке-blue)](https://t.me/press_any_button)
[![Заметки на салфетке](https://img.shields.io/badge/Telegram-Заметки_на_салфетке-blue)](https://t.me/writeanynotes)
[![Кот на салфетке чат](https://img.shields.io/badge/Telegram-Кот_на_салфетке_чат-blue)](https://t.me/+Li2vbxfWo0Q4ZDk6)

Lkeep — сервис сокращения ссылок, написанный на Python с использованием современных технологий, таких как FastAPI,
PostgreSQL, Poetry, Pydantic и других.

Проект находится в процессе разработки. Следить за ходом можно:

- На сайте [Код на салфетке](https://pressanybutton.ru/category/servis-na-fastapi/)
- В Telegram-канале [Код на салфетке](https://t.me/press_any_button)

## Технологии

- **FastAPI** — для построения высокопроизводительных API.
- **PostgreSQL** — реляционная база данных для хранения данных.
- **asyncpg** — асинхронная библиотека для подключения к PostgreSQL.
- **SQLAlchemy** — ORM для работы с базой данных.
- **Poetry** — инструмент для управления зависимостями и виртуальными окружениями.
- **Pydantic** — для валидации данных и работы с моделями.
- **pre-commit** — инструмент для автоматической проверки кода перед коммитом.
- **CI Workflow** — автоматизация тестирования приложения.
- **uvicorn** — высокопроизводительный ASGI-сервер для обработки HTTP-запросов.
- **pydantic-settings** — библиотека для работы с конфигурациями и переменными окружения с использованием Pydantic.
- **passlib** — библиотека для безопасного хеширования паролей и других данных.
- **celery** — распределённая система для выполнения фоновых задач и управления очередями, позволяющая выполнять задачи
  асинхронно.
- **redis** — высокопроизводительное in-memory хранилище, используемое для кэширования данных и как брокер сообщений для
  Celery.
- **itsdangerous** — библиотека для безопасного создания и проверки подписанных данных, что помогает защитить токены и
  другую чувствительную информацию.
- **smtplib** — стандартный модуль Python для отправки электронной почты через протокол SMTP.
- **jinja2** — современный и гибкий шаблонизатор, который позволяет динамически генерировать HTML и другие текстовые
  форматы.
- **pyJWT** — библиотека для создания, подписи и верификации JSON Web Tokens (JWT). Используется для генерации токенов
  доступа, проверки их
  целостности, срока действия и подписи, а также работы с закодированными данными (payload) в соответствии со
  стандартами JWT.

## Репозитории

- [GitHub](https://github.com/proDreams/lkeep) — основной репозиторий проекта.
- [GIT на салфетке](https://git.pressanybutton.ru/proDream/lkeep) — зеркальная копия репозитория на Gitea.

## Ссылки на статьи

Я пишу подробные статьи для новичков о процессе создания этого проекта. Ознакомьтесь с ними
на [Код на салфетке](https://pressanybutton.ru/category/servis-na-fastapi/):

1. [FastAPI 1. Инициализация проекта](https://pressanybutton.ru/post/servis-na-fastapi/fastapi-1-inicializaciya-proekta/)
2. [FastAPI 2. Подготовка проекта](https://pressanybutton.ru/post/servis-na-fastapi/fastapi-2-podgotovka-proekta/)
3. [FastAPI 3. Подключение к SQLAlchemy и генератор сессий](https://pressanybutton.ru/post/servis-na-fastapi/fastapi-3-podklyuchenie-k-sqlalchemy-i-generator-s/)
4. [FastAPI 4. Модель пользователя, миксины и Alembic](https://pressanybutton.ru/post/servis-na-fastapi/fastapi-4-model-polzovatelya-i-alembic/)
5. [FastAPI 5. Приложение аутентификации и Pydantic схемы](https://pressanybutton.ru/post/servis-na-fastapi/fastapi-5-prilozhenie-autentifikacii-i-pydantic-sh/)
6. [FastAPI 6. Пользовательский сервис и маршруты регистрации](https://pressanybutton.ru/post/servis-na-fastapi/fastapi-6-polzovatelskij-servis-i-marshruty-regist/)
7. [FastAPI 7. Электронная почта, подтверждение регистрации, Celery и Redis](https://pressanybutton.ru/post/servis-na-fastapi/fastapi-7-elektronnaya-pochta-podtverzhdenie-registracii-celery-i-redis/)
8. [FastAPI 8. Маршрут авторизации и JWT](https://pressanybutton.ru/post/servis-na-fastapi/fastapi-8-marshrut-avtorizacii-i-jwt/)
9. [FastAPI 9. Logout и проверка авторизации](https://pressanybutton.ru/post/servis-na-fastapi/fastapi-9-logout-i-proverka-avtorizacii/)
10. [FastAPI 10. Изменение данных пользователя]()

## Установка

Для установки и запуска проекта на вашем локальном компьютере выполните следующие шаги.

1. **Клонируйте репозиторий:**

   Для этого используйте команду `git clone`. Это создаст локальную копию проекта на вашем компьютере.

   Если вы используете GitHub:
   ```bash
   git clone https://github.com/proDreams/lkeep.git
   ```

   Или если предпочитаете Gitea:
   ```bash
   git clone https://git.pressanybutton.ru/proDream/lkeep.git
   ```

2. **Установите зависимости:**

   Для управления зависимостями в проекте используется Poetry. После клонирования репозитория, перейдите в папку с
   проектом и установите все необходимые пакеты:

   ```bash
   cd lkeep
   poetry install
   ```

   Poetry автоматически установит все библиотеки, указанные в файле `pyproject.toml`.

3. **Настройте переменные окружения:**

   В корне проекта находится файл `.env.example`. Скопируйте его и переименуйте в `.env`. В нем хранятся настройки для
   подключения к базе данных и другие параметры конфигурации.

   Пример команды:
   ```bash
   cp .env.example .env
   ```

   Затем откройте файл `.env` и заполните его значениями, соответствующими вашей системе (например, настройки
   подключения к базе данных PostgreSQL).

4. **Запустите БД и Redis**

    Для запуска контейнера с PostgreSQL и Redis используйте команду в терминале:
    ```bash
    docker compose up -d
    ```

5. **Запустите приложение:**

   Для запуска сервера в режиме разработки используйте команду с Poetry:
   ```bash
   poetry run app
   ```

   Это запустит приложение на локальном сервере, доступном по адресу `http://127.0.0.1:8000`.

## Автор

Проект разработан Иваном Ашихминым.
Для связи используйте [Telegram](https://t.me/proDreams).

Проект создается в рамках сайта **["Код на салфетке"](https://pressanybutton.ru/)**, где публикуются статьи и обучающие
материалы по разработке.
