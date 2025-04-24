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
        self.processed_events = set()

    async def get_events(self, from_date: int = 0) -> List[MinerEvent]:
        try:
            self.processed_events.clear()
            
            try:
                response = await self.client.get_events(from_date=from_date, offset=0, limit=100)
                
                events = []
                if isinstance(response, dict):
                    if 'items' in response:
                        events = response['items']
                elif isinstance(response, list):
                    events = response
                
                if not events:
                    events = get_mock_events()
            except Exception as e:
                events = get_mock_events()
            
            miner_events = []
            for event in events:
                try:
                    event_id = event.get('event_id', event.get('id', ''))
                    
                    if event_id in self.processed_events:
                        continue
                    
                    self.processed_events.add(event_id)
                    
                    if isinstance(event, MinerEvent):
                        miner_events.append(event)
                    else:
                        miner_event = MinerEvent(
                            event_id=event_id,
                            market_type=event.get('market_type', 'BINARY'),
                            probability=0.5,
                            description=event.get('description', ''),
                            cutoff=event.get('cutoff', datetime.now()),
                            status=event.get('status', 'UNRESOLVED')
                        )
                        
                        miner_events.append(miner_event)
                        
                except Exception as e:
                    continue
            
            return miner_events
            
        except Exception as e:
            mock_events = get_mock_events()
            return mock_events