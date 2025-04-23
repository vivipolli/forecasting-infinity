import asyncio
import pytest
from neurons.miner.config import MinerConfig
from neurons.validator.utils.logger.logger import InfiniteGamesLogger
from neurons.miner.services.if_games_service import IfGamesService
from neurons.miner.services.event_service import EventService
from neurons.validator.if_games.client import IfGamesClient

@pytest.mark.asyncio
async def test_miner_integration():
    # Initialize components
    logger = InfiniteGamesLogger(name="test_miner")
    config = MinerConfig()
    
    # Create IfGames client and service
    if_games_client = IfGamesClient(
        env=config.env,
        logger=logger,
        bt_wallet=config.wallet
    )
    if_games_service = IfGamesService(if_games_client, logger)
    
    # Create event service
    event_service = EventService(
        if_games_service=if_games_service,
        logger=logger,
        feedback_weight=config.feedback_weight
    )
    
    # Test 1: Fetch events
    print("\nTesting event fetching...")
    events = await event_service.refresh_events()
    print(f"Fetched {len(events)} events")
    for event in events[:3]:  # Show first 3 events
        print(f"Event: {event.question}")
        print(f"Probability: {event.probability}")
        print(f"Validations: {event.expert_validations}")
        print("---")
    
    # Test 2: Submit feedback (if we have events)
    if events:
        first_event = events[0]
        print(f"\nTesting feedback submission for event: {first_event.question}")
        
        success = await event_service.process_feedback(
            event_id=first_event.event_id,
            agrees=True,
            comment="Test feedback from integration test"
        )
        
        print(f"Feedback submission {'succeeded' if success else 'failed'}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    asyncio.run(test_miner_integration()) 