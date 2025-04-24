# 🔮 Infinity Crystal

## 📝 Overview
A prediction market system that uses AI and expert validation to forecast event outcomes. The system applies Reinforcement Learning from Human Feedback (RLHF) principles, where AI-generated predictions are continuously refined through expert validation. This creates a dynamic feedback loop where human expertise guides and improves the AI's forecasting capabilities.

**Key Concepts**: AI Forecasting, Expert Validation, RLHF (Reinforcement Learning from Human Feedback), Prediction Markets

## 🔄 How It Works

### Expert Onboarding
1. Submit expert application form with your area of expertise
2. Get approved through:
   - AI analysis of social media presence
   - Or human evaluation of credentials
3. Receive expert role with specific domain access

### Prediction Process
1. AI generates initial probability forecast for events
2. Experts receive event listings with current predictions
3. Experts can review and provide feedback:
   - Click "Agree" if they believe the event will occur
   - Click "Disagree" if they believe the event will not occur
4. System recalculates prediction based on:
   - Expert's feedback (agree/disagree)
   - Expert's weight in their domain
   - Current prediction value
5. Updated prediction is displayed and tracked

## 🏗️ Feedback Implementation

### LLM Forecaster
```python
# neurons/miner/forecasters/llm_forecaster.py
class LLMForecaster(BaseForecaster):
    ...

    async def adjust_with_feedback(
        self,
        current_prediction: float,
        agrees: bool,
        expert_weight: float = 1.0,
        expert_id: str = None,
        event_id: str = None
    ) -> float:
        try:
            self.logger.info(f"Adjusting prediction with expert feedback (weight: {expert_weight})")
            
            new_prediction = self.feedback_adjuster.adjust_prediction(
                current_prediction=current_prediction,
                expert_agrees=agrees,
                expert_weight=expert_weight,
                expert_id=expert_id,
                event_id=event_id
            )
            
            self.logger.info(f"Adjusted prediction: {current_prediction} -> {new_prediction}")
            return new_prediction
            
        except Exception as e:
            self.logger.error(f"Error adjusting prediction: {e}")
            return current_prediction

### Expert Feedback Adjuster
```python
# neurons/miner/services/expert_feedback_adjuster.py
class ExpertFeedbackAdjuster:
    def __init__(self):
        self.expert_history = {}
        self.feedback_history = {}
        
    def adjust_prediction(self, current_prediction: float, expert_agrees: bool, 
                         expert_weight: float = 1.0, expert_id: str = None, 
                         event_id: str = None) -> float:
        if not self._validate_expert(expert_id):
            return current_prediction
            
        feedback_key = f"{expert_id}_{event_id}"
        if feedback_key in self.feedback_history:
            return current_prediction
            
        self.feedback_history[feedback_key] = {
            "timestamp": datetime.now(),
            "agrees": expert_agrees,
            "weight": expert_weight,
            "event_id": event_id
        }
        
        adjustment = expert_weight * (0.1 if expert_agrees else -0.1)
        adjustment *= self._calculate_expert_multiplier(expert_id)
        adjustment = max(min(adjustment, 0.3), -0.3)
        
        return max(0.0, min(1.0, current_prediction + adjustment))
```

### Event Service
```python
# neurons/miner/services/event_service.py
class EventService:
    def __init__(self, if_games_client: IfGamesClient):
        self.if_games_client = if_games_client
        self.prediction_history = {}
        self.expert_performance = {}
        
    async def process_feedback(self, event_id: str, expert_id: str, agrees: bool):
        event = await self.if_games_client.get_event(event_id)
        old_probability = event.get_probability()
        
        forecaster = LLMForecaster(event, self.logger, self.if_games_client)
        new_probability = await forecaster.adjust_with_feedback(
            current_prediction=old_probability,
            agrees=agrees,
            expert_id=expert_id,
            event_id=event_id
        )
        
        self.prediction_history[event_id] = {
            "timestamp": datetime.now(),
            "old_probability": old_probability,
            "new_probability": new_probability,
            "expert_id": expert_id,
            "agrees": agrees
        }
        
        await self.if_games_client.post_prediction(event_id, new_probability)
```

#### API Layer (`neurons/miner/api/`)
- `custom_miner.py`: Custom API endpoints for feedback and predictions
- `server.py`: FastAPI server setup
- `run.py`: API startup script

#### Services (`neurons/miner/services/`)
- `event_service.py`: Event management and prediction processing
- `expert_feedback_adjuster.py`: Expert feedback handling and prediction adjustment
- `if_games_service.py`: IfGames API integration

## 🔜 Next Steps
- Implement expert performance tracking
- Add prediction history visualization
- Enhance feedback weighting system
- Improve prediction accuracy algorithms

## 🛠️ Local Development Setup

### Prerequisites

```bash
export PERPLEXITY_API_KEY=<your_perplexity_api_key>
export OPENAI_API_KEY=<your_openai_api_key>
```

### Running the System

1. **Start the Miner**
```bash
python3 neurons/miner.py --netuid 155 --subtensor.network test --wallet.name miner --wallet.hotkey miner
```

2. **Start the API**
```bash
python3 -m neurons.miner.api.run
```

> Note: This is the basic setup. For complete setup instructions, including wallet creation, registration, and advanced configuration, please refer to [miner.md](infinite_games/docs/miner.md).




