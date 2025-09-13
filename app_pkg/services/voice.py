from threading import Lock
import requests
import speech_recognition as sr
import pyttsx3 as t


API_KEY = "JJT2oAUiJNKaEzkGAcP0PpzZ1hBoExqz"
API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

tts_lock = Lock()
mic_lock = Lock()

engine = t.init()
engine.setProperty('rate', 150)
recognizer = sr.Recognizer()


def speak_text(text: str) -> None:
    with tts_lock:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass


def process_voice() -> str:
    with mic_lock:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = recognizer.listen(source, timeout=5)
                return recognizer.recognize_google(audio)
            except sr.WaitTimeoutError:
                return "No speech detected"
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError as e:
                return f"Recognition error: {str(e)}"


def get_ai_response(user_input: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [
            {"role": "system", "content": "You are a medical assistant."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    try:
        response = requests.post(API_URL, json=prompt, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "The request timed out. Please try again."
    except requests.exceptions.RequestException:
        return "AI error: Please try again later."


