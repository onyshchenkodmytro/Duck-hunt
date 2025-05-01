import pygame
import random


class Duck:
    def __init__(self, speed):
        self.image = pygame.image.load("assets/duck.png").convert_alpha()
        self.rect = self.image.get_rect()

        # Висоти для землі та трави
        self.ground_level = 196     # Верх землі (нижче летіти не можна)
        self.grass_top = 186       # Верх трави (після цього качка маневрує)

        # Початкова позиція
        self.rect.x = random.randint(100, 700)  # Обмежуємо, щоб не вилітала на дереві
        self.rect.y = self.ground_level          # Спавнимо на рівні землі

        # Стан качки
        self.alive = True
        self.speed = speed
        self.ascending = True  # Спочатку качка летить через траву вгору

        # Для випадкової зміни напряму (тільки після виліту з трави)
        self.change_direction_timer = random.randint(60, 180)

        # Стартова швидкість: тільки вгору
        self.dx = 0
        self.dy = -self.speed

    def set_random_direction(self):
        # Після виліту: випадковий політ
        angle = random.uniform(-0.5, 0.5)  # Невеликий кут
        self.dx = self.speed * random.uniform(0.7, 1.0) * random.choice([-1, 1])
        self.dy = self.speed * angle

    def update(self):
        if self.alive:
            self.rect.x += self.dx
            self.rect.y += self.dy

            if self.ascending:
                # Поки в траві — летить строго вгору
                if self.rect.top <= self.grass_top:
                    self.ascending = False
                    self.set_random_direction()
            else:
                # Відбивання від лівого та правого країв
                if self.rect.left < 0 or self.rect.right > 800:
                    self.dx = -self.dx

                # Відбивання від верху екрану
                if self.rect.top < 0:
                    self.rect.top = 0
                    self.dy = abs(self.dy)

                # Заборона залізати нижче землі
                if self.rect.top >= self.ground_level:
                    self.rect.top = self.ground_level
                    self.dy = -abs(self.dy)  # Після удару летить вгору

                # Зміна напряму через випадковий час
                self.change_direction_timer -= 1
                if self.change_direction_timer <= 0:
                    self.set_random_direction()
                    self.change_direction_timer = random.randint(60, 180)

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect)

    def is_hit(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
