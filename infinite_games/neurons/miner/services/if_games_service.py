from typing import List, Optional
from neurons.validator.if_games.client import IfGamesClient
from neurons.validator.utils.logger.logger import InfiniteGamesLogger
from neurons.miner.models.event import MinerEvent
from neurons.miner.mocks.events import get_mock_events
from neurons.miner.forecasters.llm_forecaster import LLMForecaster
import json
from datetime import datetime

class IfGamesService:
    def __init__(self, client: IfGamesClient, logger: InfiniteGamesLogger):
        self.client = client
        self.logger = logger
        self.forecaster = None
        self.processed_events = set()  # Track processed event IDs

    async def get_events(self, from_date: int = 0) -> List[MinerEvent]:
        try:
            self.logger.info(f"Starting get_events with from_date: {from_date}")
            self.processed_events.clear()  # Clear processed events for new request
            
            # Try to get real events first
            try:
                self.logger.info("Fetching events from API")
                response = await self.client.get_events(from_date=from_date, offset=0, limit=100)
                self.logger.info(f"API response received: {type(response)}")
                
                # Extract events from response
                events = []
                if isinstance(response, dict):
                    if 'items' in response:
                        events = response['items']
                        self.logger.info(f"Extracted {len(events)} events from items")
                    else:
                        self.logger.warning("No 'items' key found in response")
                elif isinstance(response, list):
                    events = response
                    self.logger.info(f"Received {len(events)} events directly")
                else:
                    self.logger.warning(f"Unexpected response type: {type(response)}")
                
                if not events:
                    self.logger.warning("No real events found, using mock events")
                    events = get_mock_events()
                    self.logger.info(f"Using {len(events)} mock events")
            except Exception as e:
                self.logger.error(f"Error getting real events: {e}")
                self.logger.warning("Using mock events as fallback")
                events = get_mock_events()
                self.logger.info(f"Using {len(events)} mock events")
            
            # Process events
            miner_events = []
            for event in events:
                try:
                    event_id = event.get('event_id', event.get('id', ''))
                    
                    # Skip if already processed
                    if event_id in self.processed_events:
                        self.logger.info(f"Skipping already processed event: {event_id}")
                        continue
                    
                    self.processed_events.add(event_id)
                    
                    if isinstance(event, MinerEvent):
                        self.logger.info(f"Event {event_id} is already a MinerEvent")
                        miner_events.append(event)
                    else:
                        self.logger.info(f"Converting event {event_id} to MinerEvent")
                        
                        # Create MinerEvent with default probability
                        miner_event = MinerEvent(
                            event_id=event_id,
                            market_type=event.get('market_type', 'BINARY'),
                            probability=0.5,  # Default value
                            description=event.get('description', ''),
                            cutoff=event.get('cutoff', datetime.now()),
                            status=event.get('status', 'UNRESOLVED')
                        )
                        
                        miner_events.append(miner_event)
                        self.logger.info(f"Successfully converted event {event_id}")
                        
                except Exception as e:
                    self.logger.error(f"Error processing event {event.get('event_id', 'unknown')}: {str(e)}")
                    continue
            
            self.logger.info(f"Returning {len(miner_events)} MinerEvent objects")
            return miner_events
            
        except Exception as e:
            self.logger.error(f"Error in get_events: {e}")
            mock_events = get_mock_events()
            self.logger.info(f"Using {len(mock_events)} mock events as final fallback")
            return mock_events