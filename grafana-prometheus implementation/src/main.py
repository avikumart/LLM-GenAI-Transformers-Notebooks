from prometheus_fastapi_intrumentator import Instrumentator
from fastapi import FastAPI
import uvicorn


app = FastAPI()
Instrumentator().instrument(app).expose(app)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, access_log=False, workers=2)