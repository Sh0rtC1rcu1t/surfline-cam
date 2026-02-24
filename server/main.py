import json
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# OpenTelemetry tracing setup (Console exporter for local dev)
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("surfline_cam_api")

# Basic tracer provider
resource = Resource.create({"service.name": "surfline-cam-api"})
provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = FastAPI(title="Surfline Cam API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
FastAPIInstrumentor().instrument_app(app)

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "cameras.json"


@app.get("/health")
def health():
    """Simple health check"""
    return {"status": "ok"}


@app.get("/api/cameras")
def get_cameras():
    """Return the cameras list read from `data/cameras.json`"""
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return data
    except Exception as exc:
        logger.exception("Failed to load cameras.json")
        raise HTTPException(status_code=500, detail=str(exc))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server.main:app", host="127.0.0.1", port=8000, reload=True)
