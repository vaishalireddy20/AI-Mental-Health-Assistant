def detect_crisis(text):

    text=text.lower()

    crisis_words=[
    "suicide",
    "kill myself",
    "end my life",
    "want to die",
    "no reason to live"
    ]

    for word in crisis_words:
        if word in text:
            return True

    return False
