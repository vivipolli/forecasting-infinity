import { EventsService } from './EventsService';

// Configuration
const USE_DIRECT_API = true; // Set to false to use local miner
const API_URL = 'http://localhost:8000/api';

export interface Event {
  event_id: string;
  market_type: string;
  title: string;
  description: string;
  cutoff: number;
  start_date: number;
  created_at: number;
  end_date: number;
  answer: string | null;
  probability?: number; // Optional as it's not in the API response
  status?: string; // Optional as it's not in the API response
}

export interface Prediction {
  prediction: number;
  timestamp: string;
  expert_id?: string;
}

export interface EventPredictions {
  count: number;
  predictions: Prediction[];
}

export interface Feedback {
  event_id: string;
  agrees: boolean;
  expert_id: string;
}

export const getEvents = async (): Promise<Event[]> => {
  try {
    if (USE_DIRECT_API) {
      return await EventsService.getOngoingEvents();
    }
    const response = await fetch(`${API_URL}/events`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching events:', error);
    return [];
  }
};

export const getPredictions = async (eventId: string): Promise<EventPredictions> => {
  try {
    if (USE_DIRECT_API) {
      const predictions = await EventsService.getEventPredictions(eventId);
      return {
        count: predictions.predictions.length,
        predictions: predictions.predictions
      };
    }
    const response = await fetch(`${API_URL}/events/${eventId}/predictions`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching predictions:', error);
    return { count: 0, predictions: [] };
  }
};

export const predictEvent = async (eventId: string): Promise<Event> => {
  const response = await fetch(`${API_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ event_id: eventId }),
  });
  return await response.json();
};

export const submitFeedback = async (feedback: Feedback): Promise<boolean> => {
  try {
    if (!feedback.expert_id) {
      throw new Error('Expert ID is required');
    }
    
    if (USE_DIRECT_API) {
      return await EventsService.submitFeedback(
        feedback.event_id,
        feedback.agrees,
        feedback.expert_id
      );
    }
    
    const response = await fetch(`${API_URL}/feedback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(feedback),
    });
    const data = await response.json();
    return data.success;
  } catch (error) {
    console.error('Error submitting feedback:', error);
    throw error;
  }
};
