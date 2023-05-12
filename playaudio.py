from winsound import PlaySound, SND_ASYNC, SND_FILENAME
from playsound import playsound

def playaudio(file : str):
    # PlaySound(file, SND_ASYNC | SND_FILENAME)
    playsound(file, block=False)

