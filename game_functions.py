import sys, pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sc):
    """Реагирует на нажатие клавиш."""
    if event.key == pygame.K_RIGHT:
        #Остановка корабля 
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        #Остановка корабля 
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # Создание новой пули и включение ее в группу bullets.
        fire_bullet(ai_settings, screen, ship, bullets, sc)
    elif event.key == pygame.K_q:
        #Запись рекорда
        save_record(stats)
        sys.exit()
            
def fire_bullet(ai_settings, screen, ship, bullets, sc):
    """Выпускает пулю, если максимум еще не достигнут."""
    if len(bullets) < ai_settings.bullets_allowed:
        #Звук выстрела
        sc.play_shot()
        #Создание пули
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
            
def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш."""
    # Переместить корабль вправо.
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    # Переместить корабль влево.   
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
        
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets, sc):
    """Обрабатывает нажатия клавиш и события мыши."""
    for event in pygame.event.get():
        #Если нажат крестик
        if event.type == pygame.QUIT:
            #Запись рекорда
            save_record(stats)
            #выйти из программы
            sys.exit()

        #Перемещение корабля
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship,
                                 bullets, stats, sc)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                                    ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                                    aliens, bullets, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Сброс игровых настроек.
        ai_settings.initialize_dynamic_settings()
        
        # Указатель мыши скрывается.
        pygame.mouse.set_visible(False)

        # Сброс игровой статистики.
        stats.reset_stats()
        stats.game_active = True

        # Сброс изображений счетов и уровня.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        # Очистка списков пришельцев и пуль.
        aliens.empty()
        bullets.empty()
        
        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                        play_button, fps, ipbox):
    """Обновляет изображения на экране и отображает новый экран."""
    
    # При каждом проходе цикла перерисовывается экран.
    screen.fill(ai_settings.bg_color)
    
    # Все пули выводятся позади изображений корабля и пришельцев.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    #Рисует корабль
    ship.blitme()
    #Рисуем пришельцев
    aliens.draw(screen)
    # Вывод счета.
    sb.show_score()
    #Вывод кадров в секунду
    sb.drav_fps(fps)
    
    # Кнопка Play отображается в том случае, если игра неактивна.
    if not stats.game_active:
        # прозрачный фон
        draw_fon(screen)
        play_button.draw_button()
    # Отображение последнего прорисованного экрана.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, sc):
    """Обновляет позиции пуль и уничтожает старые пули."""
    # Обновление позиций пуль.
    bullets.update()
    # Удаление пуль, вышедших за край экрана.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                    aliens, bullets, sc)
  
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                    aliens, bullets, sc):
    """Обработка коллизий пуль с пришельцами."""
    # Удаление пуль и пришельцев, участвующих в коллизиях.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            #Звук выстрела
            sc.play_target_shooting()
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)
        
    if len(aliens) == 0:
        # Если весь флот уничтожен, начинается следующий уровень.
        bullets.empty()
        ai_settings.increase_speed()
        
        # Увеличение уровня.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количество рядов, помещающихся на экране."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев."""
    # Создание пришельца и вычисление количества пришельцев в ряду.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    # Создание флота пришельцев.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, sc):
    """Обрабатывает столкновение корабля с пришельцем."""
    if stats.ships_left > 0:
        #Звук удара
        sc.play_hit_player()
        
        # Уменьшение ships_left.
        stats.ships_left -= 1

        # Обновление игровой информации.
        sb.prep_ships()

        # Очистка списков пришельцев и пуль.
        aliens.empty()
        bullets.empty()
        
        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
        # Пауза.
        sleep(0.5)

    else:
        #Запись рекорда
        save_record(stats)
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, sc):
    """Проверяет, добрались ли пришельцы до нижнего края экрана."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит то же, что при столкновении с кораблем.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, sc)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, sc):
    """Проверяет, достиг ли флот края экрана,
    после чего обновляет позиции всех пришельцев во флоте."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # Проверка коллизий "пришелец-корабль".
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, sc)

    # Проверка пришельцев, добравшихся до нижнего края экрана.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, sc)

def check_high_score(stats, sb):
    """Проверяет, появился ли новый рекорд."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def save_record(stats):
    #print("Запись рекорда")
    filename = 'record/record.txt'
    #Читаем из файла
    with open(filename) as file_object:
        contents = file_object.read()
        #Усли считанный чекорд больше 
        if int(contents) < stats.score:
            with open(filename, 'w') as file_object:
                file_object.write(str(stats.score))

def load_record(stats):
    filename = 'record/record.txt'
    #Читаем из файла
    with open(filename) as file_object:
        stats.high_score = int(file_object.read())
        #print(stats.score)

def draw_fon(screen):
    # Загрузка изображения корабля и получение прямоугольника.
    image = pygame.image.load('images/background.png')
    rect = image.get_rect()
    screen_rect = screen.get_rect()
        
    screen.blit(image, rect)
