import pygame
import pytmx
from settings import *
from frames import *


class Game(object):
    def __init__(self):
        self.currentLevelNumber = 0
        self.levels = {
            "level1": Level(fileName="graphics/maps/level1.tmx"),
            "level2": Level(fileName="graphics/maps/level2.tmx"),
            "level3": Level(fileName="graphics/maps/level3.tmx"),
        }
        self.done = False
        self.level_names = list(self.levels.keys())
        self.currentLevel = self.levels["level1"]
        self.player = Player(
            x=self.currentLevel.spawn_point[0], y=self.currentLevel.spawn_point[1]
        )
        self.player.currentLevel = self.currentLevel
        self.score = 0
        self.main_score = 0
        self.start_ticks = pygame.time.get_ticks()

    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.goLeft()
                elif event.key == pygame.K_RIGHT:
                    self.player.goRight()
                elif event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_UP:
                    self.player.goup()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.changeX < 0:
                    self.player.stop()
                elif event.key == pygame.K_RIGHT and self.player.changeX > 0:
                    self.player.stop()

        return self.done

    def runLogic(self):
        self.player.update()
        self.score = self.player.score
        self.health = self.player.health
        self.lifes = self.player.lifes

        if self.player.next_level():
            self.main_score += self.score
            self.changeLevel("up")
        elif self.player.below_level():
            self.changeLevel("down")

    def changeLevel(self, direction):

        if direction == "up":
            self.currentLevelNumber += 1

            self.currentLevel = self.levels[self.level_names[self.currentLevelNumber]]
            self.player = Player(
                x=self.currentLevel.spawn_point[0], y=self.currentLevel.spawn_point[1]
            )
            self.player.currentLevel = self.currentLevel

        elif direction == "down":
            self.currentLevelNumber -= 1
            self.currentLevel = self.levels[self.level_names[self.currentLevelNumber]]
            self.player = Player(
                x=self.currentLevel.spawn_point[0], y=self.currentLevel.spawn_point[1]
            )
            self.player.currentLevel = self.currentLevel

    def draw(self, screen):
        screen.fill(background)
        self.currentLevel.draw(screen)
        self.player.draw(screen)
        score = self.scorecard()
        screen.blit(score, (10, 10))
        if debug_frames:
            pygame.draw.rect(
                screen, (0, 255, 0), self.player.rect, 2
            )  # Player bounding box
            for tile in self.currentLevel.layers[1].tiles:
                pygame.draw.rect(
                    screen, (0, 0, 255), tile.rect, 2
                )  # Ground tile bounding boxes
            for tile in self.currentLevel.layers[2].tiles:
                pygame.draw.rect(screen, (255, 0, 0), tile.rect, 2)
        pygame.display.flip()

    def gameover(self, screen):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        if self.player.lifes == 0:
            text = font.render("Game Over", True, (255, 255, 255))
            text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(text, text_rect)
            pygame.display.flip()

    def scorecard(self):
        font = pygame.font.Font(None, 36)
        score_text = f"Score: {self.score+self.main_score}"
        health_text = f"Health: {self.health}"
        lifes_text = f"Lives: {self.lifes}"
        elapsed_seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        hours = int(elapsed_seconds // 3600)
        minutes = int((elapsed_seconds % 3600) // 60)
        seconds = int(elapsed_seconds % 60)
        timer_text = f"{hours:02}:{minutes:02}:{seconds:02}"
        text_surface = font.render(
            f"{score_text}  |  {health_text}  |  {lifes_text} | {timer_text}",
            True,
            (255, 255, 255),
        )
        return text_surface


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Load the spritesheet of frames for this player
        self.newplayerframes = playerFrames()
        self.image = self.newplayerframes["idle"]["right"][0]
        self.health = 100
        self.lifes = 3
        self.score = 0

        # Set player position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Set speed and direction
        self.changeX = 0
        self.changeY = 0
        self.direction = "right"
        self.action = "idle"

        # Boolean to check if player is running, current running frame, and time since last frame change
        self.running = False
        self.runningFrame = 0
        self.runningTime = pygame.time.get_ticks()

        # Player's current level, set after object initialized in game constructor
        self.currentLevel = None

        self.highestY = map_height
        self.actualY = map_height
        self.fallThreshold = 350
        self.start_ticks = pygame.time.get_ticks()

    def on_ground(self):
        self.rect.y += 1
        on_ground = pygame.sprite.spritecollideany(
            self, self.currentLevel.layers[1].tiles
        )
        self.rect.y -= 1
        return on_ground

    def applyGravity(self):
        if not self.on_ground():
            self.changeY += 0.35
        else:
            self.changeY = 0

    def fallDamage(self):
        fall_height = (self.rect.y - self.currentLevel.levelShift[1]) - self.actualY
        if fall_height > self.fallThreshold:
            self.health -= 10 * (fall_height - self.fallThreshold) // 100
            if self.health <= 0:
                self.lifes -= 1
                self.health = 100
                if self.lifes <= 0:
                    self.done = True  # End the game if no lives are left
            print(
                f"Fall damage taken. Fall height: {fall_height}, Health: {self.health}, Lives: {self.lifes}"
            )

    def jump(self):
        if self.on_ground():
            self.changeY = -10
            self.action = "jump"

    def goRight(self):
        self.action = "run"
        self.direction = "right"
        self.running = True
        self.changeX = 3

    def goLeft(self):
        self.action = "run"
        self.direction = "left"
        self.running = True
        self.changeX = -3

    def goup(self):
        if god_mode:
            self.action = "jump"
            self.changeY = -3

    def stop(self):
        self.running = False
        self.changeX = 0
        self.action = "idle"

    def wallCollide(self):
        collided_tile = pygame.sprite.spritecollideany(
            self, self.currentLevel.layers[2].tiles
        )
        if collided_tile:
            if self.changeX > 0:
                self.rect.right = collided_tile.rect.left
            else:
                self.rect.left = collided_tile.rect.right

    def ceilingCollide(self):
        collided_tile = pygame.sprite.spritecollideany(
            self, self.currentLevel.layers[2].tiles
        )
        if collided_tile:
            if self.changeY < 0:
                self.rect.top = collided_tile.rect.bottom
                self.changeY = 0

    def floating_floor_collide(self):
        collided_tile = pygame.sprite.spritecollideany(
            self, self.currentLevel.layers[1].tiles
        )
        if collided_tile:
            if self.changeY < 0:
                self.rect.top = collided_tile.rect.bottom
                self.changeY = 0

    def groudCollide(self):
        if self.on_ground() and self.changeX >= 0 or self.changeX < 0:
            collided_tile = pygame.sprite.spritecollideany(
                self, self.currentLevel.layers[1].tiles
            )
            if collided_tile:
                if self.direction == "right":
                    self.rect.left = collided_tile.rect.right
                else:
                    self.rect.right = collided_tile.rect.left

    def next_level(self) -> bool:
        if not self.on_ground():
            collided_tile = pygame.sprite.spritecollideany(
                self, self.currentLevel.layers[4].tiles
            )
            if collided_tile:
                return True
                print("Next level")
            else:
                return False
                print("Not next level")

    def below_level(self) -> bool:
        if not self.on_ground():
            collided_tile = pygame.sprite.spritecollideany(
                self, self.currentLevel.layers[5].tiles
            )
            if collided_tile:
                return True
            else:
                return False

    def update(self):
        self.groudCollide()
        self.rect.x += self.changeX
        self.rect.y += self.changeY
        self.ceilingCollide()
        self.floating_floor_collide()
        if not god_mode:
            self.applyGravity()
        self.wallCollide()

        if self.on_ground() and self.changeY >= 0:
            self.changeY = 0
            collided_tile = pygame.sprite.spritecollideany(
                self, self.currentLevel.layers[1].tiles
            )
            if collided_tile:
                self.rect.bottom = collided_tile.rect.top

        # Camera to update map based on player position
        map_height = (
            self.currentLevel.mapObject.height * self.currentLevel.mapObject.tileheight
        )
        if self.rect.right >= screen_width - 200:
            difference = self.rect.right - (screen_width - 200)
            self.rect.right = screen_width - 200
            self.currentLevel.shiftLevel(-difference, 0)
        elif self.rect.left <= 200:
            difference = 200 - self.rect.left
            self.rect.left = 200
            self.currentLevel.shiftLevel(difference, 0)

        if self.rect.top <= 200 and self.currentLevel.levelShift[1] < 0:
            difference = 200 - self.rect.top
            self.rect.top = 200
            self.currentLevel.shiftLevel(0, difference)

        elif self.rect.bottom >= screen_height - 200 and self.currentLevel.levelShift[
            1
        ] > -(map_height - screen_height):
            difference = self.rect.bottom - (screen_height - 200)
            self.rect.bottom = screen_height - 200
            self.currentLevel.shiftLevel(0, -difference)

        if (
            self.rect.y - self.currentLevel.levelShift[1]
        ) < self.actualY and self.on_ground():
            self.actualY = self.rect.y - self.currentLevel.levelShift[1]
            if self.actualY < self.highestY:
                self.highestY = self.actualY
                self.score += 100

        if (
            self.actualY < (self.rect.y - self.currentLevel.levelShift[1])
            and self.on_ground()
        ):
            self.fallDamage()
            self.actualY = self.rect.y - self.currentLevel.levelShift[1]

        print(
            f"player y: {self.actualY}, highest y: {self.highestY}, score: {self.score}"
        )
        # Update the player's animation frame
        try:
            self.image = self.newplayerframes[self.action][self.direction][
                self.runningFrame
            ]
        except:
            pass  # few sprites are missing because there are less frames in few actions
        now = pygame.time.get_ticks()
        if now - self.runningTime > 200:
            self.runningTime = now
            self.runningFrame = (self.runningFrame + 1) % len(
                self.newplayerframes[self.action][self.direction]
            )

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Level(object):
    def __init__(self, fileName):
        self.mapObject = pytmx.load_pygame(fileName)
        self.layers = []
        self.levelShift = [0, 0]
        self.spawn_point = None
        for layer in range(len(self.mapObject.layers)):
            self.layers.append(Layer(index=layer, mapObject=self.mapObject))

        self.set_spawn_point()

    def set_spawn_point(self):
        spawn_layer_name = "spawn_point"
        spawn_layer = None

        for layer in self.mapObject.visible_layers:
            if (
                isinstance(layer, pytmx.TiledTileLayer)
                and layer.name == spawn_layer_name
            ):
                spawn_layer = layer
                break

        # If the spawn layer is found, determine the spawn point
        if spawn_layer:
            # Iterate over tiles in the spawn layer
            for x, y, image in spawn_layer.tiles():
                if image:  # If there's a tile image, consider it the spawn point
                    self.spawn_point = (
                        x * self.mapObject.tilewidth,
                        y * self.mapObject.tileheight + 1,
                    )
                    break

        # If no spawn point is defined, set a default spawn point
        if not self.spawn_point:
            self.spawn_point = (
                50,
                self.mapObject.height * self.mapObject.tileheight - 100,
            )  # Default position

    def shiftLevel(self, shiftX, shiftY):

        self.levelShift[0] += shiftX
        self.levelShift[1] += shiftY

        for layer in self.layers:
            for tile in layer.tiles:
                tile.rect.x += shiftX
                tile.rect.y += shiftY

    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)


class Layer(object):
    def __init__(self, index, mapObject):
        self.index = index
        self.tiles = pygame.sprite.Group()
        self.mapObject = mapObject
        for x in range(self.mapObject.width):
            for y in range(self.mapObject.height):
                img = self.mapObject.get_tile_image(x, y, self.index)
                if img:
                    self.tiles.add(
                        Tile(
                            image=img,
                            x=(x * self.mapObject.tilewidth),
                            y=(y * self.mapObject.tileheight),
                        )
                    )

    def draw(self, screen):
        self.tiles.draw(screen)


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
