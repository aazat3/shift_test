# Question and answer API (FastAPI + SQLAlchemy + Alembic + Pydantic + Docker + Pytest)

<!-- Минимальный CRUD-сервис управления вопросами и ответами.  -->

<!-- Методы API:
Вопросы (Questions):
GET /questions/ — список всех вопросов
POST /questions/ — создать новый вопрос
GET /questions/{id} — получить вопрос и все ответы на него
DELETE /questions/{id} — удалить вопрос (вместе с ответами)

Ответы (Answers):
POST /questions/{id}/answers/ — добавить ответ к вопросу
GET /answers/{id} — получить конкретный ответ
DELETE /answers/{id} — удалить ответ -->

## Быстрый старт (Docker Compose)

```bash
docker compose up -d
docker compose exec api alembic upgrade head
```

<http://localhost:8000/docs>

## Запуск тестов

```bash
docker compose exec api pytest -v -s   
```

## Adminer (управление базой данных)

<http://localhost:8080>
(данные для подключения в env файле)

## Alembic (миграция базы данных)

```bash
docker compose alembic revision --autogenerate -m "(название)"
docker compose exec api alembic upgrade head  
```
