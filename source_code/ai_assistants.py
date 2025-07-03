#ChatGPT was used as aid to solve this problem

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from data_types import UserProfile, Request, Response, CommandType


# Base class for all assistants.
class AIAssistant(ABC):
    def __init__(self, user: UserProfile):
        self.user = user

    # Return a greeting for the user.
    def greet_user(self) -> str:
        return f"Hello, {self.user.name}! What can I do for you today?"


    # Top-level entrypoint for processing a request.
    # Subclasses should override this to dispatch to generate_response.
    @abstractmethod
    def handle_request(self, request: Request) -> Response:
        pass

    # Produce a Response object based on the request.
    @abstractmethod
    def generate_response(self, request: Request) -> Response:
        pass

# Recommends songs based on user’s mood/genre preference.
class MusicAssistant(AIAssistant):
    def __init__(self, user: UserProfile):
        super().__init__(user)
        # simple hard-coded mapping genre→playlist
        self.playlists = {
            "pop":    ["Blinding Lights – The Weeknd", "The Lazy Song– Bruno Mars"],
            "rock":   ["Hotel California – Eagles", "Do I Wanna Know? – Arctic Monkeys"],
            "jazz":   ["So What – Miles Davis", "Take Five – Dave Brubeck"],
            "classical": ["Moonlight Sonata – Beethoven", "Clair de Lune – Debussy"],
        }

    # Return a list of 5 songs for the requested genre.
    # Defaults to 'pop' if unknown.
    def recommend_playlist(self, genre: str) -> List[str]:
        return self.playlists.get(genre.lower(), self.playlists["pop"])

    def handle_request(self, request: Request) -> Response:
        # only handle PLAY_MUSIC commands
        if request.command != CommandType.PLAY_MUSIC:
            return Response(
                message="Sorry, I can only handle music requests right now.",
                confidence=0.0,
                action_performed=False
            )
        return self.generate_response(request)

    def generate_response(self, request: Request) -> Response:
        # assume request.text contains the desired genre or mood
        genre = self.user.preferences.get("genre", "pop")
        playlist = self.recommend_playlist(genre)
        msg = (
            f"Here is your {genre.title()} playlist:\n"
            + "\n".join(f" - {song}" for song in playlist)
        )
        return Response(message=msg, confidence=0.9, action_performed=True)

# Suggests simple workouts based on user’s goal.
class FitnessAssistant(AIAssistant):
    def __init__(self, user: UserProfile):
        super().__init__(user)
        # hard-coded workout routines
        self.workouts = {
            "strength": "3×5 heavy squats, 3×5 bench press, 3×5 deadlift",
            "endurance": "30-minute run, 15-minute bike, 10-minute jump rope",
            "flexibility": "20-minute yoga flow, 10-minute stretching",
        }

    # Return a workout routine for the given goal.
    # Defaults to 'endurance' if unknown.
    def suggest_workout(self, goal: str) -> str:
        return self.workouts.get(goal.lower(), self.workouts["endurance"])

    def handle_request(self, request: Request) -> Response:
        if request.command != CommandType.SUGGEST_WORKOUT:
            return Response(
                message="I’m not set up for that request.",
                confidence=0.0,
                action_performed=False
            )
        return self.generate_response(request)

    def generate_response(self, request: Request) -> Response:
        # assume user.preferences["goal"] holds their fitness goal
        goal = self.user.preferences.get("goal", "endurance")
        routine = self.suggest_workout(goal)
        msg = f"Here’s a {goal.title()} routine for you:\n{routine}"
        return Response(message=msg, confidence=0.85, action_performed=True)
