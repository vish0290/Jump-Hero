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
        "idle": ["graphics/Sprites/3 Dude_Monster/Dude_Monster_Idle_4.png", 4],
        "run": ["graphics/Sprites/3 Dude_Monster/Dude_Monster_Run_6.png", 6],
        "jump": ["graphics/Sprites/3 Dude_Monster/Dude_Monster_Jump_8.png", 8],
        "dead": ["graphics/Sprites/3 Dude_Monster/Dude_Monster_Death_8.png", 8],
        "hurt": ["graphics/Sprites/3 Dude_Monster/Dude_Monster_Hurt_4.png", 4],
    }
    for keys, values in image_data.items():
        image_data[keys] = fetchFrames(values[0], values[1])

    return image_data


def fetchFrames(filename, frame_count) -> dict:
    directions = ["right", "left"]
    sprites = SpriteSheet(filename)
    frames = {}
    for direction in directions:
        frames[direction] = []
        for i in range(0, frame_count):
            frames[direction].append(
                sprites.image_at((i * 32, 0, 32, 32), direction == "left")
            )
    return frames
