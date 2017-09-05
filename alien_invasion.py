import pygame
from ship import Ship
from button import Button
import game_functions as gf
import inputbox as ipbox
from settings import Settings
from pygame.sprite import Group
from game_stats import GameStats
from scoreboard import Scoreboard
from sound_controll import SoundControll as SC

def run_game():
    # Инициализирует pygame, settings и объект экрана.
    pygame.init()
    
    #Задаём настрйоки игры
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #Загрузка музыки и звуков
    sc = SC()
    # Создание кнопки Play.
    play_button = Button(ai_settings, screen, "Play")
    #Воспроизведение музыки
    sc.play_music()
    # Создание экземпляра для хранения игровой статистики.
    stats = GameStats(ai_settings)
    # Чтение прежнего рекорда
    gf.load_record(stats)
    # Создание экземпляров GameStats и Scoreboard.
    sb = Scoreboard(ai_settings, screen, stats)
    # Создание корабля.
    ship = Ship(ai_settings, screen)
    # Создание группы для хранения пуль.
    bullets = Group()
    # Создание группы для хранения пришельцев.
    aliens = Group()
    # Создание флота пришельцев.
    gf.create_fleet(ai_settings, screen, ship, aliens)
    #Установка частоты кадров
    clock = pygame.time.Clock()
    FPS = ai_settings.FPS
    
    # Запуск основного цикла игры.
    while True:
        #Ограничение кадров в секкнду
        clock.tick(FPS)
        fps = clock.get_fps()
        
        # Отслеживание событий клавиатуры и мыши.
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets, sc)

        if stats.game_active:
            #Обновление позиции корабля и пули
            ship.update()
            bullets.update()

            # Удаление пуль, вышедших за край экрана.
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                                bullets, sc)
            
            #Обновление пришельцев
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                                bullets, sc)        
        # Отображение последнего прорисованного экрана.
        gf.update_screen(ai_settings, screen, stats, sb, ship,
                            aliens, bullets, play_button, fps, ipbox)

run_game()
