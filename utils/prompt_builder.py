def build_prompt(field, problem, emotion, confidence):
    """
    Builds a prompt to send to Gemini AI.
    """

    prompt = f"""
You are a supportive AI Learning Assistant.

Student Academic Field:
{field}

Detected Emotion:
{emotion}

Confidence Score:
{confidence}%

Student Problem:
{problem}

Please respond with:

1. Acknowledge the student's emotion.
2. Explain the concept in a simple way.
3. Give 3 practical study tips.
4. Encourage the student to continue learning.

Keep the response positive, empathetic, and concise.
"""

    return prompt