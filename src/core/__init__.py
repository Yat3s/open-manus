from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .deep_research.routes import deep_research_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("========================")
    print("🚀 Deep Research API is starting...")
    print("========================")
    yield
    print("========================")
    print("🚀 Deep Research API has been stopped")
    print("========================")


version = "v1"
version_prefix = f"/api/{version}"


app = FastAPI(
    title="Deep Research API",
    version=version,
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    deep_research_router, prefix=f"{version_prefix}", tags=["deep_research"]
)
