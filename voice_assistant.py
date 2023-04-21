from vosk import Model, KaldiRecognizer
import os
import pyaudio

assistant_name = "софия"
rate = 44100


model = Model("vosk-model-small-ru-0.22")
rec = KaldiRecognizer(model, rate)
pAud = pyaudio.PyAudio()
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
    data = stream.read(4000, exception_on_overflow = False)
    if len(data) == 0:
        return -1
    command = (rec.Result() if rec.AcceptWaveform(data) else rec.PartialResult()).split('''"''')[3]

    return command
