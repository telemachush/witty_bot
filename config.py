"""
Configuration for the Slack Status Bot
"""

import os
from typing import Dict, List

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LOCAL_MODEL_NAME = os.getenv("LOCAL_MODEL_NAME", "distilbert-base-uncased")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2:7b")

# Status Types and their descriptions
STATUS_TYPES = {
    "busy": "Working hard on something important",
    "away": "Not available",
    "lunch": "Eating lunch/dinner",
    "short_break": "Taking a short break",
    "break": "Taking a break",
    "long_break": "Taking a long break",
    "coffee": "Getting coffee or a drink",
    "walk": "Taking a walk or exercise break",
    "errands": "Running errands or out of office",
    "sick": "Sick or not feeling well",
    "travel": "Traveling or on the road",
}

# Professional boundaries - words/phrases to avoid
UNPROFESSIONAL_WORDS = [
    "shit", "fuck", "damn", "hell", "bitch", "ass", "piss", "crap",
    "going for a shit", "taking a dump", "bathroom break",
    "drunk", "high", "stoned", "wasted",
    "hate", "kill", "die", "death"
]

# Funny but professional status templates
STATUS_TEMPLATES = {
    "busy": [
        "Drowning in code and loving it",
        "Debugging my life choices",
        "In a meeting that could have been an email",
        "Pretending to understand this code",
        "Fighting with my computer",
        "Making the magic happen",
        "Deep in the matrix",
        "Caffeinated and confused"
    ],
    "away": [
        "Probably getting coffee",
        "Lost in thought (and space)",
        "Taking a mental health break",
        "Pretending to be productive",
        "Staring at walls",
        "Questioning my career choices",
        "On a walk to clear my head",
        "Probably napping"
    ],
    "meeting": [
        "In a meeting that could have been an email",
        "Pretending to pay attention",
        "Counting ceiling tiles",
        "Planning my escape route",
        "Taking notes (of my grocery list)",
        "In a very important meeting",
        "Discussing things that matter",
        "Collaborating (or trying to)"
    ],
    "lunch": [
        "Eating my feelings",
        "Fueling up for the afternoon",
        "Pretending this is healthy",
        "Lunch break (the highlight of my day)",
        "Eating and scrolling",
        "Refueling the machine",
        "Taking a food break",
        "Lunch time adventures"
    ],
    "focus": [
        "Do not disturb (seriously)",
        "In the zone (or trying to be)",
        "Deep work mode activated",
        "Pretending to be productive",
        "Focused and fabulous",
        "In my element",
        "Making things happen",
        "Concentration station"
    ],
    "break": [
        "Taking a mental health break",
        "Stretching my legs (and brain)",
        "Quick break to reset",
        "Pretending to be busy",
        "Taking a moment",
        "Recharging my batteries",
        "Quick escape",
        "Break time bliss"
    ]
}

# LLM Prompt template
PROMPT_TEMPLATE = """
You are a professional but funny status message generator for Slack. 
Generate a humorous but appropriate status message for a {status_type} situation.

Context: {context}

Requirements:
- Keep it professional (no profanity or inappropriate content)
- Make it funny and relatable
- Keep it under 50 characters
- Be creative and original
- Avoid: {avoid_words}

Generate only the status message, nothing else:
""" 