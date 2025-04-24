import axios from 'axios';

const BASE_URL = 'https://ifgames.win/api/v2';

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
  probability?: number;
  status?: string;
}

export class EventsService {
  static async getOngoingEvents(limit: number = 25, offset: number = 0): Promise<Event[]> {
    try {
      const response = await axios.get(`${BASE_URL}/events`, {
        params: {
          from_date: 1,
          offset,
          limit
        }
      });
      return (response.data.items || []).map((event: any) => ({
        ...event,
        probability: event.probability || 0.5 // Default to 0.5 if not present
      }));
    } catch (error) {
      console.error('Error fetching ongoing events:', error);
      return [];
    }
  }

  static async getResolvedEvents(limit: number = 100, offset: number = 0): Promise<Event[]> {
    try {
      const response = await axios.get(`${BASE_URL}/events/resolved`, {
        params: {
          offset,
          resolved_since: 1,
          limit
        }
      });
      return (response.data.items || []).map((event: any) => ({
        ...event,
        probability: event.probability || 0.5 // Default to 0.5 if not present
      }));
    } catch (error) {
      console.error('Error fetching resolved events:', error);
      return [];
    }
  }

  static async getEventPredictions(eventId: string): Promise<{ predictions: any[] }> {
    try {
      const response = await axios.get(`${BASE_URL}/events/${eventId}/predictions`);
      return {
        predictions: (response.data.predictions || []).map((pred: any) => ({
          ...pred,
          prediction: pred.prediction || 0.5 // Default to 0.5 if not present
        }))
      };
    } catch (error) {
      console.error('Error fetching event predictions:', error);
      return { predictions: [] };
    }
  }

  static async submitFeedback(eventId: string, agrees: boolean, expertId: string): Promise<boolean> {
    try {
      const response = await axios.post(`${BASE_URL}/events/${eventId}/feedback`, {
        agrees,
        expert_id: expertId
      });
      return response.data.success;
    } catch (error) {
      console.error('Error submitting feedback:', error);
      return false;
    }
  }
} 