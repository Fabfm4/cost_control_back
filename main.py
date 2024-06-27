import path  # noqa: F401
from fastapi import FastAPI

from bank.infrastructure.api.bank_api import router as bank_router
from bank.infrastructure.api.card_api import router as card_router


app = FastAPI(
    title="FastAPI Demo",
    description="This is a simple FastAPI demo.",
)


app.include_router(bank_router)
app.include_router(card_router)
