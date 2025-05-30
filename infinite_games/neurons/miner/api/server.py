from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .custom_miner import router as custom_miner_router

app = FastAPI(
    title="Miner API",
    description="API for the Infinite Games Miner",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(custom_miner_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
