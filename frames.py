import pygame


class SpriteSheet(object):
    def __init__(self, fileName):
        self.sheet = pygame.image.load(fileName)

    def image_at(self, rectangle, flip):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if flip:
            image = pygame.transform.flip(image, True, False)
        return image


def playerFrames() -> dict:

    image_data = {
        "idle": "graphics/Sprites/01-King Human/Idle (78x58).png",
        "run": "graphics/Sprites/01-King Human/Run (78x58).png",
        "jump": "graphics/Sprites/01-King Human/Jump (78x58).png",
        "fall": "graphics/Sprites/01-King Human/Fall (78x58).png",
        "attack": "graphics/Sprites/01-King Human/Attack (78x58).png",
    }
    action = {"idle": 11, "run": 11, "jump": 4, "attack": 5}
    direction = ["right", "left"]


def fetchFrames() -> dict:
    directions = ["right", "left"]


def player_idle_right() -> tuple:
    sprites = SpriteSheet("graphics/Sprites/01-King Human/Idle (78x58).png")
    frames = []
    for i in range(0, 11):
        frames.append(sprites.image_at((i * 78 + 5, 10, 45, 35), False))

    return tuple(frames)


def player_idle_left() -> tuple:
    sprites = SpriteSheet("graphics/Sprites/01-King Human/Idle (78x58).png")
    frames = []
    for i in range(0, 11):
        frames.append(sprites.image_at((i * 78 + 5, 10, 45, 35), True))
    return tuple(frames)


def player_walk_right() -> tuple:
    sprites = SpriteSheet("graphics/Sprites/01-King Human/Run (78x58).png")
    frames = []
    for i in range(0, 11):
        frames.append(sprites.image_at((i * 78 + 5, 10, 45, 35), False))
    return tuple(frames)


def player_walk_left() -> tuple:
    sprites = SpriteSheet("graphics/Sprites/01-King Human/Run (78x58).png")
    frames = []
    for i in range(0, 11):
        frames.append(sprites.image_at((i * 78 + 5, 10, 45, 35), True))

    return tuple(frames)


def player_jump_right() -> tuple:
    sprites_1 = SpriteSheet("graphics/Sprites/01-King Human/Run (78x58).png")
    sprites_2 = SpriteSheet("graphics/Sprites/01-King Human/Jump (78x58).png")
    sprites_3 = SpriteSheet("graphics/Sprites/01-King Human/Fall (78x58).png")
    frames = (
        sprites_1.image_at((0, 0, 58, 44), False),
        sprites_2.image_at((0, 0, 58, 44), False),
        sprites_3.image_at((0, 0, 58, 44), False),
        sprites_1.image_at((0, 0, 58, 44), False),
    )
    return frames


def player_jump_left() -> tuple:
    sprites_1 = SpriteSheet("graphics/Sprites/01-King Human/Run (78x58).png")
    sprites_2 = SpriteSheet("graphics/Sprites/01-King Human/Jump (78x58).png")
    sprites_3 = SpriteSheet("graphics/Sprites/01-King Human/Fall (78x58).png")
    frames = (
        sprites_1.image_at((0, 0, 58, 44), True),
        sprites_2.image_at((0, 0, 58, 44), True),
        sprites_3.image_at((0, 0, 58, 44), True),
        sprites_1.image_at((0, 0, 58, 44), True),
    )
    return frames


def player_attack_right() -> tuple:
    sprites = SpriteSheet("graphics/Sprites/01-King Human/Attack (78x58).png")
    frames = []
    for i in range(0, 5):
        frames.append(sprites.image_at((i * 78, 0, 78, 58), False))
    return tuple(frames)


def player_attack_left() -> tuple:
    sprites = SpriteSheet("graphics/Sprites/01-King Human/Attack (78x58).png")
    frames = []
    for i in range(0, 5):
        frames.append(sprites.image_at((i * 78, 0, 78, 58), True))
    return tuple(frames)


def basicpigframes():
    actions = {
        "idle": [11, "graphics/Sprites/03-Pig/Idle (34x28).png"],
        "run": [6, "graphics/Sprites/03-Pig/Run (34x28).png"],
        "attack": [5, "graphics/Sprites/03-Pig/Attack (34x28).png"],
        "hit": [2, "graphics/Sprites/03-Pig/Hit (34x28).png"],
        "death": [6, "graphics/Sprites/03-Pig/Dead (34x28).png"],
    }
    directions = ["right", "left"]
    frames = {}
    for action, values in actions.items():
        frames[action] = {}
        for direction in directions:
            frames[action][direction] = []
            for i in range(0, values[0]):
                sprites = SpriteSheet(values[1])
                frames[action][direction].append(
                    sprites.image_at((i * 78, 0, 78, 58), direction == "left")
                )
