from pygame import mixer

class SoundPlayer:
    def __init__(self):
        mixer.init()
        self.sounds = {
            "snare": mixer.Sound("sounds/snare.wav"),
            "kick": mixer.Sound("sounds/kick.wav"),
            "hi-hat": mixer.Sound("sounds/hihat.wav"),
        }

    def play_sound(self, drum_name):
        if drum_name in self.sounds:
            self.sounds[drum_name].play()