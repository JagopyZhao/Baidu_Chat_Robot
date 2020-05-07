# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 16:10:29 2020

@author: Zhao
"""

import speech_recognition as sr
import requests
import json
import pyaudio
import wave
import os
import time
from aip import AipSpeech

APP_ID = '15886117'
API_KEY = 'mxMjmaZh7bjVppc3UXE588iD'
SECRET_KEY = 'I5meO0pDg1DNK9wZE3rIo5jYo7VP8wTp'

TURING_KEY = "23a6c7901ba743d99f0c52bd93813063"
URL = "http://openapi.tuling123.com/openapi/api/v2"
HEADERS = {'Content-Type': 'application/json;charset=UTF-8'}

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def rec(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")
        audio = r.listen(source)

    with open("recording.wav", "wb") as f:
        f.write(audio.get_wav_data())

def listen():
    with open('recording.wav', 'rb') as f:
        audio_data = f.read()

    result = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1537,
    })

    result_text = result["result"][0]
    
    #result_text = result["err_no"]

    print("you said: " + result_text)

    return result_text

def robot(text=""):
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": ""
            },
            "selfInfo": {
                "location": {
                    "city": "杭州",
                    "street": "网商路"
                }
            }
        },
        "userInfo": {
            "apiKey": TURING_KEY,
            "userId": "starky"
        }
    }

    data["perception"]["inputText"]["text"] = text
    response = requests.request("post", URL, json=data, headers=HEADERS)
    response_dict = json.loads(response.text)

    result = response_dict["results"][0]["values"]["text"]
    print("the AI said: " + result)
    return result

def speak(text=""):
    result = client.synthesis(text, 'zh', 1, {
        'spd': 4,
        'vol': 5,
        'per': 4,
    })

    if not isinstance(result, dict):
        with open('audio.mp3', 'wb') as f:
            f.write(result)

def play():
    os.system('sox audio.mp3 audio.wav')
    wf = wave.open('audio.wav', 'rb')
    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    wf.close()

    p.terminate()

if __name__ == "__main__":
    rec()
    your_said = listen()
    the_ai_said = robot(your_said)
    speak(the_ai_said)
    play()