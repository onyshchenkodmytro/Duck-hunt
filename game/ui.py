import pygame

class UIManager:
    def __init__(self, player, timer):
        self.player = player
        self.timer = timer
        self.font = pygame.font.SysFont("Comic Sans MS", 24)

    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.player.score}", True, (255, 253, 208))
        bullets_text = self.font.render(f"Bullets: {self.player.bullets}", True, (255, 253, 208))
        lives_text = self.font.render(f"Lives: {self.player.lives}", True, (255, 0, 0))
        time_text = self.font.render(f"Time: {int(self.timer.get_time_left())}", True, (255, 140, 0))

        screen.blit(score_text, (10, 10))
        screen.blit(bullets_text, (10, 40))
        screen.blit(lives_text, (10, 70))
        screen.blit(time_text, (10, 100))