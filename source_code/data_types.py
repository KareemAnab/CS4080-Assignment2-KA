#ChatGPT was used as aid to solve this problem

from __future__ import annotations
from enum import Enum
from datetime import datetime
from typing import Any, Dict

# Enumeration of the kinds of requests the assistant can handle.
class CommandType(Enum):
    PLAY_MUSIC = "play_music"
    SUGGEST_WORKOUT = "suggest_workout"
    SCHEDULE_STUDY = "schedule_study"


class UserProfile:
    """
    Holds information about a user.
      - name: non-empty string
      - age: positive integer
      - preferences: dict of arbitrary settings
      - is_premium: boolean flag
    """

    def __init__(
        self,
        name: str,
        age: int,
        preferences: Dict[str, Any],
        is_premium: bool
    ):
        # Basic type & value validations:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("UserProfile.name must be a non-empty string")
        if not isinstance(age, int) or age <= 0:
            raise ValueError("UserProfile.age must be a positive integer")
        if not isinstance(preferences, dict):
            raise ValueError("UserProfile.preferences must be a dict")
        if not isinstance(is_premium, bool):
            raise ValueError("UserProfile.is_premium must be a boolean")

        self.name        = name.strip()
        self.age         = age
        self.preferences = preferences
        self.is_premium  = is_premium

    def __repr__(self) -> str:
        return (
            f"UserProfile(name={self.name!r}, age={self.age}, "
            f"is_premium={self.is_premium}, preferences={self.preferences})"
        )


class Request:
    """
    Represents an incoming user request.
      - text: the raw input string
      - timestamp: when the request was created
      - command: a CommandType enum
    """

    def __init__(
        self,
        text: str,
        timestamp: datetime,
        command: CommandType
    ):
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Request.text must be a non-empty string")
        if not isinstance(timestamp, datetime):
            raise ValueError("Request.timestamp must be a datetime object")
        if not isinstance(command, CommandType):
            raise ValueError("Request.command must be a CommandType enum")

        self.text      = text.strip()
        self.timestamp = timestamp
        self.command   = command

    def __repr__(self) -> str:
        return (
            f"Request(text={self.text!r}, "
            f"timestamp={self.timestamp.isoformat()}, "
            f"command={self.command})"
        )


class Response:
    """
    Represents the assistant’s reply.
      - message: the text to show the user
      - confidence: between 0.0 and 1.0
      - action_performed: True if the assistant actually did something
    """

    def __init__(
        self,
        message: str,
        confidence: float = 1.0,
        action_performed: bool = True
    ):
        if not isinstance(message, str) or not message.strip():
            raise ValueError("Response.message must be a non-empty string")
        if (
            not isinstance(confidence, (int, float))
            or not (0.0 <= confidence <= 1.0)
        ):
            raise ValueError("Response.confidence must be between 0.0 and 1.0")
        if not isinstance(action_performed, bool):
            raise ValueError("Response.action_performed must be a boolean")

        self.message          = message.strip()
        self.confidence       = float(confidence)
        self.action_performed = action_performed

    def __repr__(self) -> str:
        return (
            f"Response(message={self.message!r}, "
            f"confidence={self.confidence:.2f}, "
            f"action_performed={self.action_performed})"
        )
