from textblob import TextBlob

def detect_emotion(text):

    analysis = TextBlob(text)

    polarity = analysis.sentiment.polarity

    if polarity > 0.3:
        return "Happy"

    elif polarity < -0.3:
        return "Sad"

    else:
        return "Neutral"
