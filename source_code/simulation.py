#ChatGPT was used as aid to solve this problem

import re
from datetime import datetime, timedelta
from random import choice, randint

from data_types import UserProfile, Request, Response, CommandType
from ai_assistants import MusicAssistant, FitnessAssistant

def parse_command(text: str) -> CommandType:
    """
    Very simple keyword-based intent classifier.
    """
    t = text.lower()
    if re.search(r"\b(play|song|music)\b", t):
        return CommandType.PLAY_MUSIC
    if re.search(r"\b(workout|exercise|strength|endurance)\b", t):
        return CommandType.SUGGEST_WORKOUT
    if re.search(r"\b(study|learn|explain)\b", t):
        return CommandType.SCHEDULE_STUDY
    # fallback
    return CommandType.PLAY_MUSIC

def simulate_user_interaction(user: UserProfile, utterance: str):
    """
    Given a user and raw text utterance, parse it into a Request,
    pick the right assistant, and print its response.
    """
    cmd = parse_command(utterance)
    req = Request(text=utterance, timestamp=datetime.now(), command=cmd)

    # Choose assistant based on detected intent:
    if cmd == CommandType.PLAY_MUSIC:
        bot = MusicAssistant(user)
    elif cmd == CommandType.SUGGEST_WORKOUT:
        bot = FitnessAssistant(user)
    else:
        bot = MusicAssistant(user)  # fallback to music for demonstration

    # Greet once per session
    print(f"[{user.name}] {bot.greet_user()}")
    # Handle & generate
    res = bot.handle_request(req)
    print(f"[{user.name} → {cmd.name}] {res.message}\n")

def main():
    # Create several users with different prefs
    users = [
        UserProfile("Alice", age=30, preferences={"genre":"jazz",   "goal":"strength"}, is_premium=True),
        UserProfile("Bob",   age=22, preferences={"genre":"rock",   "goal":"endurance"}, is_premium=False),
        UserProfile("Cara",  age=27, preferences={"genre":"classical","goal":"flexibility"}, is_premium=True),
    ]

    # Each user makes a random set of utterances
    sample_utterances = [
        "Hey, play some music for me",
        "I want a strength workout routine",
        "Can you help me study OOP concepts?",
        "Give me a pop playlist",
        "Suggest an endurance exercise plan",
        "Explain polymorphism in simple terms",
    ]

    # Simulate
    for user in users:
        print("=== Session for", user.name, "===\n")
        for _ in range(3):
            text = choice(sample_utterances)
            simulate_user_interaction(user, text)
        print("\n")

if __name__ == "__main__":
    main()
