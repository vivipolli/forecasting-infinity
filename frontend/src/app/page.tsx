'use client';

import React from 'react';
import { Layout } from '@/components/Layout';
import { EventCard } from '@/components/EventCard';

// Mock data - replace with actual API calls
const mockEvents = [
  {
    eventId: '1',
    question: 'Will Bitcoin reach $100,000 by the end of 2024?',
    probability: 0.73,
    context: 'Based on current market trends and historical data...',
    category: 'Crypto',
  },
  {
    eventId: '2',
    question: 'Will the Federal Reserve cut interest rates in Q2 2024?',
    probability: 0.45,
    context: 'Considering current inflation rates and economic indicators...',
    category: 'Finance',
  },
];

export default function Home() {
  const handleFeedback = async (eventId: string, agrees: boolean) => {
    try {
      const response = await fetch('/api/feedback', {
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
    <Layout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-white">Active Events</h1>
          <div className="text-white/50">
            Last updated: {new Date().toLocaleTimeString()}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mockEvents.map((event) => (
            <EventCard
              key={event.eventId}
              eventId={event.eventId}
              question={event.question}
              probability={event.probability}
              context={event.context}
              category={event.category}
              onFeedback={(agrees) => handleFeedback(event.eventId, agrees)}
            />
          ))}
        </div>
      </div>
    </Layout>
  );
} 