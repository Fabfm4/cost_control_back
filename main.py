from fastapi import FastAPI
from src.bank.infrastructure.api.bank_api import router as bank_router
from src.bank.infrastructure.api.card_api import router as card_router


app = FastAPI(
    title="FastAPI Demo",
    description="This is a simple FastAPI demo.",
)

app.include_router(bank_router)
app.include_router(card_router)
