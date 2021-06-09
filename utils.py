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
    enc_path = os.path.dirname(path) + "/ENC" + os.path.basename(path)
    enc_filename, extension = os.path.splitext(enc_path)
    counter = 1

    while os.path.exists(path) or os.path.exists(enc_path):
        path = filename + "_" + str(counter) + extension
        enc_path = enc_filename + "_" + str(counter) + extension
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
    if os.path.exists('key.key'):
        return open("key.key", "rb").read()
    return


def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
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
    recording_filename = os.path.basename(file)
    recording_filename = os.path.splitext(recording_filename)[0]
    print(recording_filename)
    prefix = recording_filename[0:3]
    if file:
        if prefix == "ENC":
            file = change_prefix_and_decrypt(file, KEY)

        file_list = open("julius/test.dbl", 'w')
        file_list.write(file)
        file_list.close()

        if not os.path.exists('julius_output'):
            os.mkdir('julius_output')

        output = increment_filename("julius_output/output-" + recording_filename + ".txt")

        subprocess.run(["julius-dnn", "-C", "julius.jconf", "-dnnconf", "dnn.jconf", ">", "../" + output],
                       shell=True, cwd="julius",
                       check=True)

        if prefix == "ENC":
            file = change_prefix_and_encrypt(file, KEY)

        r = re.compile(r"sentence1: <s> (.+?) </s>")

        f1 = open(output, 'r')
        lines = f1.readlines()
        f1.close()

        if not os.path.exists('transcriptions'):
            os.mkdir('transcriptions')

        transcription = increment_filename("transcriptions/transcription-" + recording_filename + ".txt")
        f2 = open(transcription, 'a')

        for line in lines:
            c = r.match(line)
            if c is not None:
                f2.write("\n")
                f2.write(c.group(1))

        f2.close()

        with open(transcription, 'r', encoding="iso-8859-2") as f:
            text = f.read()

        transcription_filename = os.path.basename(transcription)
        change_prefix_and_encrypt(output, KEY)
        change_prefix_and_encrypt(transcription, KEY)

        return text, transcription_filename


def change_prefix_and_decrypt(file, key):
    decrypt(file, key)
    dec_filename = os.path.basename(file)
    dec_filename = dec_filename.replace("ENC", "")
    dec_filename = os.path.dirname(file) + "/" + dec_filename
    os.rename(file, dec_filename)
    file = dec_filename
    return file


def change_prefix_and_encrypt(file, key):
    encrypt(file, key)
    enc_filename = "ENC" + os.path.basename(file)
    enc_filename = os.path.dirname(file) + "/" + enc_filename
    os.rename(file, enc_filename)
    file = enc_filename
    return file
