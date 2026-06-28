from utils.response_templates import templates


def get_response(emotion):
    """
    Returns a template response based on emotion.
    """

    if emotion in templates:
        return templates[emotion]

    return {
        "emoji": "🙂",
        "response": "Keep learning and never give up!"
    }