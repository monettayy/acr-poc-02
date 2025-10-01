from fastapi import FastAPI
from app.routers import health, users
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="A FastAPI backend with PostgreSQL and SQLAlchemy",
    version="1.0.0"
)

# Include routers
app.include_router(health.router)
app.include_router(users.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to FastAPI Backend", "docs": "/docs"}
