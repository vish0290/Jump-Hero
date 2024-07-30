import pytest
import pygame
from unittest.mock import patch, Mock
from game import Game, Player, Level


@pytest.fixture
def init_game():
    # Initialize the game without a graphical display
    pygame.display.init()
    screen = pygame.display.set_mode((800, 600))
    game = Game()
    yield game, screen
    pygame.display.quit()


def test_initial_player_position(init_game):
    game, screen = init_game
    player = game.player
    assert player.rect.x == game.currentLevel.spawn_point[0]
    assert player.rect.y == game.currentLevel.spawn_point[1]


def test_player_movement_right(init_game):
    game, screen = init_game
    initial_x = game.player.rect.x
    game.player.goRight()
    game.player.update()
    assert game.player.rect.x > initial_x


def test_player_movement_left(init_game):
    game, screen = init_game
    initial_x = game.player.rect.x
    game.player.goLeft()
    game.player.update()
    assert game.player.rect.x < initial_x


def test_player_jump(init_game):
    game, screen = init_game
    initial_y = game.player.rect.y
    game.player.jump()
    game.player.applyGravity()
    game.player.update()
    assert game.player.rect.y < initial_y


def test_change_level_up(init_game):
    game, screen = init_game
    game.currentLevelNumber = 0  # Assuming 'level1' is the first level
    game.changeLevel("up")
    assert game.currentLevelNumber == 1  # Should move to 'level2'


def test_change_level_down(init_game):
    game, screen = init_game
    game.currentLevelNumber = 2  # Assuming 'level3' is the last level
    game.changeLevel("down")
    assert game.currentLevelNumber == 1  # Should move to 'level2'


def test_player_health(init_game):
    game, screen = init_game
    initial_health = game.player.health
    game.player.health -= 20
    assert game.player.health == initial_health - 20


def test_game_over(init_game):
    game, screen = init_game
    game.player.health = 0
    assert game.processEvents() == True  # Game should end
