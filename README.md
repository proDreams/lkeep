# Napkin Tools: Lkeep (Links Keeper)

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

4. **Запустите приложение:**

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
