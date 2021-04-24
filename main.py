import subprocess
import re
import utils
import os
import threading

if __name__ == "__main__":
    os.chdir("julius")
    recording = utils.increment_filename("media/recording.wav")
    record_control = utils.RecordControl()
    thread = threading.Thread(target=utils.record_audio, args=(recording, record_control))

    print("Started recording")
    thread.start()
    input("Enter any character to stop ")
    record_control.finished = True
    thread.join()
    print("Finished recording")

    file_list = open("test.dbl", 'w')
    file_list.write(recording)
    file_list.close()

    os.chdir("..")

    julius_output = utils.increment_filename("julius_output.txt")

    subprocess.run(["julius-dnn", "-C", "julius.jconf", "-dnnconf", "dnn.jconf", ">", "../" + julius_output],
                   shell=True, cwd="julius",
                   check=True)

    r = re.compile(r"sentence1: <s> (.+?) </s>")

    f1 = open(julius_output, 'r')
    lines = f1.readlines()
    f1.close()

    transcription = utils.increment_filename("transcription.txt")
    f2 = open(transcription, 'a')

    for line in lines:
        c = r.match(line)
        if c is not None:
            f2.write("\n")
            f2.write(c.group(1))

    f2.close()
