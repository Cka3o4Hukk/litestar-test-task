# LiteStar Test Task

## Описание проекта

Проект представляет собой REST API для управления пользователями, разработанное в рамках тестового задания. API реализовано на базе фреймворка **LiteStar (версия 2.x)** с использованием **Python 3.12** и базы данных **PostgreSQL**. Поддерживаются CRUD-операции для таблицы `users`, а также Swagger-документация.

### Таблица `user`

- **id** — UUID, первичный ключ, генерируется автоматически с использованием `uuid.uuid4`.
- **name** — строка (до 100 символов), обязательное поле.
- **surname** — строка (до 100 символов), обязательное поле.
- **password** — строка (до 255 символов), обязательное поле.
- **created_at** — дата и время создания с часовым поясом; по умолчанию — текущее время в UTC.
- **updated_at** — дата и время обновления с часовым поясом; по умолчанию — текущее время в UTC, автоматически обновляется при изменении записи.

### Стек технологий

- **Backend**: LiteStar 2.x.
- **База данных**: PostgreSQL + Advanced-SQLAlchemy.
- **Инфраструктура**: Docker, docker-compose.
- **Пакетный менеджер**: Poetry 1.8.3.

## Установка и запуск

1. **Клонирование репозитория**

   Склонируйте репозиторий с GitHub:

   ```bash
   git clone https://github.com/Cka3o4Hukk/litestar-test-task.git
   ```

   ```bash
   cd litestar-test-task
   ```

2. **Настройка окружения**

   Создайте файл `.env` в корне проекта со следующим содержимым:

   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=testdb
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/testdb
   ```

3. **Запуск сервера**

   - Если у вас в инфре k8s, то для запуска приложения рекомендую uvicorn, если его нет - gunicorn

   **Вариант 1: Использование docker-compose напрямую**

   Соберите и запустите контейнеры:

   ```bash
   docker-compose build
   ```

   ```bash
   docker-compose up -d
   ```

   **Вариант 2: Использование Makefile**

   Проект предоставляет Makefile для упрощения команд. Убедитесь, что у вас установлен `make`.

   Соберите образы:

   ```bash
   make build
   ```

   Запустите приложение:

   ```bash
   make up
   ```

4. **Применение миграций**

   После запуска контейнеров примените миграции для создания таблиц в базе данных:

   ```bash
   make migrations
   ```

   Или, если вы используете docker-compose напрямую:

   ```bash
   docker-compose run --rm app alembic upgrade head
   ```

5. **Swagger**

   Swagger-документация доступна по адресу:

   ```plaintext
   http://localhost:8000/docs
   ```

   Протестируйте API с помощью тестового запроса:

   ```bash
   make test
   ```

   Ожидаемый ответ:

   ```json
   {
   	"id": "...",
   	"name": "Алексей",
   	"surname": "Иванов",
   	"created_at": "...",
   	"updated_at": "..."
   }
   ```

   Также вы можете запустить все тесты

   ```bash
   make test-pytest
   ```

   Ожидаемый ответ:

   ```python
   7 passed, 2 warnings
   ```

6. **Остановка приложения**

   Для остановки контейнеров выполните:

   ```bash
   make down
   ```

   Или, если вы используете docker-compose напрямую:

   ```bash
   docker-compose down
   ```
