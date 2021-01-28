import sys
import os

import sounddevice as sd
import soundfile as sf
from playsound import playsound
import numpy
import tkinter as tk


# Command line arguments
INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "words.txt"
OUTPUT_DIRECTORY = sys.argv[2].rstrip("/") if len(sys.argv) > 2 else "recordings"


# Get already recorded words
_, _, files = next(os.walk(OUTPUT_DIRECTORY))
print(files)


# Get words to record
with open(INPUT_FILE) as f:
    words = list(map(lambda x: x.strip(), f.readlines()))


# Audio numbers
SAMPLERATE = 44100
CHANNELS = 1
BLOCKSIZE = 512


# Keeping track of current word
word_index = 0
while words[word_index]+".wav" in files:
    word_index += 1
word_text = words[word_index]
filepath = f"{OUTPUT_DIRECTORY}/{word_text}.wav"


# Global variables for recording
recording = False
stream = None
soundfile = None


# Functions for recording and playing audio
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    soundfile.write(indata.copy())

def record():
    global recording, stream, soundfile, record_button
    if not recording:
        recording = True
        record_button.config(text="stop")
        stream = sd.InputStream(samplerate=SAMPLERATE, blocksize=BLOCKSIZE, channels=CHANNELS, callback=callback)
        soundfile = sf.SoundFile(filepath, "w", SAMPLERATE, CHANNELS)
        stream.start()
    else:
        recording = False
        record_button.config(text="record")
        stream.stop()
        stream.close()
        soundfile.close()

def play():
    playsound(filepath)


# Function for getting next word
def next_word():
    global word_index, word_text, filepath
    word_index += 1
    if word_index == len(words):
        word_label.config(text="DONE")
        record_button.pack_forget()
        play_button.pack_forget()
    elif word_index > len(words):
        root.destroy()
    else:
        while words[word_index]+".wav" in files:
            word_index += 1
        word_text = words[word_index]
        filepath = f"{OUTPUT_DIRECTORY}/{word_text}.wav"
        word_label.config(text=word_text)


# Key event handler
def key_event(event):
    key = event.char
    if key == "j":   # Press J to record and stop
        record_button.invoke()
    elif key == "k": # Press K to play recording
        play_button.invoke()
    elif key == "l": # Press L to go to next word
        next_button.invoke()

# Configure window
root = tk.Tk()
word_label = tk.Label(root, text=word_text, font=("",24))

record_button = tk.Button(text="record", command=record)
play_button = tk.Button(text="play", command=play)
next_button = tk.Button(text="next", command=next_word)

root.bind("<Key>", key_event)

word_label.pack()
record_button.pack(side=tk.LEFT)
play_button.pack(side=tk.LEFT)
next_button.pack(side=tk.LEFT)

root.mainloop()
