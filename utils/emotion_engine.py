import random

def get_emotion_and_confidence(text):
    text = text.lower()

    if "confused" in text or "don't understand" in text:
        return "Confused", random.randint(30, 40)

    if "frustrated" in text or "hard" in text or "difficult" in text:
        return "Frustrated", random.randint(50, 60)

    if "love" in text or "easy" in text or "clear" in text:
        return "Confident", random.randint(85, 98)

    if "curious" in text or "why" in text:
        return "Curious", random.randint(90, 95)

    return "Bored", random.randint(60, 70)