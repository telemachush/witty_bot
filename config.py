"""
Configuration for the Slack Status Bot
"""

import os
from typing import Dict, List

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "templates")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LOCAL_MODEL_NAME = os.getenv("LOCAL_MODEL_NAME", "distilbert-base-uncased")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

# Status Types and their descriptions
STATUS_TYPES = {
    "lunch": "Eating lunch",
    "dinner": "Eating dinner",
    "short_break": "Taking a short break",
    "break": "Taking a break",
    "long_break": "Taking a long break",
    "coffee": "Getting coffee or a drink",
    "walk": "Taking a walk or exercise break",
    "errands": "Running errands or out of office",
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
    "lunch": [
        "Eating my feelings",
        "Fueling up for the afternoon",
        "Pretending this is healthy",
        "Lunch break (the highlight of my day)",
        "Eating and scrolling",
        "Refueling the machine",
        "Taking a food break",
        "Lunch time adventures",
        "Chewing and contemplating life",
        "Midday fuel injection"
    ],
    "dinner": [
        "Dinner time - adulting at its finest",
        "Cooking up some magic",
        "Evening fuel for tomorrow",
        "Dinner and daydreaming",
        "Chef mode activated",
        "Evening sustenance ritual",
        "Dinner date with my kitchen",
        "Cooking my way to happiness"
    ],
    "short_break": [
        "Quick mental reset",
        "Brief pause for sanity",
        "Micro-break for maximum focus",
        "Quick escape from reality",
        "Brief moment of peace",
        "Short break, long thoughts",
        "Quick recharge session",
        "Brief pause for perspective"
    ],
    "break": [
        "Taking a mental health break",
        "Stretching my legs (and brain)",
        "Quick break to reset",
        "Pretending to be busy",
        "Taking a moment",
        "Recharging my batteries",
        "Quick escape",
        "Break time bliss",
        "Pause for the cause",
        "Break time - brain maintenance"
    ],
    "long_break": [
        "Extended mental vacation",
        "Long break for deep thoughts",
        "Extended recharge session",
        "Long pause for perspective",
        "Extended escape from reality",
        "Long break, longer thoughts",
        "Extended mental reset",
        "Long break for maximum zen"
    ],
    "coffee": [
        "Caffeinated and confused",
        "Coffee break - sanity restored",
        "Fueled by caffeine and hope",
        "Coffee time - adulting properly",
        "Caffeinated and ready for chaos",
        "Coffee break for clarity",
        "Fueled by beans and dreams",
        "Coffee time - brain activation"
    ],
    "walk": [
        "Walking and thinking",
        "Exercise break for sanity",
        "Walking my way to clarity",
        "Fresh air and fresh thoughts",
        "Walking break - nature therapy",
        "Exercise mode activated",
        "Walking and daydreaming",
        "Fresh air for fresh ideas"
    ],
    "errands": [
        "Adulting in progress",
        "Running errands like a grown-up",
        "Errand time - life admin",
        "Adult responsibilities calling",
        "Errand break - real world stuff",
        "Life admin in progress",
        "Errand time - adulting properly",
        "Running errands, avoiding work"
    ],
    "travel": [
        "Traveling and working remotely",
        "On the road to somewhere",
        "Travel mode activated",
        "Working from the road",
        "Traveling and contemplating life",
        "On the move and online",
        "Travel break - exploring life",
        "Working from anywhere"
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