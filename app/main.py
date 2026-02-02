from fastapi import FastAPI

app = FastAPI(title="Mini Social API")

@app.get("/health")
async def health_check():
    return {"status": "ok"}