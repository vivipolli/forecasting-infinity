import React, { useState, useEffect } from 'react';
import { EventCard } from '../components/EventCard';
import { EventFilter } from '../components/EventFilter';
import { getEvents, submitFeedback, Event } from '../services/api';

const EXPERTISE_OPTIONS = [
  'Crypto',
  'Finance',
  'Technology',
  'Politics',
  'Science',
  'Economics',
];

const Home: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        console.log('Fetching events...');
        const ongoingEvents = await getEvents();
        console.log('Received events:', ongoingEvents);
        setEvents(ongoingEvents);
        setError(null);
      } catch (error) {
        console.error('Error fetching events:', error);
        setError('Failed to load events. Please try again later.');
        setEvents([]);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  const filteredEvents = events;

  const handleFeedback = async (eventId: string, agrees: boolean) => {
    try {
      console.log('Submitting feedback for event:', eventId, agrees);
      await submitFeedback({
        event_id: eventId,
        agrees,
        expert_weight: 1.0,  // Default weight
        expert_id: 'test_expert'  // For testing, should be replaced with actual expert ID
      });
      
      console.log('Feedback submitted successfully, refreshing events...');
      const updatedEvents = await getEvents();
      setEvents(updatedEvents);
    } catch (error) {
      console.error('Error submitting feedback:', error);
      setError(error instanceof Error ? error.message : 'Failed to submit feedback');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-red-500">{error}</div>
      </div>
    );
  }

  console.log('Rendering events:', filteredEvents);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-center">Forecasting Events</h1>
      
      <EventFilter
        categories={EXPERTISE_OPTIONS}
        selectedCategory={selectedCategory}
        onCategoryChange={setSelectedCategory}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
        {filteredEvents.map((event) => (
          <EventCard
            key={event.event_id}
            eventId={event.event_id}
            description={event.description}
            probability={event.probability}
            expertValidations={0}
            onFeedback={handleFeedback}
          />
        ))}
      </div>
    </div>
  );
};

export default Home; 