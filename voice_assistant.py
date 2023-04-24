from vosk import Model, KaldiRecognizer
import os
import pyaudio
import pyttsx3
import va_config
from va_config import config

assistant_name = "софия"
rate = 44100

model = Model("vosk-model-small-ru-0.22")
rec = KaldiRecognizer(model, rate)
pAud = pyaudio.PyAudio()
engine = pyttsx3.init()
stream = pAud.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=rate,
    input=True,
    frames_per_buffer=rate
)
stream.start_stream()


def read_data_stream():
    global rec
    global stream
    data = stream.read(4000, exception_on_overflow=False)
    if len(data) == 0:
        return -1
    command = (rec.Result() if rec.AcceptWaveform(data) else rec.PartialResult()).split('''"''')[3]

    return command


def understand_and_respond(data):
    global engine
    data = data.replace("софия ", "")
    if data == "":
        return 0
    for key in config.keys():
        if data in key:
            response = config[key]
            print(response)
            if response == "quit_listening":
                engine.say("okay")
                engine.runAndWait()
                return "ql"
            if response == "start_getting_task":
                engine.say("what is the task you want to create")
                engine.runAndWait()
                return "sgt"


def Get_task_data(step, data):
    global engine