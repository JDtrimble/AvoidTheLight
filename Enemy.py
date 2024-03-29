import pygame
import random
from data.useful_functions import load
import math

pygame.init()
pygame.mixer.init()

COLORS, CONSTANTS = load()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.isCollided = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        self.animations = {
            'standing': pygame.transform.scale(pygame.image.load('data/gfx/enemy.png'), (CONSTANTS['SCALE'], CONSTANTS['SCALE']))
        }
        self.image = self.animations['standing']
        self.rect = self.image.get_rect(x=x * CONSTANTS['SCALE'], y=y * CONSTANTS['SCALE'])
        self.x = x
        self.y = y
        self.brightness = CONSTANTS['SCALE'] * 3    
        self.move_speed = {  # сделать зависимость от кадров
            'x': round(CONSTANTS['WIDTH'] * 0.15 / CONSTANTS['FPS']),
            'y': round(CONSTANTS['HEIGHT'] * 0.25 / CONSTANTS['FPS'])
        }
        self.current_speed = {
            'x': 0,
            'y': 0
        }
        self.path = {
            'active': 0,
            'direction': 0  # stay calm
        }
        self.light = Light(self.rect.center[0], self.rect.center[1], self)

    def update(self, fps, surface: pygame.surface.Surface, level: pygame.sprite.Group, events: pygame.event.get(), keys: pygame.key.get_pressed(), paused):
        self.move_speed = {  # сделать зависимость от кадров
            'x': round(CONSTANTS['WIDTH'] * 0.15 / fps),
            'y': round(CONSTANTS['HEIGHT'] * 0.25 / fps)
        }
        if not paused:
            self.calculate_movement(keys)
            self.rect.y += self.current_speed['y']
            self.checkCollide_y(level)
            self.rect.x += self.current_speed['x']
            self.checkCollide_x(level)
        self.draw(surface)

    def checkCollide_x(self, level: pygame.sprite.Group):
        for tile in level:
            if pygame.sprite.collide_rect(self, tile):
                if self.current_speed['x'] > 0:  # right
                    self.rect.right = tile.rect.left
                elif self.current_speed['x'] < 0:  # left
                    self.rect.left = tile.rect.right
        if self.rect.topleft[0] <= 0 and self.current_speed['x'] < 0:
            self.current_speed['x'] = 0
            self.rect.left = 0
        elif self.rect.bottomright[0] >= CONSTANTS['WIDTH'] and self.current_speed['x'] > 0:
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

    def calculate_movement(self, keys):
        # if self.path['active'] == 64:  # нету пути
        #     self.path['active'] = 0
        #     self.path['direction'] = random.randint(0, 9)  # direction where to move UNUSED
        #     self.path['active'] = True
        #     if self.path['direction'] == 0:  # 0 - none
        #         self.current_speed['x'], self.current_speed['y'] = 0, 0
        #     if self.path['direction'] == 1:  # 1 - up left
        #         self.current_speed['x'], self.current_speed['y'] = 1, -1
        #     if self.path['direction'] == 2:  # 2 - up
        #         self.current_speed['x'], self.current_speed['y'] = 0, -1
        #     if self.path['direction'] == 3:  # 3 - up right
        #         self.current_speed['x'], self.current_speed['y'] = 1, -1
        #     if self.path['direction'] == 4:  # 4 - right
        #         self.current_speed['x'], self.current_speed['y'] = 1, 0
        #     if self.path['direction'] == 5:  # 5 - down right
        #         self.current_speed['x'], self.current_speed['y'] = 1, 1
        #     if self.path['direction'] == 6:  # 6 - down
        #         self.current_speed['x'], self.current_speed['y'] = 0, 1
        #     if self.path['direction'] == 7:  # 7 - down left
        #         self.current_speed['x'], self.current_speed['y'] = -1, 1
        #     if self.path['direction'] == 8:  # 8 - left
        #         self.current_speed['x'], self.current_speed['y'] = -1, 0
        # elif self.path['active'] < 64:  # есть путь, проверка выполнился ли путь
        #     self.path['active'] += 1

        if keys[pygame.K_LEFT]:
            self.current_speed['x'] = self.move_speed['x'] * -1  # left
        if keys[pygame.K_RIGHT]:
            self.current_speed['x'] = self.move_speed['x']  # right
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.current_speed['x'] = 0
        if keys[pygame.K_UP]:
            self.current_speed['y'] = self.move_speed['y'] * -1  # up
        if keys[pygame.K_DOWN]:
            self.current_speed['y'] = self.move_speed['y']  # down
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.current_speed['y'] = 0

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.image, self.rect)


class Light(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy: Enemy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((enemy.brightness*2, enemy.brightness*2))
        self.image.fill(COLORS['background_color'])
        for i in range(1, len(COLORS['saturation_colors']) + 1):
            pygame.draw.circle(self.image, COLORS['saturation_colors'][-i], (enemy.brightness, enemy.brightness), enemy.brightness - i * CONSTANTS['HEIGHT'] / 54)
        self.rect = self.image.get_rect(x=x, y=y)
        # self.mask_image = self.image
        # self.mask_image.set_colorkey(COLORS['background_color'])
        # self.mask = pygame.mask.from_surface(self.mask_image)

    def update(self, surface: pygame.surface.Surface, enemy: Enemy, level: pygame.sprite.Group):
        self.draw(surface, enemy)
        self.redraw(surface, level, enemy)
        # surface.blit(self.mask_image, (400, 200))
        # surface.blit(self.image, (0, 200))

    def draw(self, surface, enemy: Enemy):
        '''
        draws basic light
        '''
        self.rect.center = enemy.rect.center
        surface.blit(self.image, self.rect)

    def redraw(self, surface: pygame.surface.Surface, level: pygame.sprite.Group, enemy: Enemy):
        '''
        draws shades
        '''
        collided_tiles = []
        for tile in level:
            if pygame.sprite.collide_rect(self, tile):
                collided_points = []
                if self.rect.collidepoint(tile.rect.topright):
                    collided_points.append(tile.rect.topright)
                if self.rect.collidepoint(tile.rect.topleft):
                    collided_points.append(tile.rect.topleft)
                if self.rect.collidepoint(tile.rect.bottomright):
                    collided_points.append(tile.rect.bottomright)
                if self.rect.collidepoint(tile.rect.bottomleft):
                    collided_points.append(tile.rect.bottomleft)
                collided_tiles.append(collided_points)
        collided_points = []
        for points in collided_tiles:
            exit_value = sorted(points, key=lambda x: math.atan2(x[1] - self.rect.centery, x[0] - self.rect.centerx))
            # collided_points.append((exit_value[0], exit_value[-1]))  # Нужные точки уже отсортированные
            values = (exit_value[-1], exit_value[0], self.count_iterable(exit_value[0]), self.count_iterable(exit_value[-1]))
            pygame.draw.polygon(
                surface, 
                COLORS['background_color'], 
                values
            )
            # self.mask_image = self.image
            # pygame.draw.polygon(
            #     self.mask_image,
            #     COLORS['background_color'],
            #     values
            # )
            # self.mask_image.set_colorkey(COLORS['background_color'])
            # self.mask = pygame.mask.from_surface(self.mask_image)
        

    def count_iterable(self, value) -> tuple((int, int)):
        # Наша прямоя имеет вид 
        # (x - self.rect.centerx)/(value[0] - self.rect.centerx) = (y - self.rect.centery)/(value[1] - self.rect.centery)
        # Надо найти точки пересечения ее с прямыми {
        # x = 0
        # x = CONSTANTS['WIDTH']
        # y = 0
        # y = CONSTANTS['HEIGHT']
        # }
        # k = (value[0] - self.rect.centerx)/(x - self.rect.centerx)
        x1, y1, x2, y2 = self.rect.centerx, self.rect.centery, value[0], value[1]
        
        try:
            x0 = -y1*(x2-x1)/(y2-y1) + x1 # подставляю y = 0
            xh = (CONSTANTS['HEIGHT']-y1)*(x2-x1)/(y2-y1) + x1  # подставляю y = height
            if (x2 - x1)/(x0 - x1) > 0:
                xf = (x0, 0)
            else:
                xf = (xh, CONSTANTS['HEIGHT'])
        except ZeroDivisionError:
            xf1 = (0, y1)
            xf2 = (CONSTANTS['WIDTH'], y1)
            if x1 <= CONSTANTS['WIDTH']:
                return xf1
            else:
                return xf2
        
        try:
            y0 = -x1*(y2-y1)/(x2-x1) + y1  # подставляю x = 0
            yw = (CONSTANTS['WIDTH']-x1)*(y2-y1)/(x2-x1) + y1  # подставляю x = width
            if (y2 - y1)/(y0 - y1) > 0:
                yf = (0, y0)
            else:
                yf = (CONSTANTS['WIDTH'], yw)
        except ZeroDivisionError:
            yf1 = (0, y1)
            yf2 = (CONSTANTS['WIDTH'], y1)
            if y1 <= CONSTANTS['HEIGHT']:
                return yf1
            else:
                return yf2
        
        
        if self.rect.centerx - xf[0] + self.rect.centery - xf[1] >= self.rect.centerx - yf[0] + self.rect.centery - yf[1]:
            return xf
        else:
            return yf
        # return xf
        


