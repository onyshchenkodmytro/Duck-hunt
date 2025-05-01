import sys
import os
# Додаємо корінь проєкту в шлях імпорту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import pytest
from game.duck import Duck

@pytest.fixture(autouse=True)
def init_pygame_display():
    # Перед створенням Duck забезпечуємо video mode
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()

@pytest.fixture
def duck():
    return Duck(speed=3)


def test_duck_initial_position(duck):
    assert duck.rect.y == duck.ground_level
    assert duck.alive is True


def test_duck_set_random_direction_changes_values(duck):
    dx_before, dy_before = duck.dx, duck.dy
    duck.set_random_direction()
    assert (duck.dx, duck.dy) != (dx_before, dy_before)
