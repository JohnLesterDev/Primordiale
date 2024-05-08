import os
import pygame

PATH = os.getcwd()
# Initialize pygame audio
pygame.mixer.init()

# Background Music
def play_background_music(loop_count=-1):
    pygame.mixer.music.load(os.path.join(PATH, "resources", "bgm", "bgm.mp3"))
    pygame.mixer.music.play(loop_count)

def stop_background_music():
    pygame.mixer.music.stop()

def pause_background_music():
    pygame.mixer.music.pause()

def unpause_background_music():
    pygame.mixer.music.unpause()

# Sound Effects
def load_sound(file_path):
    return pygame.mixer.Sound(os.path.join(PATH, "resources", "sfx", file_path))

def play_sound(sound):
    sound.play()

def stop_sound(sound):
    sound.stop()

def set_sound_volume(sound, volume):
    sound.set_volume(volume)
