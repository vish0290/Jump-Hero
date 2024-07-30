import pytest
import pygame
from unittest.mock import MagicMock, patch
from settings import *
from frames import *
from game import Game, Player, Level, Layer, Tile


@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    with patch("pygame.display.set_mode"), patch("pygame.display.update"), patch(
        "pygame.display.flip"
    ), patch("pygame.event.get"), patch("pygame.time.get_ticks"):
        yield
    pygame.quit()


@pytest.fixture
def game():
    with patch("pygame.event.get"), patch("pygame.time.get_ticks"), patch.object(
        Game, "draw"
    ), patch("game.Level") as MockLevel:
        game = Game()
        game.currentLevel = MockLevel.return_value
        game.currentLevel.mapObject = MagicMock()
        game.currentLevel.mapObject.height = 10
        game.currentLevel.mapObject.tileheight = 32
        game.currentLevel.mapObject.width = 10
        game.currentLevel.mapObject.tilewidth = 32
        game.currentLevel.layers = [MagicMock(), MagicMock(), MagicMock()]
        game.currentLevel.layers[1].tiles = pygame.sprite.Group()
        game.currentLevel.layers[2].tiles = pygame.sprite.Group()
        game.player.currentLevel = game.currentLevel
        yield game


def test_player_wall_collision(game):
    # Add a wall tile to the level
    wall_tile = Tile(
        image=pygame.Surface((32, 32)), x=game.player.rect.x + 1, y=game.player.rect.y
    )
    game.currentLevel.layers[2].tiles.add(wall_tile)

    # Move player towards the wall
    game.player.changeX = 3
    game.player.wallCollide()

    # Check if the player's right side is at the wall's left side
    assert game.player.rect.right == wall_tile.rect.left


def test_player_movement_left(game):
    # Move player left
    game.player.goLeft()

    # Check if the player's changeX is set to -3
    assert game.player.changeX == -3

    # Stop the player
    game.player.stop()

    # Check if the player's changeX is set to 0
    assert game.player.changeX == 0


def test_player_movement_right(game):
    # Move player right
    game.player.goRight()

    # Check if the player's changeX is set to 3
    assert game.player.changeX == 3

    # Stop the player
    game.player.stop()

    # Check if the player's changeX is set to 0
    assert game.player.changeX == 0


def test_player_jump(game):
    # Ensure the player is on the ground
    ground_tile = Tile(
        image=pygame.Surface((32, 32)), x=game.player.rect.x, y=game.player.rect.y + 1
    )
    game.currentLevel.layers[1].tiles.add(ground_tile)

    # Make the player jump
    game.player.jump()

    # Check if the player's changeY is set to -10
    assert game.player.changeY == -10


def test_player_gravity_application(game):
    # Ensure the player is not on the ground
    game.currentLevel.layers[1].tiles.empty()

    # Apply gravity
    game.player.applyGravity()

    # Check if the player's changeY is incremented
    assert game.player.changeY == 0.35


def test_player_update(game):
    # Update the player
    game.player.update()

    # Check if the player's position has changed
    assert game.player.rect.x == 0
    assert game.player.rect.y == 0


def test_level_shiftLevel(game):
    # Shift the level
    game.currentLevel.shiftLevel(10, 10)

    # Check if the levelShift has been updated
    assert game.currentLevel.levelShift == [10, 10]


def test_layer_draw(game):
    # Create a screen surface
    screen = pygame.Surface((screen_width, screen_height))

    # Draw the layer
    game.currentLevel.layers[0].draw(screen)

    # Check if the screen has been updated
    assert screen.get_at((0, 0)) == (0, 0, 0, 255)


def test_tile_init(game):
    # Initialize a tile
    tile = Tile(image=pygame.Surface((32, 32)), x=0, y=0)

    # Check if the tile's position is set correctly
    assert tile.rect.x == 0
    assert tile.rect.y == 0
