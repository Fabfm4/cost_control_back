from fastapi import FastAPI

from app.bank.infrastructure.api import router as bank_router
from app.card.infrastructure.api import router as card_router
from app.transaction.infrastructure.api import router as transaction_router
from app.transaction_split.infrastructure.api import router as transaction_split_router  # noqa
from app.card_balance.infrastructure.api import router as card_balance_router  # noqa


app = FastAPI(
    title="FastAPI Demo",
    description="This is a simple FastAPI demo.",
)


app.include_router(bank_router)
app.include_router(card_router)
app.include_router(transaction_router)
app.include_router(transaction_split_router)
app.include_router(card_balance_router)
