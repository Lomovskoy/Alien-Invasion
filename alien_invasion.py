import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf

def run_game():
    # Инициализирует pygame, settings и объект экрана.
    pygame.init()
    
    #Задаём настрйоки игры
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Создание корабля.
    ship = Ship(ai_settings, screen)
    # Создание группы для хранения пуль.
    bullets = Group()
    # Создание группы для хранения пришельцев.
    aliens = Group()
    # Создание флота пришельцев.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Запуск основного цикла игры.
    while True:
        
        # Отслеживание событий клавиатуры и мыши.
        gf.check_events(ai_settings, screen, ship, bullets)
        
        #Обновление позиции корабля и пули
        ship.update()
        bullets.update()

        # Удаление пуль, вышедших за край экрана.
        gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
        
        #Обновление пришельцев
        gf.update_aliens(ai_settings, aliens)
        
        # Отображение последнего прорисованного экрана.
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)


run_game()
#270
