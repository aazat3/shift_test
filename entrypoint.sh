#!/bin/sh

# alembic upgrade head

exec uvicorn shift_test.src.main:app \
    --host ${UVICORN_HOST} \
    --port ${UVICORN_PORT} \
    ${UVICORN_RELOAD:+--reload}