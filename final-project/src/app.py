import os
import time
from fastapi import FastAPI, Request, HTTPException, status
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from prometheus_client import Counter, Histogram, make_asgi_app

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="MLOps Production Inference API", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

REQUEST_COUNT = Counter("prediction_requests_total", "Total inference requests", ["model_version", "status"])
REQUEST_LATENCY = Histogram("prediction_latency_seconds", "Inference latency in seconds", ["model_version"])

MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0.0")

class PredictRequest(BaseModel):
    data: list[float] = Field(..., min_length=1, description="Вхідний вектор ознак")

class PredictResponse(BaseModel):
    model_version: str
    prediction: list[float]
    latency: float

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy", "model_version": MODEL_VERSION}

@app.get("/ready", status_code=status.HTTP_200_OK)
def readiness_check():
    return {"status": "ready"}

@app.post("/predict", response_model=PredictResponse)
@limiter.limit("5/minute")
def predict(payload: PredictRequest, request: Request):
    start_time = time.time()
    try:
        # Емуляція / запуск моделі
        prediction = [round(x * 0.5, 4) for x in payload.data]
        latency = round(time.time() - start_time, 4)
        
        REQUEST_COUNT.labels(model_version=MODEL_VERSION, status="success").inc()
        REQUEST_LATENCY.labels(model_version=MODEL_VERSION).observe(latency)
        
        return PredictResponse(
            model_version=MODEL_VERSION,
            prediction=prediction,
            latency=latency
        )
    except Exception as e:
        REQUEST_COUNT.labels(model_version=MODEL_VERSION, status="error").inc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
