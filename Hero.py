import pygame
from data.useful_functions import load
import Enemy
import math

pygame.init()
pygame.mixer.init()

COLORS, CONSTANTS = load()

if __name__ == '__main__':
    screen = pygame.display.set_mode((CONSTANTS['WIDTH'], CONSTANTS['HEIGHT']))


class Hero(pygame.sprite.Sprite):
    MAX_HP = 10

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('data/gfx/main_character.png'), (CONSTANTS['SCALE'], CONSTANTS['SCALE']))
        self.rect = self.image.get_rect(x=x * CONSTANTS['SCALE'], y=y * CONSTANTS['SCALE'])
        self.can_play = True
        self.isCollided = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        self.move_speed = {
            'x': round(CONSTANTS['WIDTH'] * 0.3 / CONSTANTS['FPS']),
            'y': round(CONSTANTS['HEIGHT'] * 0.5 / CONSTANTS['FPS'])
        }
        self.current_speed = {
            'x': 0,
            'y': 0
        }
        self.hp = Hero.MAX_HP
        self.immortalTime = {
            'max': CONSTANTS['IMMORTAL'] * CONSTANTS['FPS'],
            'current': 0
        }
        self.kill_animation = {
            '1': pygame.transform.scale(pygame.image.load('data/gfx/death1.png'), (CONSTANTS['SCALE'], CONSTANTS['SCALE'])),
            '2': pygame.transform.scale(pygame.image.load('data/gfx/death2.png'), (CONSTANTS['SCALE'], CONSTANTS['SCALE'])),
            '3': pygame.transform.scale(pygame.image.load('data/gfx/death3.png'), (CONSTANTS['SCALE'], CONSTANTS['SCALE'])),
        }

    def update(self, fps, surface: pygame.surface.Surface, level: pygame.sprite.Group, enemy, powerups: pygame.sprite.Group, events: pygame.event.get(), keys: pygame.key.get_pressed(), paused):
        self.move_speed = {
            'x': round(CONSTANTS['WIDTH'] * 0.3 / fps),
            'y': round(CONSTANTS['HEIGHT'] * 0.3 / fps)
        }
        if not paused and self.can_play:
            self.check_controls(keys, events)
            self.rect.y += self.current_speed['y']
            self.checkCollide_y(level)
            self.rect.x += self.current_speed['x']
            self.checkCollide_x(level)
            self.check_damage(enemy, level)
            self.check_powerup(powerups)
        self.draw(surface)
        return round(self.current_speed['x'], 1), round(self.current_speed['y'], 1)

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.image, self.rect)

    def check_controls(self, keys, events=None):
        # events можно использовать так как pygame не любит когда много раз вызывают event.get()
        if keys[pygame.K_a]:
            self.current_speed['x'] = self.move_speed['x'] * -1  # left
        if keys[pygame.K_d]:
            self.current_speed['x'] = self.move_speed['x']  # right
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.current_speed['x'] = 0
        if keys[pygame.K_w]:
            self.current_speed['y'] = self.move_speed['y'] * -1  # up
        if keys[pygame.K_s]:
            self.current_speed['y'] = self.move_speed['y']  # down
        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.current_speed['y'] = 0

    def checkCollide_x(self, level: pygame.sprite.Group):
        for tile in level:
            if pygame.sprite.collide_rect(self, tile):
                if self.current_speed['x'] > 0:  # right
                    self.rect.right = tile.rect.left
                elif self.current_speed['x'] < 0:  # left
                    self.rect.left = tile.rect.right
        if self.rect.topleft[0] <= 0 and self.current_speed['x'] < 0:  # left
            self.current_speed['x'] = 0
            self.rect.left = 0
        elif self.rect.bottomright[0] >= CONSTANTS['WIDTH'] and self.current_speed['x'] > 0:  # right
            self.current_speed['x'] = 0
            self.rect.right = CONSTANTS['WIDTH']

    def checkCollide_y(self, level: pygame.sprite.Group):
        for tile in level:
            if pygame.sprite.collide_rect(self, tile):
                if self.current_speed['y'] > 0:  # down
                    self.rect.bottom = tile.rect.top
                elif self.current_speed['y'] < 0:  # up
                    self.rect.top = tile.rect.bottom
        if self.rect.topleft[1] <= 0 and self.current_speed['y'] < 0:  # up
            self.current_speed['y'] = 0
            self.rect.top = 0
        elif self.rect.bottomright[1] >= CONSTANTS['HEIGHT'] and self.current_speed['y'] > 0:  # down
            self.current_speed['y'] = 0
            self.rect.bottom = CONSTANTS['HEIGHT']

    def check_damage(self, enemy_group: pygame.sprite.Group, level: pygame.sprite.Group):
        # TODO: not optimal check for kill, better hadn't done it. It works optimal only with one enemy, so I will use it only with one enemy
        for enemy in enemy_group.sprites():
            if pygame.sprite.collide_rect(self, enemy.light):
                if not self.immortalTime['current']:
                    self.get_damage(1)
                    self.immortalTime['current'] = 1
        if self.immortalTime['current'] > 0:
            self.immortalTime['current'] += 1
            if self.immortalTime['current'] >= self.immortalTime['max']:
                self.immortalTime['current'] = 0
    
    def check_powerup(self, powerups: pygame.sprite.Group):
        if self.hp != 10:
            dict = pygame.sprite.groupcollide(pygame.sprite.GroupSingle(self), powerups, False, True)
            if dict != {}:
                self.hp = 10

    def get_damage(self, damage):
        self.hp -= damage
        print(self.hp)
        if self.hp <= 0:
            self.death()

    def death(self):
        global can_play
        self.can_play = False
    
    def kill(self, screen: pygame.surface.Surface, i: int):
        self.image = self.kill_animation[str(i)]
        screen.blit(self.image, self.rect)
