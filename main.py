import pygame
from data.useful_functions import load, draw_text
import data.gfx.button
import Enemy
import powerup
import Hero
import random
import block


# Originally, map was made to play on 16x9 scale
# but not every solution can be used to play
# Tested solutions are those, where width / height is ~1.78
# Examples are: 1920x1080, 640x360

# Another comment is about pause menu
# I don't have strict design, and because of that, my pause menu is such a mess. If you want to change it, go to line 144

current_map = 0
maps = [  # map is 16x9
    [  # this is gaming map
        '......-.........',
        '......-......#..',
        '..@.............',
        '......-+........',
        '......--...-----',
        '...........-....',
        '.----......-....',
        '.----...........',
        '+...............',
    ],
    [  # this is a debug map
        '-..............-',
        '.@..............',
        '................',
        '................',
        '................',
        '................',
        '................',
        '..............#.',
        '-..............-',
        '................',
        '-..............-',
    ]
]

# Tiles = pygame.sprite.Group()
# Heroes = pygame.sprite.Group()
# Enemies = pygame.sprite.Group()
# Powerups = pygame.sprite.Group()
def generate_map(temp):
    map = maps[temp]
    for row, line in enumerate(map):
        print(row, line)
        for column, pos in enumerate(line):
            if pos == '@':  # Hero
                Heroes.add(Hero.Hero(column, row))
            elif pos == '#':  # Enemy
                Enemies.add(Enemy.Enemy(column, row))
            elif pos == '-':  # Tile
                Tiles.add(block.Block(column, row))
            elif pos == '+':  # Powerup
                Powerups.add(powerup.PowerUp(column, row))

def draw_pause():
    global paused, run
    if button_resume.draw(WIN):
        paused = False
    button_options.draw(WIN)
    if button_quit.draw(WIN):
        run = False


def main():
    global fps, paused, run
    run = True
    # initializing map

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        WIN.fill(COLORS['background_color'])  # фон
        if Heroes.sprites()[0].can_play:
            Enemies.sprites()[0].light.update(WIN, Enemies.sprites()[0], Tiles)  # Light 6
            draw_text(
                WIN, 'press SPACE to pause',
                COLORS['text_color'],
                CONSTANTS['WIDTH'] * 0.234,
                CONSTANTS['HEIGHT'] * 0.39, 
                hint_font)  # Hint 5
            draw_text(
                WIN, 
                str(round(1000 / fps)), 
                COLORS['text_color'], 
                CONSTANTS['WIDTH'] * 0.9375,
                0, 
                fps_font)  # FPS 5
            Tiles.update()  # Blocks 4
            Enemies.update(
                WIN, 
                Tiles, 
                pygame.event.get(), 
                paused)  # Enemy 3
            Heroes.update(WIN, Tiles, Enemies, pygame.event.get(), paused)  # Hero 2
        if not Heroes.sprites()[0].can_play:
            game_over()  # Game Over 2
        draw_pause() if paused else None  # Pause 1
        pygame.display.flip()
        fps = clock.tick(CONSTANTS['FPS'])
    pygame.quit()


def game_over():
    draw_text(WIN, 'GAME OVER', COLORS['game_over'], CONSTANTS['WIDTH'] * 0.23, CONSTANTS['HEIGHT'] * 0.39, over_font)


if __name__ == '__main__':
    COLORS, CONSTANTS = load()  # Словари с константами
    WIN = pygame.display.set_mode((CONSTANTS['WIDTH'], CONSTANTS['HEIGHT']))  # Основное окно
    pygame.display.set_caption('Avoid the Light')  # Название
    fps = CONSTANTS['FPS']  # задание фпс для первого кадра

    # Задание меню паузы
    hint_font = pygame.font.SysFont("arialblack", int(CONSTANTS['HEIGHT'] / 12.8))  # шрифт подсказок
    fps_font = pygame.font.SysFont("arialblack", int(CONSTANTS['HEIGHT'] / 27))  # шрифт фпс
    over_font = pygame.font.SysFont("arialblack", int(CONSTANTS['HEIGHT'] / 7.68))  # шрифт доп. вещей

    clock = pygame.time.Clock()

    Tiles = pygame.sprite.Group()
    Heroes = pygame.sprite.Group()
    Enemies = pygame.sprite.Group()
    Powerups = pygame.sprite.Group()
    generate_map(current_map)

    resume_img = pygame.image.load('data/gfx/button_resume.png')
    options_img = pygame.image.load('data/gfx/button_options.png')
    quit_img = pygame.image.load('data/gfx/button_quit.png')

    button_resume = data.gfx.button.Button(
        CONSTANTS['WIDTH'] * 0.21, 
        CONSTANTS['HEIGHT'] * 0.12, 
        resume_img, 
        CONSTANTS['WIDTH'] * 0.56, 
        CONSTANTS['HEIGHT'] * 0.18)
    
    button_options = data.gfx.button.Button(
        CONSTANTS['WIDTH'] * 0.21, 
        CONSTANTS['HEIGHT'] * 0.41, 
        options_img, 
        CONSTANTS['WIDTH'] * 0.56, 
        CONSTANTS['HEIGHT'] * 0.18)
    
    button_quit = data.gfx.button.Button(
        CONSTANTS['WIDTH'] * 0.21, 
        CONSTANTS['HEIGHT'] * 0.71, 
        quit_img, 
        CONSTANTS['WIDTH'] * 0.56, 
        CONSTANTS['HEIGHT'] * 0.18)
    
    paused = False
    run = True
    main()
