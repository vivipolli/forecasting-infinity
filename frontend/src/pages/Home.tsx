import React, { useState, useMemo } from 'react';
import { EventCard } from '../components/EventCard';
import { EventFilter } from '../components/EventFilter';
import { mockEvents } from '../mocks/events';

const Home: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const categories = useMemo(() => {
    const uniqueCategories = new Set(mockEvents.map(event => event.category));
    return Array.from(uniqueCategories).sort();
  }, []);

  const filteredEvents = useMemo(() => {
    if (!selectedCategory) return mockEvents;
    return mockEvents.filter(event => event.category === selectedCategory);
  }, [selectedCategory]);

  const handleFeedback = async (eventId: string, agrees: boolean) => {
    try {
      const response = await fetch('http://localhost:8000/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          event_id: eventId,
          agrees,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to submit feedback');
      }
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">Active Events</h1>
        <div className="text-white/50">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>

      <EventFilter
        categories={categories}
        selectedCategory={selectedCategory}
        onCategoryChange={setSelectedCategory}
      />

      <div className="space-y-4">
        {filteredEvents.map((event) => (
          <EventCard
            key={event.eventId}
            eventId={event.eventId}
            question={event.question}
            probability={event.probability}
            context={event.context}
            category={event.category}
            expertValidations={event.expertValidations || 0}
            onFeedback={(agrees: boolean) => handleFeedback(event.eventId, agrees)}
          />
        ))}
      </div>
    </div>
  );
};

export default Home; 