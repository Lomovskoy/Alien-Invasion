import pygame

class SoundControll():

    def __init__(self):
        # Загрузка музыки.
        self.musics = pygame.mixer.music.load('sound/music_comp.ogg')
        #Загрузка звуков
        self.shot = pygame.mixer.Sound('sound/Zvuk_lazera.ogg')
        self.hit = pygame.mixer.Sound('sound/hit_player.ogg')
        self.target = pygame.mixer.Sound('sound/target_shooting.ogg')

    def play_music(self):
        # Начинаем проигрывать музыку,
        # loops = -1 заставляет проигрывать звук циклично,
        # непереставая.
        self.music_channel = pygame.mixer.music.play(loops = -1)
        # Устанавливаем громкость.
        pygame.mixer.music.set_volume(0.8)
        
    def play_shot(self):
        # Начинаем проигрывать звук.
        self.shot_channel = self.shot.play(loops = 0)
        # Устанавливаем громкость.
        self.shot_channel.set_volume(0.3)
        
    def play_hit_player(self):
        # Начинаем проигрывать звук.
        self.hit_channel = self.hit.play(loops = 0)
        # Устанавливаем громкость.
        self.hit.set_volume(0.3)
        
    def play_target_shooting(self):
        # Начинаем проигрывать звук.
        self.target_channel = self.target.play(loops = 0)
        # Устанавливаем громкость.
        self.target.set_volume(0.2)
