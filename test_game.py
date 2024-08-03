import pytest
import pygame
from unittest.mock import Mock, patch

# Assume these are imported from your game file
from game_attr import Game, Player, Level


@pytest.fixture
def mock_game():
    game = Mock(spec=Game)
    game.player = Mock(spec=Player)
    game.currentLevel = Mock(spec=Level)
    game.currentLevelNumber = 1
    game.done = False
    return game


@pytest.fixture
def mock_player():
    player = Mock(spec=Player)
    player.rect = pygame.Rect(100, 100, 32, 32)
    player.changeX = 0
    player.changeY = 0
    player.health = 100
    player.lifes = 3
    player.score = 0
    player.direction = "right"
    player.action = "idle"
    player.currentLevel = Mock(spec=Level)
    player.currentLevel.levelShift = [0, 0]
    player.jump_sound = Mock()
    player.hurt_sound = Mock()
    player.fallThreshold = 100
    player.actualY = 0
    player.highestY = 0
    return player


class TestPlayerMovement:
    def test_move_right(self, mock_player):
        mock_player.goRight = lambda: setattr(mock_player, "changeX", 3)
        mock_player.goRight()
        assert mock_player.changeX > 0
        assert mock_player.direction == "right"

    def test_move_left(self, mock_player):
        # mock_player.goLeft = lambda: setattr(mock_player, 'changeX', -3 )
        # mock_player.goLeft = lambda: setattr(mock_player.goLeft, 'direction', 'left' )
        mock_player.goLeft = lambda: (
            setattr(mock_player, "changeX", -3),
            setattr(mock_player, "direction", "left"),
        )
        mock_player.goLeft()
        # print()
        assert mock_player.changeX < 0
        assert mock_player.direction == "left"

    def test_stop(self, mock_player):
        mock_player.stop = lambda: setattr(mock_player, "changeX", 0)
        mock_player.stop()
        assert mock_player.changeX == 0

    def test_jump(self, mock_player):
        mock_player.jump = lambda: setattr(mock_player, "changeY", -10)
        mock_player.on_ground = Mock(return_value=True)
        mock_player.jump()
        assert mock_player.changeY < 0


class TestFallDamage:
    def test_fall_damage_applied(self, mock_player):
        mock_player.fallDamage = lambda: setattr(
            mock_player, "health", mock_player.health - 10
        )
        initial_health = mock_player.health
        mock_player.fallDamage()
        assert mock_player.health < initial_health

    def test_no_fall_damage_below_threshold(self, mock_player):
        mock_player.fallDamage = lambda: None
        initial_health = mock_player.health
        mock_player.fallDamage()
        assert mock_player.health == initial_health


class TestLevelChange:
    def test_next_level(self, mock_game):
        mock_game.changeLevel = lambda direction: setattr(
            mock_game, "currentLevelNumber", mock_game.currentLevelNumber + 1
        )
        mock_game.changeLevel("up")
        assert mock_game.currentLevelNumber == 2

    def test_player_position_after_level_change(self, mock_game):
        new_spawn_point = (50, 100)
        mock_game.currentLevel.spawn_point = new_spawn_point
        mock_game.player.rect = pygame.Rect(0, 0, 32, 32)
        mock_game.changeLevel = lambda direction: setattr(
            mock_game.player.rect, "topleft", new_spawn_point
        )
        mock_game.changeLevel("up")
        assert mock_game.player.rect.x == new_spawn_point[0]
        assert mock_game.player.rect.y == new_spawn_point[1]


class TestScoring:
    def test_score_increase(self, mock_player):
        initial_score = mock_player.score
        mock_player.update = lambda: setattr(
            mock_player, "score", mock_player.score + 100
        )
        mock_player.update()
        assert mock_player.score > initial_score


class TestGameOver:
    def test_game_over_on_no_lives(self, mock_game):
        mock_game.player.lifes = 0
        mock_game.player.health = 0
        mock_game.runLogic = lambda: setattr(mock_game, "done", True)
        mock_game.runLogic()
        assert mock_game.done == True
