import pygame
from random import randrange as rnd
WIDTH, HEIGTH = 1200, 700
fps = 60
score = 0
#paddle settings
paddle_w = 250
paddle_h = 25
paddle_speed = 15 
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGTH - paddle_h-10,paddle_w, paddle_h)
#ball settings 
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball= pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGTH // 2, ball_rect, ball_rect)
dx, dy = 1, -1
#block settings
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50)for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256))  for i in range(10) for j in range(4)]
pygame.init() 
font_score = pygame.font.SysFont('Arial', 40, bold=True)
font_end = pygame.font.SysFont('Arial', 65, bold=True)
font_win = pygame.font.SysFont('Arial', 65, bold=True)
sc = pygame.display.set_mode((WIDTH, HEIGTH))
clock = pygame.time.Clock()
#background
img = pygame.image.load('1.jpg').convert()
def detect_colision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = rect.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top
    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.blit(img, (0, 0))
    #drawing world
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('black'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)
    #show score
    render_score = font_score.render(f'SCORE :{score}', 1, pygame.Color('white'))
    sc.blit(render_score, (500, 450))
    #ball movement
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    #left, right
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    #top
    if ball.centery < ball_radius:
        dy = -dy
    #paddle
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_colision(dx, dy, ball, paddle)
    #collision blocks
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_colision(dx, dy, ball, hit_rect)
        #special effect
        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hit_color, hit_rect)
        fps += 2
        score += 1
    #control
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed
    #win, lose
    if ball.bottom > HEIGTH:
        render_end = font_end.render('GG VP:((((((', 1, pygame.Color('red'))

        sc.blit(render_end, (400, 300))
    elif not len(block_list):
        render_win = font_win.render('izi katka', 1, pygame.Color('red')) 

        sc.blit(render_win, (400, 300))
    #update screen
    pygame.display.flip()
    clock.tick(fps)