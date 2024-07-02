import path  # noqa: F401
from fastapi import FastAPI

from bank.infrastructure.api import router as bank_router
from card.infrastructure.api import router as card_router
from transaction.infrastructure.api import router as transaction_router


app = FastAPI(
    title="FastAPI Demo",
    description="This is a simple FastAPI demo.",
)


app.include_router(bank_router)
app.include_router(card_router)
app.include_router(transaction_router)
