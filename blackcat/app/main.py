from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.database import init_db
from app.routes.identities import router as identities_router
import os

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="BlackCat Identity Management",
    description="Identity and entitlement management system",
    version="0.1.0"
)

# Include routers
app.include_router(identities_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to BlackCat Identity Management",
        "environment": os.getenv("ENV", "development"),
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Service is running"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
