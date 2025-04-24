import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export interface Event {
  event_id: string;
  market_type: string;
  probability: number;
  description: string;
  cutoff: string;
  status: string;
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
  comment?: string;
  expert_weight: number;
  expert_id: string;  // Required expert identifier
}

export const getEvents = async (): Promise<Event[]> => {
  try {
    const response = await axios.get(`${API_URL}/events`);
    console.log('API Response:', response.data); // Debug log
    if (!response.data || !Array.isArray(response.data)) {
      console.error('Invalid response format:', response.data);
      return [];
    }
    return response.data;
  } catch (error) {
    console.error('Error fetching events:', error);
    return [];
  }
};

export const getPredictions = async (eventId: string): Promise<EventPredictions> => {
  try {
    const response = await axios.get(`${API_URL}/events/${eventId}/predictions`);
    return response.data;
  } catch (error) {
    console.error('Error fetching predictions:', error);
    return { count: 0, predictions: [] };
  }
};

export const predictEvent = async (eventId: string): Promise<Event> => {
  const response = await axios.post(`${API_URL}/predict`, { event_id: eventId });
  return response.data;
};

export const submitFeedback = async (feedback: Feedback): Promise<boolean> => {
  try {
    if (!feedback.expert_id) {
      throw new Error('Expert ID is required');
    }
    
    const response = await axios.post(`${API_URL}/feedback`, feedback);
    console.log('Feedback response:', response.data);
    return response.data.success;
  } catch (error) {
    console.error('Error submitting feedback:', error);
    if (axios.isAxiosError(error)) {
      if (error.response?.status === 404) {
        throw new Error('Event not found');
      }
      throw new Error(error.response?.data?.detail || 'Failed to submit feedback');
    }
    throw error;
  }
};
