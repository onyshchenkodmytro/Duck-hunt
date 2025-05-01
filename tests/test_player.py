import pytest
from game.player import Player
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
@pytest.fixture
def player():
    return Player()

def test_initial_values(player):
    assert player.bullets == 3
    assert player.lives == 5
    assert player.score == 0

@pytest.mark.parametrize("shots,expected_bullets", [(1, 2), (2, 1), (3, 0)])
def test_shoot_reduces_bullets(player, shots, expected_bullets):
    for _ in range(shots):
        player.shoot()
    assert player.bullets == expected_bullets

def test_reload(player):
    player.bullets = 0
    player.reload()
    assert player.bullets == 3

def test_lose_life(player):
    player.lose_life(2)
    assert player.lives == 3

def test_is_alive(player):
    player.lives = 0
    assert not player.is_alive()
