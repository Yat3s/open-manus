from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .deep_research.routes import deep_research_router
from contextlib import asynccontextmanager
from rich.console import Console
from rich import print as rprint

console = Console()


@asynccontextmanager
async def lifespan(app: FastAPI):
    console.rule("[bold blue]Deep Research API Starting")
    rprint("[bold green]🚀 Initializing services...")
    rprint("[bold yellow]⚙️  Loading configurations...")
    rprint("[bold green]✨ Initialization completed")

    yield

    console.rule("[bold blue]Deep Research API Stopping")
    rprint("[bold red]🛑 Shutting down services...")
    rprint("[bold green]✅ Cleanup completed")


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
