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

from bittensor import logging

from neurons.miner.forecasters.base import BaseForecaster
from neurons.miner.forecasters.rlhf_forecaster import RLHFForecaster
from neurons.miner.main import Miner
from neurons.miner.models.event import MinerEvent
from neurons.validator.utils.logger.logger import InfiniteGamesLogger, miner_logger


def get_forecaster(logger: InfiniteGamesLogger):
    async def assign_forecaster(event: MinerEvent) -> typing.Type[BaseForecaster]:
        return RLHFForecaster(
            event,
            logger=logger,
            extremize=False,
            feedback_weight=0.3,  # Weight of human feedback in final prediction
            min_feedback_count=3,  # Minimum number of feedbacks required to use them
            use_feedback=True,     # Whether to use feedback at all
        )

    return assign_forecaster


if __name__ == "__main__":
    start_time = time.time()

    async def run_miner() -> None:
        miner_logger.start_session()

        miner = Miner(logger=miner_logger, assign_forecaster=get_forecaster(miner_logger))
        await miner.initialize()
        with miner as miner:
            while True:
                miner_logger.debug(f"Miner running for {time.time() - start_time:.1f} seconds")
                await asyncio.sleep(5)

    asyncio.run(run_miner())
