import time
from random import randint
import pygame
from pygame import *
pygame.init()

background_color = (255, 255, 255)
win_width = 700
win_height = 600

window = pygame.display.set_mode((win_width, win_height))
window.fill(background_color)

platform_1_score = 0
platform_2_score = 0


class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_width, sprite_height, sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (sprite_width, sprite_height))
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y
        self.speed = sprite_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Platform:
    def __init__(self, sprite_color, sprite_x, sprite_y, sprite_width, sprite_height, sprite_speed):
        self.color = sprite_color
        self.rect = pygame.Rect(sprite_x, sprite_y, sprite_width, sprite_height)
        self.speed = sprite_speed

    def reset(self):
        pygame.draw.rect(window, self.color, self.rect)

    def update_1(self):
        keys = pygame.key.get_pressed()
        if keys[K_w] and self.rect.top >= 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.bottom <= win_height:
            self.rect.y += self.speed

    def update_2(self):
        keys = pygame.key.get_pressed()
        if keys[K_UP] and self.rect.top >= 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom <= win_height:
            self.rect.y += self.speed


class Ball(GameSprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_width, sprite_height, sprite_speed_y, sprite_speed_x):
        self.image = transform.scale(image.load(sprite_image), (sprite_width, sprite_height))
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y
        self.speed_y = sprite_speed_y
        self.speed_x = sprite_speed_x
        self.angle = 0

    def movement(self):
        # pygame.draw.rect(window, (255, 255, 255), self.rect, 2)
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0:
            self.speed_y = -self.speed_y
        if self.rect.bottom >= win_height:
            self.rect.bottom = win_height
            self.speed_y = -self.speed_y

        if self.rect.y >= win_height:
            self.rect.x = randint(50, win_width - 80)
            self.rect.y = 0
            self.angle = 0
        self.angle += self.speed_x

        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.rect = rotated_image.get_rect(center=self.rect.center)
        window.blit(rotated_image, self.rect.topleft)

        # if self.rect.left <= 0:
        #     self.speed_x = -self.speed_x
        # if self.rect.right >= win_width:
        #     self.rect.right = win_width
        #     self.speed_x = -self.speed_x


x = win_width // 2
y = win_height // 2

ball = Ball('ball.png', x, y, 50, 50, randint(4, 6), randint(4, 6))
platform_2 = Platform((0, 0, 0), win_width - 95, win_height // 2, 30, 160, 4)
platform_1 = Platform((0, 0, 0), 50, win_height // 2, 30, 160, 4)

font = pygame.font.Font(None, 70)

fps = 60
clock = time.Clock()
game = True
finish = False
state = 'game'
while game:
    for e in event.get():
        if e.type == pygame.QUIT:
            game = False
    if not finish:
        if state == 'game':
            window.fill(background_color)
            # ball.reset()
            platform_1.reset()
            platform_2.reset()
            platform_1.update_1()
            platform_2.update_2()
            ball.movement()

            if ball.rect.colliderect(platform_1.rect):
                # ball.speed_y = -ball.speed_y
                ball.speed_x = -ball.speed_x
            if ball.rect.colliderect(platform_2.rect):
                # ball.speed_y = -ball.speed_y
                ball.speed_x = -ball.speed_x

            text_lose = font.render(str(platform_1_score) + ' - ' + str(platform_2_score), True, (0, 0, 0))
            window.blit(text_lose, (300, 20))

            if ball.rect.x <= 0:
                platform_1_score += 1
                ball = Ball('ball.png', x, y, 50, 50, randint(4, 6), randint(4, 6))
                ball.movement()
            elif ball.rect.x >= win_width:
                platform_2_score += 1
                ball = Ball('ball.png', x, y, 50, 50, randint(4, 6), randint(4, 6))
                ball.movement()

    pygame.display.update()
    clock.tick(fps)
