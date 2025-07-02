from google.adk.agents import Agent
from vertexai.preview import reasoning_engines
from typing import Dict, Any, List


async def find_movie_showtimes(movie: str, location: str, date: str) -> dict:
    """Finds available showtimes for a given movie, location, and date."""
    print(f"[Tool Call] find_movie_showtimes(movie='{movie}', location='{location}', date='{date}')")
    if movie.lower() == "avengers: endgame" and location.lower() == "hyderabad" and date == "2025-05-15":
        
        return {"status": "success", "showtimes": ["14:00", "17:30", "21:00"]}
    else:
        return {"status": "error", "error_message": f"No showtimes found for '{movie}' in '{location}' on '{date}'."}

async def select_seats(showtime: str, num_seats: int, preferences: str = "") -> Dict[str, Any]:
    """Selects a specified number of seats for a given showtime."""
    print(f"[Tool Call] select_seats(showtime='{showtime}', num_seats={num_seats}, preferences='{preferences}')")
    if num_seats <= 2:
        selected_seats_list = ["A5", "A6"] if num_seats == 2 else ["B3"]
        return {"status": "success", "seats": selected_seats_list, "message": f"Selected {num_seats} seats..."}
    else:
        return {"status": "error", "error_message": f"Could not select {num_seats} seats... Maximum 2 allowed."}

async def confirm_booking(movie: str, showtime: str, seats: List[str]) -> dict:
    """Confirms the booking and provides a booking ID."""
    print(f"[Tool Call] confirm_booking(movie='{movie}', showtime='{showtime}', seats={seats})")
    booking_id = "BOOKING12345"
    return {"status": "success", "booking_id": booking_id, "confirmation_message": f"Your booking for '{movie}'... is confirmed."}


root_agent = Agent(
    name="movie_booking_agent",
 
    model="gemini-1.5-flash-001",
    description=("Agent to help users book movie tickets by finding showtimes, selecting seats, and confirming bookings."),
    instruction=("You are a helpful and friendly assistant for booking movie tickets..."),
    tools=[find_movie_showtimes, select_seats, confirm_booking]
)



app = reasoning_engines.make_app(root_agent)