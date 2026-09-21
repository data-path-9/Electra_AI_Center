"""Friendly Greeter Plugin – fills the missing handler for simple greetings.

This plugin intercepts common greeting phrases and returns a friendly response.
It is safe, lightweight, and never crashes the host application.
"""

import os
import random
from typing import Dict, List

# -------------------- Plugin Metadata --------------------
PLUGIN_NAME = "Friendly Greeter"
PLUGIN_VERSION = "1.0.0"
PLUGIN_DESCRIPTION = "Handles simple greetings and small‑talk requests."
PLUGIN_AUTHOR = "AutoRepair"
PLUGIN_ENABLED = True
PLUGIN_TYPE = "ROUTER"

# Triggers that will activate this router.  They cover the most common
# greeting utterances.  The router matches case‑insensitively.
PLUGIN_TRIGGERS = [
    "hi",
    "hello",
    "hey",
    "greetings",
    "good morning",
    "good evening",
    "what's up",
    "whats up",
    "how are you",
    "how's it going",
    "how are things",
]

# Unique token used by the router to identify this plugin.
PLUGIN_ROUTE_TOKEN = "GREETER"

# Optional slash‑command registration (none needed for a simple greeter).
PLUGIN_COMMANDS = []


# -------------------- Helper Functions --------------------
def _choose_response(prompt: str) -> str:
    """Select a friendly reply based on the incoming prompt."""
    lowered = prompt.lower().strip()

    # Simple pattern matching – more can be added later.
    if any(greet in lowered for greet in ("good morning", "morning")):
        return random.choice(
            [
                "Good morning! ☀️ How can I help you today?",
                "Morning! Ready to tackle anything you need.",
                "Top of the morning to you! What’s on your mind?",
            ]
        )
    if any(greet in lowered for greet in ("good evening", "evening")):
        return random.choice(
            [
                "Good evening! 🌙 How may I assist you?",
                "Evening! Let me know what you’d like to do.",
                "Hope you’re having a pleasant evening. What can I do for you?",
            ]
        )
    if any(greet in lowered for greet in ("how are you", "how's it going", "how are things")):
        return random.choice(
            [
                "I’m doing great, thanks for asking! How about you?",
                "All systems operational. How can I help?",
                "Feeling ready to assist! What would you like to discuss?",
            ]
        )
    if any(greet in lowered for greet in ("what's up", "whats up", "what up")):
        return random.choice(
            [
                "Just here, ready to help! What’s on your agenda?",
                "Nothing much, just waiting for your next command.",
                "Ready when you are – what would you like to do?",
            ]
        )
    # Default generic greeting
    return random.choice(
        [
            "Hello! How can I assist you today?",
            "Hi there! What would you like to talk about?",
            "Hey! Let me know what you need.",
        ]
    )


# -------------------- Main Entry Point --------------------
def run(prompt: str, context: Dict) -> str:
    """
    Entry point called by Electra when a trigger matches.

    Parameters
    ----------
    prompt: str
        The raw user input that matched one of PLUGIN_TRIGGERS.
    context: dict
        Runtime context supplied by Electra (see spec v2.1).

    Returns
    -------
    str
        A friendly response string. Must be non‑empty.
    """
    try:
        # Use the provided print function for progressive feedback (optional).
        # Here we just send a single line, but the pattern is kept for consistency.
        response = _choose_response(prompt)

        # If the host app expects progressive output, we can emit it now.
        if "print_fn" in context and callable(context["print_fn"]):
            context["print_fn"](response)

        return response
    except Exception as e:
        # Never let an exception escape – return a safe fallback message.
        fallback = "Sorry, I ran into an unexpected issue. How can I help you otherwise?"
        if "print_fn" in context and callable(context["print_fn"]):
            try:
                context["print_fn"](fallback)
            except Exception:
                pass
        return fallback