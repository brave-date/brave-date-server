from fastapi import (
    FastAPI,
    Request,
)
from fastapi.middleware.cors import (
    CORSMiddleware,
)
from functools import (
    lru_cache,
)
import logging
from typing import (
    Dict,
)
import uvicorn

from app.auth import (
    router as auth_router,
)
from app.config import (
    settings,
)
from app.users import (
    router as users_router,
)
from app.utils import (
    engine,
)

logger = logging.getLogger(__name__)


@lru_cache()
def get_app() -> FastAPI:
    tinder_app = FastAPI(
        docs_url="/docs",
        redoc_url="/redocs",
        title="Brave Date Server",
        description="The server side of Brave Date.",
        version="0.1.0",
        openapi_url="/api/v1/openapi.json",
    )

    origins = [
        "http://127.0.0.1:8000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://localhost:3000",
    ]
    app_settings = settings()
    origins.extend(app_settings.cors_origins)

    tinder_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @tinder_app.on_event("startup")
    async def startup() -> None:
        logger.info("Connecting to MongoDB...")
        await engine.init_engine_app(tinder_app)
        logger.info("Connected to MongoDB!")

    @tinder_app.on_event("shutdown")
    async def shutdown() -> None:
        logger.info("Closing connection with MongoDB...")
        # bug: TypeError: object NoneType can't be used in 'await' expression
        try:
            await tinder_app.state.client.close()
        except Exception as err:
            logger.error(repr(err))
        logger.info("Closed connection with MongoDB!")

    @tinder_app.get("/api")
    async def root() -> Dict[str, str]:
        return {"message": "Welcome to the Brave Date Server."}

    tinder_app.include_router(auth_router.router, tags=["Auth"])
    tinder_app.include_router(users_router.router, tags=["User"])

    return tinder_app


tinder_app = get_app()


def serve() -> None:
    try:

        uvicorn.run(
            "app.main:tinder_app",
            host="0.0.0.0",
            workers=4,
            port=8000,
            reload=True,
            log_level="info",
        )
    except Exception as e:
        print(e)


if __name__ == "__main__":
    serve()
