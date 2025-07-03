#!/usr/bin/env python3
"""
Movie Booking Agent - Generic Implementation
This is a generic agent implementation that can be deployed on various platforms
"""

from typing import Dict, Any, List
import random

class MovieBookingAgent:
    """Generic movie booking agent that can be adapted to different platforms."""
    
    def __init__(self):
        self.name = "movie_booking_agent"
        self.description = (
            "A friendly and efficient movie booking assistant that helps users find showtimes, "
            "select seats, and confirm bookings for movies in their preferred location."
        )
        # RENAMED from self.instructions to self.system_instruction for clarity and consistency
        self.system_instruction = (
            "You are a helpful and friendly assistant for booking movie tickets. "
            "Follow these guidelines:\n"
            "1. Always greet users warmly and ask for their movie preferences\n"
            "2. For finding showtimes, you need: movie name, location, and date\n"
            "3. For seat selection, ask about preferences (front/middle/back) and number of seats\n"
            "4. For booking confirmation, collect contact information if needed\n"
            "5. Always provide clear confirmations with booking IDs\n"
            "6. Be conversational and helpful throughout the process\n"
            "7. If any step fails, explain the issue and suggest alternatives\n"
            "8. Handle multiple movies or showtimes gracefully"
        )
    
    def find_movie_showtimes(self, movie: str, location: str, date: str) -> Dict[str, Any]:
        """Find movie showtimes for a given movie, location, and date."""
        print(f"[Tool Call] find_movie_showtimes(movie='{movie}', location='{location}', date='{date}')")
        if movie.lower() == "avengers: endgame" and location.lower() == "hyderabad" and date == "2025-05-15":
            return { "status": "success", "showtimes": ["14:00", "17:30", "21:00"], "theaters": ["PVR Forum Mall", "INOX GVK One", "AMB Cinemas"], "prices": {"regular": 250, "premium": 350} }
        elif "spider-man" in movie.lower() and location.lower() == "hyderabad":
            return { "status": "success", "showtimes": ["13:00", "16:30", "20:00"], "theaters": ["Prasads IMAX", "PVR Punjagutta"], "prices": {"regular": 200, "premium": 300} }
        else:
            return { "status": "error", "error_message": f"No showtimes found for '{movie}' in '{location}' on '{date}'." }

    def select_seats(self, showtime: str, num_seats: int, preferences: str = "") -> Dict[str, Any]:
        """Select seats for a movie showtime."""
        print(f"[Tool Call] select_seats(showtime='{showtime}', num_seats={num_seats}, preferences='{preferences}')")
        if num_seats <= 2:
            if preferences.lower() == "front": selected_seats_list = ["C5", "C6"] if num_seats == 2 else ["C5"]
            elif preferences.lower() == "back": selected_seats_list = ["H5", "H6"] if num_seats == 2 else ["H5"]
            else: selected_seats_list = ["E5", "E6"] if num_seats == 2 else ["E5"]
            return { "status": "success", "seats": selected_seats_list, "message": f"Selected {num_seats} seats ({', '.join(selected_seats_list)}) for {showtime} showtime.", "preferences_applied": preferences if preferences else "middle section (default)"}
        else:
            return { "status": "error", "error_message": f"Could not select {num_seats} seats for {showtime}. Maximum 2 seats allowed in this demo." }

    def confirm_booking(self, movie: str, showtime: str, seats: List[str], contact_info: str = "") -> Dict[str, Any]:
        """Confirm the movie booking."""
        print(f"[Tool Call] confirm_booking(movie='{movie}', showtime='{showtime}', seats={seats}, contact='{contact_info}')")
        booking_id = f"BK{random.randint(100000, 999999)}"
        return { "status": "success", "booking_id": booking_id, "confirmation_message": (f"✅ Your booking for '{movie}' at {showtime} in seats {', '.join(seats)} is confirmed! Booking ID: {booking_id}. Please arrive 15 minutes before the show time."), "booking_details": { "movie": movie, "showtime": showtime, "seats": seats, "booking_id": booking_id, "contact": contact_info } }
    
    def get_tools(self):
        """Return the list of tools/functions available to this agent."""
        return [ self.find_movie_showtimes, self.select_seats, self.confirm_booking ]
    
    def get_config(self):
        """Return agent configuration."""
        return {
            "name": self.name,
            "description": self.description,
            # THE FIX: Use the correct key 'system_instruction'
            "system_instruction": self.system_instruction,
            "tools": self.get_tools()
        }

# Create agent instance - this is what the deployment script looks for
agent = MovieBookingAgent()