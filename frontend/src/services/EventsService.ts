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
      return response.data.items || [];
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
      return response.data.items || [];
    } catch (error) {
      console.error('Error fetching resolved events:', error);
      return [];
    }
  }
} 