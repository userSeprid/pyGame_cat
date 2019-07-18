import pygame
from pygame_functions import *
pygame.init()

DISPLAYSURF = pygame.display.set_mode((500, 500))
FPS = 30
run = True
is_jump = False
left = False
right = False
x = 100
y = 420
width = 60
height = 71
speed = 5
minX = 0
maxX = 440
minY = 0
maxY = 420
jump_count = 8
anim_count = 0
facing = 1

walkRight = [pygame.image.load('right_1.png'), pygame.image.load('right_2.png'),
             pygame.image.load('right_3.png'), pygame.image.load('right_4.png'),
             pygame.image.load('right_5.png'), pygame.image.load('right_6.png')]
walkLeft = [pygame.image.load('left_1.png'), pygame.image.load('left_2.png'),
            pygame.image.load('left_3.png'), pygame.image.load('left_4.png'),
            pygame.image.load('left_5.png'), pygame.image.load('left_6.png')]
playerStand = pygame.image.load('idle.png')
bg = pygame.image.load('bg.jpg')
bulletImage = pygame.image.load('bullet.png')

clock = pygame.time.Clock()

lastMove = "right"

bullets = []
platforms = []

bgX = 0
bgX2 = bg.get_width()


class Bullet:
    def __init__(self, bullet_x_pos, bullet_y_pos, radius, color, facing_direction):
        self.x = bullet_x_pos
        self.y = bullet_y_pos
        self.radius = radius
        self.color = color
        self.facing = facing_direction
        self.vel = 12 * facing_direction

    def draw(self, display_surface):
        display_surface.blit(bulletImage, (self.x, self.y - 10))
        # pygame.draw.circle(display_surface, self.color, (self.x, self.y), self.radius)

    @staticmethod
    def handle_bullet(bullets_array):
        for bullet in bullets_array:
            if 500 > bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets_array.pop(bullets_array.index(bullet))


class Platform:
    def __init__(self, platform_x_pos, platform_y_pos, platform_width, platform_height):
        self.x = platform_x_pos
        self.y = platform_y_pos
        self.width = platform_width
        self.height = platform_height
        self.vel = -1

    def draw(self, display_surface):
        pygame.draw.line(display_surface, (3, 252, 28), (self.x, self.y), (self.x + self.width, self.y), self.height)

    @staticmethod
    def handle_platform(platforms_array):
        for platform in platforms_array:
            if 500 > platform.x > 0:
                platform.x += platform.vel
                platform.y += platform.vel
            else:
                platforms_array.pop(platforms_array.index(platform))


platforms.append(Platform(200, 400, 100, 5))


pygame.display.set_caption("Base frame")


def draw_window():
    global anim_count
    # DISPLAYSURF.blit(bg, (0, 0))

    DISPLAYSURF.blit(bg, (bgX, 0))  # draws our first bg image
    DISPLAYSURF.blit(bg, (bgX2, 0))  # draws the seconf bg image
    pygame.display.update()  # updates the screen

    if anim_count + 1 >= 30:
        anim_count = 0

    if left:
        DISPLAYSURF.blit(walkLeft[anim_count // 5], (x, y))
        anim_count += 1
    elif right:
        DISPLAYSURF.blit(walkRight[anim_count // 5], (x, y))
        anim_count += 1
    else:
        DISPLAYSURF.blit(playerStand, (x, y))

    for bullet in bullets:
        bullet.draw(DISPLAYSURF)

    for platform in platforms:
        platform.draw(DISPLAYSURF)

    pygame.display.update()


# Movement keys processing logic
def process_movement_keys_pressed():
    global x, left, right, lastMove, anim_count
    if keys[pygame.K_LEFT] and x > minX:
        x -= speed
        left = True
        right = False
        lastMove = "left"
    elif keys[pygame.K_RIGHT] and x < maxX:
        x += speed
        left = False
        right = True
        lastMove = "right"
    else:
        left = False
        right = False
        anim_count = 0


# Jump key processing logic
def process_jump_keys_pressed():
    global is_jump, jump_count, y

    if not is_jump:
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_count >= -8:
            if jump_count < 0:
                y += int((jump_count ** 2) / 2)
            else:
                y -= int((jump_count ** 2) / 2)
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 8


# Attack key processing logic
def process_attack_keys_pressed():
    global lastMove, facing, bullets
    if keys[pygame.K_f]:
        if lastMove == "right":
            facing = 1
        else:
            facing = -1

        if len(bullets) < 1:
            bullets.append(Bullet(x + width // 2, y + height // 2, 5, (150, 50, 0), facing))


# !!!!!!!!!!!!!!!!!!!!!!
#  Game main loop start
# !!!!!!!!!!!!!!!!!!!!!!
while run:
    clock.tick(30)
    # Definition of game FPS
    pygame.time.delay(FPS)

    bgX -= 1.4  # Move both background images back
    bgX2 -= 1.4

    if bgX < bg.get_width() * -1:  # If our bg is at the -width then reset its position
        bgX = bg.get_width()

    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    # Handling exit from the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Handle each bullet
    Bullet.handle_bullet(bullets)

    Platform.handle_platform(platforms)

    # Collect all pressed keys
    keys = pygame.key.get_pressed()
    # Process all pressed keys
    process_attack_keys_pressed()
    process_movement_keys_pressed()
    process_jump_keys_pressed()

    # Draw scene
    draw_window()
# !!!!!!!!!!!!!!!!!!!!!!
#  Game main loop end
# !!!!!!!!!!!!!!!!!!!!!!

pygame.quit()
