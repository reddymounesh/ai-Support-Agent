from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.error_handlers import register_exception_handlers
from app.logging_config import configure_logging
from app.middleware import RequestIDMiddleware

from app.routers import customers, health, orders,chat,tickets

configure_logging()

app = FastAPI(
    title="AI Customer Support Agent",
    version="0.1.0",
    description="Backend for an AI-powered customer support agent.",
)

register_event_handlers(app)


app.add_middleware(RequestIDMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(chat.router)
app.include_router(tickets.router)

