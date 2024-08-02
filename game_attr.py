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
            "level4": "Victory",
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

        self.level_music = {
            "level1": "audio/level1.mp3",
            "level2": "audio/level2.mp3",
            "level3": "audio/level3.mp3",
            "level4": "audio/victory.mp3",
            "gameover": "audio/game_over.mp3",
        }
        self.currentLevel_music = None
        self.play_music("level1")
        self.victory = False

    def play_music(self, level):
        if self.currentLevel_music:
            self.currentLevel_music.stop()
        self.currentLevel_music = pygame.mixer.Sound(self.level_music[level])
        self.currentLevel_music.play(-1)

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
                elif event.key == pygame.K_DOWN:
                    self.player.godown()

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
            if self.currentLevelNumber == 2:
                self.victory = True
            else:
                self.changeLevel("up")
        elif self.player.below_level() and self.currentLevelNumber > 0:
            self.changeLevel("down")

    def changeLevel(self, direction):
        if direction == "up":
            self.currentLevelNumber += 1
        elif direction == "down":
            self.currentLevelNumber -= 1

        self.currentLevel = self.levels[self.level_names[self.currentLevelNumber]]

        if direction == "up":
            new_pos = self.currentLevel.spawn_point
        else:
            new_pos = self.currentLevel.drop_point

        print(f"Changing to level: {self.level_names[self.currentLevelNumber]}")
        print(f"New player position: {new_pos}")

        self.player = Player(x=new_pos[0], y=new_pos[1])
        self.player.currentLevel = self.currentLevel
        self.play_music(self.level_names[self.currentLevelNumber])

        print(f"Player rect after change: { self.player.rect}")

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

    def end_screen(self, screen, flag):
        screen.fill((0, 0, 0))  # Fill screen with black color

        # Define fonts
        title_font = pygame.font.Font(None, 72)
        text_font = pygame.font.Font(None, 36)

        if flag == "victory":
            title_text = "Victory"
            completion_text = "You have completed the game!"
        else:
            title_text = "Game Over"
            completion_text = "Better Luck Next Time!"
        # Define text content
        score_text = f"Score: {self.score + self.main_score}"
        elapsed_seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        hours = int(elapsed_seconds // 3600)
        minutes = int((elapsed_seconds % 3600) // 60)
        seconds = int(elapsed_seconds % 60)
        timer_text = f"Time: {hours:02}:{minutes:02}:{seconds:02}"

        # Render text surfaces
        title_surface = title_font.render(title_text, True, (255, 215, 0))  # Gold color
        completion_surface = text_font.render(
            completion_text, True, (255, 255, 255)
        )  # White color
        score_surface = text_font.render(
            score_text, True, (255, 255, 255)
        )  # White color
        timer_surface = text_font.render(
            timer_text, True, (255, 255, 255)
        )  # White color

        # Get text rectangles
        title_rect = title_surface.get_rect(
            center=(screen_width / 2, screen_height / 2 - 100)
        )
        completion_rect = completion_surface.get_rect(
            center=(screen_width / 2, screen_height / 2 - 20)
        )
        score_rect = score_surface.get_rect(
            center=(screen_width / 2, screen_height / 2 + 40)
        )
        timer_rect = timer_surface.get_rect(
            center=(screen_width / 2, screen_height / 2 + 80)
        )

        # Blit text surfaces onto the screen
        screen.blit(title_surface, title_rect)
        screen.blit(completion_surface, completion_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(timer_surface, timer_rect)
        if flag == "victory":
            self.play_music("level4")
        else:
            self.play_music("gameover")
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

        # game audio
        self.jump_sound = pygame.mixer.Sound("audio/jump.wav")
        self.hurt_sound = pygame.mixer.Sound("audio/hurt.wav")

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
            self.action = "hurt"
            self.hurt_sound.play()
            self.health -= 10 * (fall_height - self.fallThreshold) // 100
            if self.health <= 0:
                self.action = "dead"
                self.lifes -= 1
                self.health = 100
                if self.lifes <= 0:
                    self.done = True  # End the game if no lives are left

    def jump(self):
        if self.on_ground():
            self.changeY = -10
            self.action = "jump"
            self.jump_sound.play()

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

    def godown(self):
        if god_mode:
            self.action = "jump"
            self.changeY = 3

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
                self.changeY = 0
                return True
            else:
                return False

    def below_level(self) -> bool:
        if not self.on_ground():
            collided_tile = pygame.sprite.spritecollideany(
                self, self.currentLevel.layers[5].tiles
            )
            if collided_tile:
                self.changeY = 0
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
            f"player y: {self.actualY},{self.currentLevel.spawn_point[1]} highest y: {self.highestY}"
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
        self.drop_point = None
        for layer in range(len(self.mapObject.layers)):
            self.layers.append(Layer(index=layer, mapObject=self.mapObject))

        self.set_drop_point()
        self.set_spawn_point()
        print(f"Spawn point: {self.spawn_point}")

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
                        y * self.mapObject.tileheight - 1,
                    )
                    break

        # If no spawn point is defined, set a default spawn point
        if not self.spawn_point:
            self.spawn_point = (
                50,
                self.mapObject.height * self.mapObject.tileheight - 100,
            )  # Default position

    def set_drop_point(self):
        drop_layer_name = "below_level"
        drop_layer = None

        for layer in self.mapObject.visible_layers:
            if (
                isinstance(layer, pytmx.TiledTileLayer)
                and layer.name == drop_layer_name
            ):
                drop_layer = layer
                break

        # If the drop layer is found, determine the drop point
        if drop_layer:
            # Iterate over tiles in the drop layer
            for x, y, image in drop_layer.tiles():
                if image:
                    self.drop_point = (
                        x * self.mapObject.tilewidth,
                        y * self.mapObject.tileheight + 1,
                    )
                    break
                    # exit()

        if not self.drop_point:
            self.drop_point = (
                50,
                self.mapObject.height * self.mapObject.tileheight - 100,
            )

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
