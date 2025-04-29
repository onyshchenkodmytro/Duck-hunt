import pygame
import random
import json
import os
from game.duck import Duck
from game.player import Player
from game.timer import Timer
from game.ui import UIManager
from game.explosion import Explosion

class Game:
    def __init__(self, difficulty='easy'):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 452))
        pygame.display.set_caption("Duck Hunt")
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("assets/background.png")
        self.crosshair = pygame.image.load("assets/crosshair.png").convert_alpha()

        self.difficulty = difficulty
        self.player = Player()
        self.timer = Timer(6)
        self.ui = UIManager(self.player, self.timer)
        self.ducks = []
        self.explosions = []
        self.spawned_ducks = 0
        self.duck_speed = 3 if difficulty == 'easy' else 4
        self.ducks_at_once = 1 if difficulty == 'easy' else 2

    def spawn_ducks(self):
        while len(self.ducks) < self.ducks_at_once:
            self.ducks.append(Duck(self.duck_speed))
            self.spawned_ducks += 1
            if self.spawned_ducks % 10 == 0:
                self.duck_speed += 1

    def start(self):
        running = True
        self.spawn_ducks()

        while running and self.player.is_alive():
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.player.shoot():
                        for duck in self.ducks:
                            if duck.is_hit(pygame.mouse.get_pos()) and duck.alive:
                                duck.alive = False
                                self.player.score += 1
                                self.explosions.append(Explosion(duck.rect.center))
                                break  # Один постріл — одна качка

            # Update
            for duck in self.ducks:
                duck.update()
            for explosion in self.explosions:
                explosion.update()
            self.explosions = [e for e in self.explosions if not e.is_finished()]
            self.ducks = [d for d in self.ducks if d.alive]

            # Перевірка умови завершення раунду
            if self.timer.is_time_up() or self.player.bullets == 0 or \
                (self.difficulty == 'easy' and len(self.ducks) == 0) or \
                (self.difficulty == 'hard' and len(self.ducks) == 0 and self.player.bullets < 3):
                
                missed = len(self.ducks)
                self.player.lose_life(missed)
                self.ducks = []
                self.player.reload()
                self.timer.reset()
                if self.player.is_alive():
                    self.spawn_ducks()

            # Нарисувати все
            for duck in self.ducks:
                duck.draw(self.screen)
            for explosion in self.explosions:
                explosion.draw(self.screen)
            self.ui.draw(self.screen)
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.crosshair, (mouse_pos[0] - 20, mouse_pos[1] - 20))

            pygame.display.flip()
            self.clock.tick(60)

        self.save_score()
        self.show_game_over()
        pygame.quit()

    def save_score(self):
        scores_file = "scores.json"
        if os.path.exists(scores_file):
            with open(scores_file, "r") as f:
                scores = json.load(f)
        else:
            scores = []

        scores.append({
            "score": self.player.score,
            "difficulty": self.difficulty
        })

        scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:5]

        with open(scores_file, "w") as f:
            json.dump(scores, f, indent=4)

    def show_game_over(self):
        font = pygame.font.SysFont("Comic Sans MS", 48)
        small_font = pygame.font.SysFont("Comic Sans MS", 24)
        text = font.render("Game Over", True, (255, 0, 0))
        score_text = font.render(f"Score: {self.player.score}", True, (255, 255, 255))

        # Завантажити топ-5 результатів
        scores = []
        if os.path.exists("scores.json"):
            with open("scores.json", "r") as f:
                scores = json.load(f)

        self.screen.fill((0, 0, 0))
        self.screen.blit(text, text.get_rect(center=(400, 100)))
        self.screen.blit(score_text, score_text.get_rect(center=(400, 170)))

        self.screen.blit(small_font.render("Top 5 Scores:", True, (255, 255, 0)), (300, 220))
        for i, entry in enumerate(scores):
            s = f"{i+1}. {entry['score']} pts ({entry['difficulty']})"
            self.screen.blit(small_font.render(s, True, (255, 255, 255)), (300, 250 + i * 30))

        pygame.display.flip()


        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
