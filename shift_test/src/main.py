import logging

from fastapi import FastAPI

from shift_test.src.core.logging import setup_logging
from shift_test.src.api.router import api_router

logger = logging.getLogger(__name__)

app = FastAPI(title="SHIFT Test API", version="1.0.0")
app.include_router(api_router)

setup_logging()