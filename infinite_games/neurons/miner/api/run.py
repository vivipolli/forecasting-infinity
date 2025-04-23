import uvicorn
from neurons.miner.config import MinerConfig
from neurons.validator.utils.logger.logger import InfiniteGamesLogger

if __name__ == "__main__":
    logger = InfiniteGamesLogger(name="miner_api")
    
    config = MinerConfig()
    
    logger.info(f"Starting miner API with config: {config.__dict__}")
    
    uvicorn.run(
        "neurons.miner.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 