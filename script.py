import argparse
import tempfile
import queue
import sys
from os import system

import sounddevice as sd
import soundfile as sf
import numpy
assert numpy

import subprocess

samplerate = 16000
channels = 1
device = 0
subtype = 'PCM_24'

q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

def record(filename):
    try:
        # Make sure the file is opened before recording anything
        with sf.SoundFile(filename, mode='x', samplerate=samplerate,
                        channels=channels, subtype=subtype) as file:
            with sd.InputStream(samplerate=samplerate, device=device,
                                channels=channels, callback=callback):
                print('#' * 80)
                print('press Ctrl+C to stop the recording')
                print('#' * 80)
                while True:
                    file.write(q.get())
    except KeyboardInterrupt:
        print('\nRecording finished: ' + repr(filename))
    except Exception as e:
        print('\nError: ' + str(e))

def demo(filename):
    file = "wav/c"+str(filename)+".wav"
    print("\nPlaying demo for \""+file+"\"")
    subprocess.call(["afplay", file])

def main():
    f = open("PRUS.txt", "r")
    sentences = f.readlines()

    start = int(input("Enter Starting Point (Int): "))
    for i in range(start, 708):
        filename = "21100229/"+str(i)+".wav"
        while True:
            system("clear")
            print(sentences[i])
            print("\n1) Record\n2) Demo")
            op = input("Enter operation number: ")
            if op == "1":
                record(filename)
            elif op == "2":
                demo(i+1)
                system("pause")
                continue
            else:
                continue
            user = input("Satisfied (y/n)")
            if user == 'y':
                break
            else:
                continue

main()