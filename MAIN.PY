import pyttsx3
import speech_recognition as sr
import webbrowser
import time
import datetime
import feedparser
import pywhatkit
from google import genai
import pyautogui
# import pvporcupine
import pyaudio
import struct


def speak(text):
    engine = pyttsx3.init('sapi5')
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[0].id)
    engine.setProperty('volume', 1.0)
    engine.setProperty('rate', 155)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


is_playing = False
song_start_time = 0
song_duration = 190
song_buffer = 1
recognize = sr.Recognizer()
def open_chrome():
    speak("Opening Chrome")
    webbrowser.open("https://www.google.com")

def open_youtube():
    speak("Opening YouTube")
    webbrowser.open("https://www.youtube.com")

def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    speak(f"The current time is {current_time}")

def play_music(c):
    global is_playing, song_start_time

    song = c.lower().replace("play", "").strip()
    print("SONG COMMAND =", song)

    if song:
        speak("playing " + song)

        try:
            # agar pehle se song chal raha hai → tab close karo
            if is_playing:
                import pyautogui
                pyautogui.hotkey("ctrl", "w")   # current tab close
                time.sleep(2)

            # naya song play
            pywhatkit.playonyt(song)

            time.sleep(10)   # load hone ka wait
            is_playing = True
            song_start_time = time.time()

        except Exception as e:
            print("ERROR:", e)
            speak("song change nahi ho paya boss")

    else:
        speak("song name bolo boss")
def pause_song():
    pyautogui.press("k")
    speak("music stopped")

def resume_song():
    pyautogui.press("k")
    speak("music started")

def tell_news():
    speak("fetching latest news")

    news_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(news_url)

    count = 0
    for entry in feed.entries:
        if count == 5:
            break
        speak(entry.title)
        print(entry.title)
        count += 1

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")
def ai_brain(question):
    try:
        response = model.generate_content(question)
        reply = response.text
        print("AI:", reply)
        return reply
    except Exception as e:
        print("Error:", e)
        return "Sorry boss, AI error."
    
if __name__ == "__main__":
    speak("Initializing jarvis")
    access_key = " access key "

    porcupine = pvporcupine.create(
        access_key=access_key,
        keywords=["jarvis"]
    )

    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    time.sleep(1)
    while True:
        try:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h"*porcupine.frame_length, pcm)
            result = porcupine.process(pcm)
            if is_playing:
                if time.time()> song_start_time + song_duration:
                    is_playing = False
                    speak("boss i am back")
                else:
                    time.sleep(5)
                    continue


            if result >= 0:
                speak("yes boss")

                with sr.Microphone() as source:
                    recognize.adjust_for_ambient_noise(source, duration=1)
                    audio = recognize.listen(source, phrase_time_limit=5)
            else:
                continue
            word = recognize.recognize_google(audio).lower()
            word = word.lower().strip()
            print("heard:", word)

            if "stop" in word:
                speak("stopping jarvis")
                break

            if "jarvis" in word:
                time.sleep(0.3)
                speak("yes boss")

            if "how are you" in word:
                time.sleep(0.3)
                speak("i am good sir what about you")

            if "i am also good" in word:
                time.sleep(0.3)
                speak("sounds good sir")

            
             # COMMANDS
            if "open chrome" in word:
                open_chrome()
            if "open youtube" in word:
                open_youtube()
            if "what is the time" in word:
                tell_time()
            if "open google" in word:
                speak("Opening Google")
                webbrowser.open("https://www.google.com")
            if "play" in word:
                play_music(word)
                continue

            
            if "news" in word:
                tell_news()

            # if any(k in word for k in ai_words):
            #     ai_brain(word)

        except Exception as e:
            print("error",e)