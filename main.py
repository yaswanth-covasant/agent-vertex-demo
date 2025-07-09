# main.py

from google.adk.agents import Agent
from google.adk.cli.fast_api import get_fast_api_app
from typing import Dict, Any, List
from fastapi import FastAPI
import uvicorn

# --- Tool Functions (Your core logic) ---
# (This code is identical to what you provided)

async def find_movie_showtimes(movie: str, location: str, date: str) -> dict:
    """Finds movie showtimes for a given movie, location, and date."""
    print(f"[Tool Call] find_movie_showtimes(movie='{movie}', location='{location}', date='{date}')")
    if movie.lower() == "avengers: endgame" and location.lower() == "hyderabad" and date == "2025-05-15":
        return {
            "status": "success",
            "showtimes": ["14:00", "17:30", "21:00"],
        }
    else:
        return {
            "status": "error",
            "error_message": f"No showtimes found for '{movie}' in '{location}' on '{date}'.",
        }

async def select_seats(showtime: str, num_seats: int, preferences: str = "") -> Dict[str, Any]:
    """Selects a specified number of seats for a given showtime."""
    print(f"[Tool Call] select_seats(showtime='{showtime}', num_seats={num_seats}, preferences='{preferences}')")
    if num_seats <= 2:
        selected_seats_list = ["A5", "A6"] if num_seats == 2 else ["B3"]
        return {
            "status": "success",
            "seats": selected_seats_list,
            "message": f"Selected {num_seats} seats ({', '.join(selected_seats_list)}) for {showtime} (preferences: {preferences if preferences else 'none'}).",
        }
    else:
        return {
            "status": "error",
            "error_message": f"Could not select {num_seats} seats for {showtime}. Maximum 2 seats allowed in this demo.",
        }

async def confirm_booking(movie: str, showtime: str, seats: List[str]) -> dict:
    """Confirms a booking for a movie, showtime, and selected seats."""
    print(f"[Tool Call] confirm_booking(movie='{movie}', showtime='{showtime}', seats={seats})")
    booking_id = "BOOKING12345"
    return {
        "status": "success",
        "booking_id": booking_id,
        "confirmation_message": (
            f"Your booking for '{movie}' at {showtime} in seats {', '.join(seats)} is confirmed."
            f" Your booking ID is {booking_id}."
        ),
    }

# --- Agent and App Definition ---

# Define the agent's high-level configuration. The deployment process will
# use this definition when creating the agent engine.
root_agent = Agent(
    name="movie_booking_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to help users book movie tickets by finding showtimes, selecting seats, and confirming bookings."
    ),
    instruction=(
        "You are a helpful and friendly assistant for booking movie tickets. "
        "Use the available tools to find showtimes, select seats, and confirm bookings based on the user's requests. "
        "Ensure you gather all necessary information for each step. For example, to find showtimes, you need the movie, location, and date. "
        "For seat selection, you need the showtime and number of seats. For booking confirmation, you need movie, showtime, and the list of selected seats."
    ),
    tools=[find_movie_showtimes, select_seats, confirm_booking]
)

# Create a FastAPI app instance
app = FastAPI()

# Use the ADK utility to automatically create the required
# /health, /tools, and /execute_tool endpoints.
get_fast_api_app(app, root_agent)

# Optional: Add a main entrypoint for local testing
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)