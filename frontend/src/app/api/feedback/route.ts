import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { event_id, agrees } = body;

    // Here you would typically make a request to your backend API
    // For now, we'll just log the feedback
    console.log('Received feedback:', { event_id, agrees });

    return NextResponse.json(
      { success: true, message: 'Feedback submitted successfully' },
      { status: 200 }
    );
  } catch (error) {
    console.error('Error processing feedback:', error);
    return NextResponse.json(
      { success: false, message: 'Failed to process feedback' },
      { status: 500 }
    );
  }
} 