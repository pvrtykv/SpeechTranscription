import binascii
import hashlib
import os
import re
import subprocess
from cryptography.fernet import Fernet
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


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    return open("key.key", "rb").read()


def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(filename, "wb") as file:
        file.write(decrypted_data)


KEY = load_key()


def transcribe(file):
    if file:
        file_list = open("julius/test.dbl", 'w')
        file_list.write(file)
        file_list.close()

        if not os.path.exists('julius_output'):
            os.mkdir('julius_output')

        output = increment_filename("julius_output/output.txt")

        subprocess.run(["julius-dnn", "-C", "julius.jconf", "-dnnconf", "dnn.jconf", ">", "../" + output],
                       shell=True, cwd="julius",
                       check=True)

        r = re.compile(r"sentence1: <s> (.+?) </s>")

        f1 = open(output, 'r')
        lines = f1.readlines()
        f1.close()

        if not os.path.exists('transcriptions'):
            os.mkdir('transcriptions')

        transcription = increment_filename("transcriptions/transcription.txt")
        f2 = open(transcription, 'a')

        for line in lines:
            c = r.match(line)
            if c is not None:
                f2.write("\n")
                f2.write(c.group(1))

        f2.close()

        with open(transcription, 'r') as f:
            text = f.read()

        encrypt(output, KEY)
        encrypt(transcription, KEY)
        return text
