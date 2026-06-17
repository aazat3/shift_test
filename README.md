# Shift_test API (FastAPI + SQLAlchemy + Alembic + Pydantic + Docker + Pytest)

Веб-сервис для автоматизации бронирования переговорных комнат в коворкинге.

Система позволяет:

- пользователям просматривать доступность переговорных комнат;
- создавать и отменять свои бронирования;
- администраторам управлять всеми бронированиями;
- управлять временными слотами комнат.

Аутентификация реализована через JWT-токены.

---

## Технологии

- Python 3.12+
- FastAPI
- SQLAlchemy (Async)
- PostgreSQL
- Alembic
- JWT Authentication
- Docker / Docker Compose
- Pytest

---

## Быстрый старт (Docker Compose)

```bash
git clone https://github.com/aazat3/shift_test.git 
cd shift_test  
docker compose up -d
docker compose exec api alembic upgrade head 
```

<http://localhost:8000/docs>

## Запуск тестов

```bash
docker compose exec api pytest -v 
```

## Adminer (управление базой данных)

<http://localhost:8080>
(данные для подключения в env файле)

## Alembic (миграция базы данных)

```bash
docker compose exec api alembic revision --autogenerate -m "(название)"
docker compose exec api alembic upgrade head  
```

## API Endpoints

## Authentication

### POST `/api/auth/register`

Регистрация нового пользователя.
Создает учетную запись сотрудника в системе.

### POST `/api/auth/login`

Авторизация пользователя.
Возвращает JWT-токен для доступа к защищенным эндпоинтам.

### POST `/api/auth/logout`

Выход пользователя из системы.
Удаляет текущую сессию авторизации.

### GET `/api/auth/me/`

Получение информации о текущем авторизованном пользователе.

---

## Rooms

### GET `/api/rooms/`

Получение списка всех переговорных комнат вместе с доступными временными слотами.

### POST `/api/rooms/`

Создание новой переговорной комнаты.
Доступно только администраторам.

### GET `/api/rooms/{room_id}`

Получение информации о конкретной комнате.

### PUT `/api/rooms/{room_id}`

Обновление информации о переговорной комнате.
Доступно только администраторам.

### DELETE `/api/rooms/{room_id}`

Удаление переговорной комнаты.
Доступно только администраторам.

---

## Room Slots

### GET `/api/room_slots/`

Получение списка всех временных слотов комнат.

### POST `/api/room_slots/`

Создание нового временного слота для комнаты.
Доступно администраторам.

### GET `/api/room_slots/{room_id}/room_slots`

Получение всех временных слотов конкретной комнаты.

### PUT `/api/room_slots/{room_slot_id}`

Изменение времени существующего слота.
Доступно администраторам.

### DELETE `/api/room_slots/{room_slot_id}`

Удаление временного слота.
Доступно администраторам.

---

## Bookings

### GET `/api/bookings/`

Получение списка всех бронирований.
Доступно администраторам.

### POST `/api/bookings/`

Создание нового бронирования.
Пользователь может забронировать свободный временной слот на выбранную дату.

### GET `/api/bookings/my`

Получение списка собственных бронирований текущего пользователя.

### GET `/api/bookings/{booking_id}`

Получение информации о конкретном бронировании.

### DELETE `/api/bookings/{booking_id}`

Отмена бронирования.
Пользователь может отменить только свои бронирования.
Администратор может отменить любое бронирование.

---

## Availability

### GET `/api/availability/`

Получение доступности всех переговорных комнат на выбранную дату.
Параметры: date - дата проверки доступности
Пример: GET /api/availability/?date=2026-06-17

### GET `/api/availability/rooms/{room_id}`

Получение доступности конкретной комнаты на выбранную дату.
Параметры: booking_date - дата проверки
Пример: GET /api/availability/rooms/1?booking_date=2026-06-17
Возвращает список временных слотов комнаты с информацией:

- время начала
- время окончания
- доступность слота
