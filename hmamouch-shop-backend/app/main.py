from fastapi import FastAPI

app = FastAPI(title="Hmamouch Shop Backend")

@app.get("/")
async def root():
    return {"ok": True, "message": "Hmamouch Shop backend is running"}
