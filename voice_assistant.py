from vosk import Model, KaldiRecognizer
import os
import pyaudio
import pyttsx3
import va_config
from va_config import config
from va_config import time_config
from va_config import date_config

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


def understand_time(data):
    global engine
    data_sep = data.split(" ")
    hour_from = ""
    minute_from = ""
    hour_to = ""
    minute_to = ""
    try:
        if not data_sep[0] == "с":
            data_sep.insert(0, "с")

        for key in time_config.keys():
            if data_sep[1] in key:
                hour_from = time_config[key]
            if data_sep[2] in key:
                minute_from = time_config[key]
            if not data_sep[3] == "до":
                if data_sep[3] in key:
                    if len(minute_from) == 2:
                        minute_from[-1] = time_config[key]
                    else:
                        minute_from += time_config[key]
            else:
                if len(minute_from) < 2:
                    minute_from = "0" + minute_from

            if data_sep[data_sep.index("до") + 1] in key:
                hour_to = time_config[key]
            if data_sep[data_sep.index("до") + 2] in key:
                minute_to = time_config[key]
            if len(data_sep) == data_sep.index("до") + 4:
                if data_sep[data_sep.index("до") + 3] in key:
                    if len(minute_to) == 2:
                        minute_to[-1] = time_config[key]
                    else:
                        minute_to += time_config[key]
            else:
                if len(minute_from) < 2:
                    minute_to = "0" + minute_to

    except IndexError:
        pass
    if hour_from == "" or minute_from == "" or hour_to == "" or minute_to == "":
        return ""
    engine.say("what is the date of the task")
    engine.runAndWait()
    return f"{hour_from}:{minute_from}-{hour_to}:{minute_to}"


def understand_date(data):
    data = data.replace(" ноль", "")
    data_sep = data.split(" ")
    offset = ""
    day = ""
    month = ""
    year = ""
    try:
        for key in date_config.keys():
            if data_sep[0] in key:
                day = date_config[key]
        if len(data_sep) == 3:
            for key in date_config.keys():
                if data_sep[1] in key:
                    day[-1] = date_config[key]
                if data_sep[2] in key:
                    month = date_config[key]
        else:
            for key in date_config.keys():
                if data_sep[1] in key:
                    month = date_config[key]

    except IndexError:
        pass
    if day == "" or month == "":
        return ""
    engine.say("what is the type of the task")
    engine.runAndWait()
    return f"{month}-{day}"


def va_say(fraze):
    global engine
    engine.say(fraze)
    engine.runAndWait()
