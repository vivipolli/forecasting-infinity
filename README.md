# Infinite Games Prediction System

## Overview

This project enhances the Infinite Games ecosystem by creating an advanced prediction system that combines AI-powered forecasting with human expert validation. The system aims to improve market liquidity and forecast accuracy through innovative approaches to prediction and validation.

### Key Innovations

- **RLHF Integration**
  - Base adjustment of 0.1 per expert feedback
  - Maximum adjustment capped at 0.3
  - Weighted adjustments based on expert reliability
  - Minimum of 3 expert validations required
  - One feedback per expert per event
- Real-time event monitoring and prediction updates
- Modern web interface for event visualization and feedback submission

## System Architecture

### Core Components

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
   - RESTful endpoints for events and feedback
   - Real-time event updates
   - Feedback submission and validation
   - Integration with IfGames API

3. **Frontend**
   - Event card display with probabilities
   - Feedback modal for expert input
   - Real-time prediction updates
   - Category-based filtering

## Getting Started

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

## Project Structure

```
infinite_games/
└── neurons/
    └── miner/
        ├── api/                    # API endpoints
        ├── forecasters/            # Prediction models
        ├── services/              # Business logic
        └── models/                # Data models
```

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

## Feedback and Prediction Storage Flow

### Overview
The system implements a robust feedback-based prediction system that combines AI-powered forecasts with expert validations. Predictions are continuously refined through expert feedback and stored in a persistent database for historical tracking and analysis.

### Components

1. **Event Service**
   - Manages events and their predictions
   - Handles feedback processing
   - Uses `ExpertFeedbackAdjuster` to calculate new probabilities
   - Maintains prediction history and expert performance metrics

2. **Expert Feedback System**
   - Experts can agree or disagree with current predictions
   - Dynamic expert weighting based on historical performance
   - Feedback validation and anti-manipulation measures
   - Expert reputation tracking and scoring

3. **Prediction Storage**
   - Predictions stored in PostgreSQL database
   - Historical tracking of all prediction changes
   - Expert feedback history and impact analysis
   - Performance metrics and analytics

### Flow

1. Expert submits feedback through the frontend
2. Feedback is sent to `/api/feedback` endpoint
3. `EventService` processes the feedback:
   - Validates expert credentials and reputation
   - Checks for manipulation attempts
   - Uses `ExpertFeedbackAdjuster` to calculate new probability
   - Updates event's probability in database
   - Records feedback and prediction change history
4. Updated prediction is immediately available for display
5. Expert performance metrics are updated

### Technical Details

- Feedback endpoint: `POST /api/feedback`
- Required parameters:
  - `event_id`: string
  - `agrees`: boolean
  - `expert_id`: string
  - `comment`: string (optional)
  - `confidence`: float (optional)

- Response format:
```json
{
  "success": boolean,
  "message": string,
  "timestamp": datetime,
  "new_probability": float,
  "expert_impact": float,
  "prediction_history": array
}
```

### Features

- **Persistent Storage**
  - All predictions stored in PostgreSQL
  - Historical tracking of changes
  - Expert performance metrics
  - Event resolution tracking

- **Expert System**
  - Dynamic weight calculation
  - Reputation scoring
  - Feedback validation
  - Anti-manipulation measures

- **Analytics**
  - Prediction accuracy tracking
  - Expert performance analysis
  - Market type specific metrics
  - Historical trend analysis

- **Security**
  - Expert authentication
  - Rate limiting
  - IP-based restrictions
  - Feedback validation


