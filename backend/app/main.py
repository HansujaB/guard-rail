from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1 import dashboard, tracks, sensors, alerts, auth, intent

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX, tags=["auth"])
app.include_router(dashboard.router, prefix=settings.API_V1_PREFIX, tags=["dashboard"])
app.include_router(tracks.router, prefix=settings.API_V1_PREFIX, tags=["tracks"])
app.include_router(sensors.router, prefix=settings.API_V1_PREFIX, tags=["sensors"])
app.include_router(alerts.router, prefix=settings.API_V1_PREFIX, tags=["alerts"])
app.include_router(intent.router, prefix=settings.API_V1_PREFIX, tags=["intent"])


@app.get("/")
async def root():
    return {
        "message": "IRSS COMMAND API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

