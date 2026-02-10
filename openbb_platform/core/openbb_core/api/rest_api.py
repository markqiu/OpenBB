"""REST API for the OpenBB Platform."""

import json
import logging
import math
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.responses import Response
from openbb_core.api.app_loader import AppLoader
from openbb_core.api.router.commands import router as router_commands
from openbb_core.api.router.coverage import router as router_coverage
from openbb_core.api.router.system import router as router_system
from openbb_core.app.service.auth_service import AuthService
from openbb_core.app.service.system_service import SystemService
from openbb_core.env import Env

logger = logging.getLogger("uvicorn.error")


class SafeJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles NaN and Inf values."""

    def default(self, obj):
        """Convert NaN and Inf to None for JSON compliance."""
        if isinstance(obj, float):
            if math.isnan(obj) or math.isinf(obj):
                return None
        return super().default(obj)

    def iterencode(self, obj, _one_shot=False):
        """Encode with NaN/Inf handling."""
        def replace_nan_inf(o):
            """Recursively replace NaN and Inf with None."""
            if isinstance(o, dict):
                return {k: replace_nan_inf(v) for k, v in o.items()}
            elif isinstance(o, list):
                return [replace_nan_inf(item) for item in o]
            elif isinstance(o, float):
                if math.isnan(o) or math.isinf(o):
                    return None
            return o

        safe_obj = replace_nan_inf(obj)
        return super().iterencode(safe_obj, _one_shot)


class SafeJSONResponse(JSONResponse):
    """Custom JSONResponse that handles NaN and Inf values."""

    def render(self, content: any) -> bytes:
        """Render content to JSON, replacing NaN and Inf with null."""
        # Use jsonable_encoder to handle Pydantic models and other complex types
        json_data = jsonable_encoder(content)
        
        # Use custom encoder to handle NaN and Inf
        return json.dumps(
            json_data,
            ensure_ascii=False,
            allow_nan=False,
            cls=SafeJSONEncoder,
            indent=None,
        ).encode("utf-8")

system = SystemService().system_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Startup event."""
    auth = "ENABLED" if Env().API_AUTH else "DISABLED"
    banner = rf"""

                   ███╗
  █████████████████╔══█████████████████╗       OpenBB Platform v{system.version}
  ███╔══════════███║  ███╔══════════███║
  █████████████████║  █████████████████║       Authentication: {auth}
  ╚═════════════███║  ███╔═════════════╝
     ██████████████║  ██████████████╗
     ███╔═══════███║  ███╔═══════███║
     ██████████████║  ██████████████║
     ╚═════════════╝  ╚═════════════╝
Investment research for everyone, anywhere.

    https://my.openbb.co/app/platform

"""
    logger.info(banner)
    yield


app = FastAPI(
    title=system.api_settings.title,
    description=system.api_settings.description,
    version=system.api_settings.version,
    terms_of_service=system.api_settings.terms_of_service,
    contact={
        "name": system.api_settings.contact_name,
        "url": system.api_settings.contact_url,
        "email": system.api_settings.contact_email,
    },
    license_info={
        "name": system.api_settings.license_name,
        "url": system.api_settings.license_url,
    },
    servers=[
        {
            "url": s.url,
            "description": s.description,
        }
        for s in system.api_settings.servers
    ],
    lifespan=lifespan,
    default_response_class=SafeJSONResponse,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=system.api_settings.cors.allow_origins,
    allow_methods=system.api_settings.cors.allow_methods,
    allow_headers=system.api_settings.cors.allow_headers,
)
AppLoader.add_routers(
    app=app,
    routers=(
        [AuthService().router, router_system, router_coverage, router_commands]
        if Env().DEV_MODE
        else (
            [router_commands, router_coverage]
            if hasattr(router_commands, "routes") and router_commands.routes
            else [router_commands]
        )
    ),
    prefix=system.api_settings.prefix,
)
AppLoader.add_openapi_tags(app)
AppLoader.add_exception_handlers(app)


if __name__ == "__main__":
    # pylint: disable=import-outside-toplevel
    import uvicorn

    # This initializes the OpenBB environment variables so they can be read before uvicorn is run.
    Env()
    uvicorn_kwargs = system.python_settings.model_dump().get("uvicorn", {})
    uvicorn_reload = uvicorn_kwargs.pop("reload", None)

    if uvicorn_reload is None or uvicorn_reload:
        uvicorn_kwargs["reload"] = True

    uvicorn_app = uvicorn_kwargs.pop("app", "openbb_core.api.rest_api:app")

    uvicorn.run(uvicorn_app, **uvicorn_kwargs)
