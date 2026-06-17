from fastapi import APIRouter

from shift_test.src.api.bookings import router as bookings_router
from shift_test.src.api.rooms import router as rooms_router
from shift_test.src.api.auth import router as auth_router
from shift_test.src.api.room_slot import router as room_slot_router
from shift_test.src.api.availability import router as room_availability_router





api_router = APIRouter(prefix="/api")
api_router.include_router(bookings_router)
api_router.include_router(rooms_router)
api_router.include_router(auth_router)
api_router.include_router(room_slot_router)
api_router.include_router(room_availability_router)
