from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import auth_routes, orphanage_routes, donation_routes, notification_routes

app = FastAPI(title="Donation App Backend (Orphanages)")

# CORS - allow Flutter web / mobile dev origins as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(orphanage_routes.router, prefix="/orphanages", tags=["orphanages"])
app.include_router(donation_routes.router, prefix="/donations", tags=["donations"])
app.include_router(notification_routes.router, prefix="/notifications", tags=["notifications"])


@app.get("/")
async def root():
    return {"message": "Donation App Backend — FastAPI is up."}
