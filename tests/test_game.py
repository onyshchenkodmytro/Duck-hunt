import sys
import os
import pygame
import pytest
from unittest.mock import MagicMock

# Додаємо корінь проєкту в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game.game_logic import Game

@pytest.fixture(autouse=True)
def mock_pygame(monkeypatch):
    """
    Мок для pygame:
     - встановлює dummy video driver,
     - створює поверхню замість реального вікна,
     - повертає Surface з альфа-каналом при load,
     - мок для transform.scale,
     - повертає DummyFont для тексту.
    """
    # Використовуємо headless режим для SDL
    os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
    pygame.init()
    # Встановлюємо мінімальний відео режим
    pygame.display.set_mode((1, 1))

    # Мок display.set_mode → повертає реальний Surface
    monkeypatch.setattr(pygame.display, 'set_mode', lambda size: pygame.Surface(size))
    # Мок caption (нічого не робить)
    monkeypatch.setattr(pygame.display, 'set_caption', lambda title: None)

    # Мок завантаження зображень → повертає Surface з альфа-каналом
    monkeypatch.setattr(pygame.image, 'load', lambda path: pygame.Surface((1, 1), pygame.SRCALPHA))
    # Мок transform.scale → повертає ту ж поверхню
    monkeypatch.setattr(pygame.transform, 'scale', lambda surf, size: surf)

    # Dummy‐фонт із методом render, який повертає Surface
    class DummyFont:
        def render(self, text, aa, color):
            return pygame.Surface((1, 1), pygame.SRCALPHA)
    monkeypatch.setattr(pygame.font, 'SysFont', lambda name, size: DummyFont())

    yield

    pygame.quit()

@pytest.fixture
def game(monkeypatch):
    # Мокуємо save_score, щоб не писати файл фізично
    monkeypatch.setattr(Game, 'save_score', lambda self: None)
    # Мокуємо show_game_over, щоб уникнути безкінечного циклу очікування подій
    monkeypatch.setattr(Game, 'show_game_over', lambda self: None)
    # Створюємо екземпляр гри
    g = Game(difficulty="easy")
    # Мокуємо player, щоб цикл гри одразу завершився
    g.player = MagicMock()
    g.player.is_alive.return_value = False
    g.player.score = 0
    return g


def test_game_quits_if_player_dead(game):
    # Запуск start() повинен одразу вийти (player.is_alive → False)
    game.start()
    # Якщо дійшли сюди без помилок – тест пройшов успішно
    assert True