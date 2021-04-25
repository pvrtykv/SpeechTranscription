import os
import pyaudio
import wave


class RecordControl:
    def __init__(self):
        self.finished = False


def increment_filename(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + str(counter) + extension
        counter += 1

    return path


def record_audio(filename: str, record_control: RecordControl):
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 16000
    
    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    while not record_control.finished:
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
