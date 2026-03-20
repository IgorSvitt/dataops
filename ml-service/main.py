import json
import logging
import os
import time
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from starlette.responses import Response

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://service:service@db:5432/service")
MODEL_VERSION = os.getenv("MODEL_VERSION", "0.1.0")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True)
    model_version = Column(String(32), nullable=False)
    model_input = Column(Text, nullable=False)
    model_output = Column(Text, nullable=False)
    duration_ms = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


Base.metadata.create_all(bind=engine)

logger = logging.getLogger("ml_service")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(handler)

REQUEST_COUNT = Counter("ml_service_requests_total", "Total number of prediction requests")
REQUEST_ERRORS = Counter("ml_service_request_errors_total", "Total number of failed prediction requests")
REQUEST_LATENCY = Histogram("ml_service_request_duration_seconds", "Prediction latency in seconds")

app = FastAPI(title="Simple ML Service", version=MODEL_VERSION)


class PredictRequest(BaseModel):
    features: list[float] = Field(min_length=1)


class PredictResponse(BaseModel):
    prediction: float
    model_version: str
    duration_ms: int


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/predict", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    REQUEST_COUNT.inc()
    start = time.perf_counter()

    try:
        prediction = sum(payload.features) / len(payload.features)
        duration_ms = int((time.perf_counter() - start) * 1000)

        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "prediction",
            "input": payload.features,
            "output": prediction,
            "duration_ms": duration_ms,
            "model_version": MODEL_VERSION,
        }
        logger.info(json.dumps(log_record, ensure_ascii=False))

        with SessionLocal() as session:
            row = PredictionLog(
                model_version=MODEL_VERSION,
                model_input=json.dumps(payload.features),
                model_output=json.dumps({"prediction": prediction}),
                duration_ms=duration_ms,
            )
            session.add(row)
            session.commit()

        REQUEST_LATENCY.observe((time.perf_counter() - start))
        return PredictResponse(prediction=prediction, model_version=MODEL_VERSION, duration_ms=duration_ms)

    except Exception:
        REQUEST_ERRORS.inc()
        raise


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
