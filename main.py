import subprocess
import re
import utils

if __name__ == "__main__":
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
