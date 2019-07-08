import pygame

pygame.init()
win = pygame.display.set_mode((500, 500))
x = 50
y = 250
radius = 40
height = 60
speed = 5
run = True
minX = 40
maxX = 460
minY = 40
maxY = 460
is_jump = False
jump_count = 10

pygame.display.set_caption("Base frame")

while run:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > minX:
        x -= speed
    if keys[pygame.K_RIGHT] and x < maxX:
        x += speed
    # if keys[pygame.K_UP] and y > minY:
    #     y -= speed
    # if keys[pygame.K_DOWN] and y < maxY:
    #     y += speed
    if not is_jump:
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_count >= -10:
            if jump_count < 0:
                y += int((jump_count ** 2) / 2)
            else:
                y -= int((jump_count ** 2) / 2)
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 10

    win.fill((0, 0, 0))
    pygame.draw.circle(win, (50, 150, 0), (x, y), radius)
    pygame.display.update()

pygame.quit()
