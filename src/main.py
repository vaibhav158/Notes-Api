from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.config import get_app_settings
from src.database import db
from src.auth.routes.auth import auth_router


def get_application() -> FastAPI:
    settings = get_app_settings()
    settings.configure_logging()

    app = FastAPI(**settings.fastapi_kwargs)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    db.init_db(app)

    return app


app = get_application()
app.include_router(auth_router)


@app.get("/")
def index_route():
    return {
        "message": "Hello, World!"
    }
