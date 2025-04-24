# Infinite Games MVP

![Infinite Games Logo](infinite-games.jpeg)

## Overview

This MVP extends the Infinite Games template by adding a complete forecasting system with expert feedback integration. The system combines AI-powered predictions with human expert validations to create more accurate forecasts.

### Key Features Added

- RLHF (Reinforcement Learning with Human Feedback) integration
- Expert feedback collection and weighting system
  - Base adjustment of 0.1 per expert feedback
  - Maximum adjustment capped at 0.3
  - Weighted adjustments based on expert reliability
  - Minimum of 3 expert validations required
  - One feedback per expert per event
- Real-time event monitoring and prediction updates
- Modern web interface for event visualization and feedback submission

## System Architecture

### Backend Components

1. **Miner Service**
   - Handles event predictions using the RLHF forecaster
   - Integrates with Bittensor network for decentralized operations
   - Processes and weights expert feedback using ExpertFeedbackAdjuster
     - Each expert feedback adjusts probability by 0.1 (base)
     - Expert weight multiplier (e.g., 1.1 for trusted experts)
     - Maximum total adjustment capped at 0.3
     - Minimum 3 expert validations required
     - One feedback per expert per event to prevent manipulation
   - Caches predictions to optimize performance

2. **API Service**
   - RESTful endpoints for event data and feedback
   - Real-time event updates
   - Feedback submission and validation
   - Integration with IfGames API

### Frontend Components

- Event card display with prediction probabilities
- Feedback modal for expert input
- Real-time updates of predictions
- Category-based filtering
- Responsive design for all devices

## Future Improvements

   - Category-specific adjustment limits
   - Feedback decay over time
   - Expert reputation system
   - Feedback cooling period
   - Rate limiting per expert
   - IP-based restrictions
   - Expert verification system
   - Anti-manipulation measures

## Local Development Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- Bittensor wallet configured for testnet
- API keys for LLM services:
  ```bash
  export PERPLEXITY_API_KEY=<your_perplexity_api_key>
  export OPENAI_API_KEY=<your_openai_api_key>
  ```

### Running the Services

1. **Start the Miner**
```bash
python3 neurons/miner.py --netuid 155 --subtensor.network test --wallet.name miner --wallet.hotkey miner
```

2. **Start the API Service**
```bash
python3 -m neurons.miner.api.run
```

The miner will run on port 8091 (default) and the API service on port 8000.

### Testing

#### Manual API Testing

1. **Test Event Fetching**
```bash
curl http://localhost:8000/api/events
```

2. **Test Feedback Submission**
```bash
curl -X POST http://localhost:8000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "your_event_id",
    "agrees": true,
    "comment": "Test feedback"
  }'
```

#### Direct Test Scripts

1. **Run API Integration Test**
```bash
python3 neurons/miner/tests/test_api.py
```

2. **Run Miner Integration Test**
```bash
python3 neurons/miner/tests/test_miner.py
```

These tests will verify:
- Event fetching and processing
- Feedback submission and integration
- RLHF forecaster functionality
- Storage and caching systems
- Task execution and async operations

## Project Structure

```
infinite_games/
└── neurons/
    └── miner/
        ├── api/                    # API REST endpoints
        │   ├── custom_miner.py     # Custom endpoints for events and feedback
        │   ├── run.py             # API server initialization
        │   └── server.py          # FastAPI server setup
        │
        ├── base/                  # Base classes
        │   ├── miner.py          # Base miner implementation
        │   └── neuron.py         # Base neuron for Bittensor
        │
        ├── forecasters/           # Prediction models
        │   ├── base.py           # Base forecaster class
        │   └── llm_forecaster.py # LLM-based predictions with expert feedback
        │
        ├── models/               # Data models
        │   └── event.py         # Event data structure
        │
        ├── services/            # Business logic
        │   ├── event_service.py # Event handling
        │   ├── expert_feedback_adjuster.py # Expert feedback processing
        │   └── if_games_service.py # IfGames integration
```

### Key Components

1. **API Layer** (`api/`)
   - `custom_miner.py`: Handles event fetching and feedback submission
   - `run.py`: Standalone API server runner
   - `server.py`: FastAPI application configuration

2. **Forecasters** (`forecasters/`)
   - `base.py`: Abstract forecaster interface
   - `llm_forecaster.py`: LLM-based prediction with expert feedback integration

3. **Services** (`services/`)
   - `event_service.py`: Event management and caching
   - `expert_feedback_adjuster.py`: Expert feedback processing and prediction adjustment
   - `if_games_service.py`: Integration with IfGames platform

### Running the Miner

1. **Start the Miner Service**
```bash
python3 neurons/miner.py --netuid 155 --subtensor.network test --wallet.name miner --wallet.hotkey miner
```

2. **Start the API Service**
```bash
python3 -m neurons.miner.api.run
```

The miner runs on port 8091 (default Bittensor port) and the API on port 8000.

### Testing

1. **Test Event Fetching**
```bash
curl http://localhost:8000/api/events
```

2. **Test Feedback Submission**
```bash
curl -X POST http://localhost:8000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "your_event_id",
    "agrees": true,
    "comment": "Test feedback"
  }'
```

3. **Monitor Miner Logs**
```bash
tail -f ~/.bittensor/miners/netuid_155/logs/output.log
```

4. **Check API Logs**
```bash
tail -f ~/.bittensor/miners/netuid_155/logs/api.log
```

### Flow

1. Miner receives events from the Bittensor network
2. Events are processed by the RLHF forecaster
3. Predictions are stored and cached
4. API endpoints serve predictions and collect feedback
5. Expert feedback is processed by ExpertFeedbackAdjuster:
   - Each expert feedback adjusts probability by 0.1 (base)
   - Expert weight multiplier applied (e.g., 1.1 for trusted experts)
   - Maximum total adjustment capped at 0.3
   - Minimum 3 expert validations required
6. Adjusted predictions are sent back to the network


