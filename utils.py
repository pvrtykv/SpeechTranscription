import binascii
import hashlib
import os
import re
import subprocess
import tkinter.messagebox as messagebox
from cryptography.fernet import Fernet
from Login import Login


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


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


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


def transcribe(file):
    recording_filename = os.path.basename(file)
    recording_filename = os.path.splitext(recording_filename)[0]
    prefix = recording_filename[0:3]
    if file:
        if prefix == "ENC":
            file = change_prefix_and_decrypt(file, Login.KEY)
            recording_filename = os.path.splitext(os.path.basename(file))[0]

        file_list = open("julius/test.dbl", 'w')
        file_list.write(file)
        file_list.close()

        output_dirname = 'julius_output/' + Login.USERNAME
        if not os.path.exists(output_dirname):
            os.makedirs(output_dirname)

        output = increment_filename(output_dirname + "/output-" + recording_filename + ".txt")

        subprocess.run(["julius-dnn", "-C", "julius.jconf", "-dnnconf", "dnn.jconf", ">", "../" + output],
                       shell=True, cwd="julius",
                       check=True)

        if prefix == "ENC":
            file = change_prefix_and_encrypt(file, Login.KEY)

        r = re.compile(r"sentence1: <s> (.+?) </s>")

        f1 = open(output, 'r')
        lines = f1.readlines()
        f1.close()

        transcriptions_dirname = "transcriptions/" + Login.USERNAME
        if not os.path.exists(transcriptions_dirname):
            os.makedirs(transcriptions_dirname)

        transcription = increment_filename(transcriptions_dirname + "/transcription-" + recording_filename + ".txt")
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
        change_prefix_and_encrypt(output, Login.KEY)
        change_prefix_and_encrypt(transcription, Login.KEY)

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


def not_authorized_message():
    messagebox.showwarning(None, "You are not authorized to access this file!")
