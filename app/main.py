from fastapi import FastAPI
from app.routers import health, users, roles
from app.config import settings
from app.database import SessionLocal
from app import crud

app = FastAPI(
    title=settings.APP_NAME,
    description="A FastAPI backend with PostgreSQL and SQLAlchemy",
    version="1.0.0"
)

# Include routers
app.include_router(health.router)
app.include_router(users.router)
app.include_router(roles.router)


@app.on_event("startup")
async def startup_event():
    """Initialize default data on startup"""
    db = SessionLocal()
    try:
        # Create default roles
        crud.create_default_roles(db)
        # Create default superuser
        crud.create_default_superuser(db)
    finally:
        db.close()


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to FastAPI Backend", "docs": "/docs"}
