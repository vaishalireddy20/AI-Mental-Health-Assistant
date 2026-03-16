import speech_recognition as sr

def get_voice_text():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except:
        return ""
