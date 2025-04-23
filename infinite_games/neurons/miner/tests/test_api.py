import asyncio
import aiohttp
import json
from datetime import datetime

async def test_api_endpoints():
    base_url = "http://localhost:8000/api"
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Get events
        print("\nTesting GET /events endpoint...")
        try:
            async with session.get(f"{base_url}/events") as response:
                print(f"Status: {response.status}")
                
                if response.status == 200:
                    events = await response.json()
                    print(f"Number of events: {len(events)}")
                    
                    if events:
                        print("\nFirst event:")
                        print(json.dumps(events[0], indent=2))
                    else:
                        print("No events returned")
                else:
                    error_text = await response.text()
                    print(f"Error response: {error_text}")
        
        except Exception as e:
            print(f"Error during GET /events: {str(e)}")
        
        # Test 2: Submit feedback (if we have events)
        if 'events' in locals() and events:
            first_event = events[0]
            print(f"\nTesting POST /feedback endpoint for event: {first_event['question']}")
            
            feedback_data = {
                "event_id": first_event["event_id"],
                "agrees": True,
                "comment": "Test feedback from API test"
            }
            
            try:
                async with session.post(
                    f"{base_url}/feedback",
                    json=feedback_data
                ) as response:
                    print(f"Status: {response.status}")
                    
                    if response.status == 200:
                        result = await response.json()
                        print("Response:")
                        print(json.dumps(result, indent=2))
                    else:
                        error_text = await response.text()
                        print(f"Error response: {error_text}")
            
            except Exception as e:
                print(f"Error during POST /feedback: {str(e)}")
    
    print("\nAPI tests completed!")

if __name__ == "__main__":
    asyncio.run(test_api_endpoints()) 