# -- DO NOT TOUCH BELOW - ENV SET --
# flake8: noqa: E402
import asyncio
import os
import sys
import typing

# Force torch - must be set before importing bittensor
os.environ["USE_TORCH"] = "1"

# Add the parent directory of the script to PYTHONPATH
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)
# -- DO NOT TOUCH ABOVE --

import time
import uvicorn

from bittensor import logging

from neurons.miner.forecasters.base import BaseForecaster
from neurons.miner.forecasters.llm_forecaster import LLMForecaster
from neurons.miner.main import Miner
from neurons.miner.models.event import MinerEvent
from neurons.validator.utils.logger.logger import InfiniteGamesLogger, miner_logger
from neurons.miner.api.server import app


async def assign_forecaster(event: MinerEvent) -> BaseForecaster:
    """
    Assign a forecaster based on event type.
    Uses LLMForecaster as the default forecaster.
    """
    return LLMForecaster(
        event=event,
        logger=logger,
        if_games_client=if_games_client,
        extremize=True
    )


async def run_api():
    """Run the API REST server"""
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    start_time = time.time()

    async def run_miner() -> None:
        miner_logger.start_session()

        miner = Miner(logger=miner_logger, assign_forecaster=assign_forecaster)
        await miner.initialize()

        try:
            await asyncio.gather(
                run_api(),
                miner.run()
            )
        except KeyboardInterrupt:
            print("Shutting down...")
        finally:
            await miner.storage.save()
            if hasattr(miner, 'storage_task'):
                miner.storage_task.cancel()
            if hasattr(miner, 'task_executor_task'):
                miner.task_executor_task.cancel()

    asyncio.run(run_miner())
