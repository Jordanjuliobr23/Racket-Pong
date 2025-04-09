import pygame
import random
import time

# Inicializa o Pygame
pygame.init()

# Dimensões da tela
screen_w, screen_h = 1240, 600
screen = pygame.display.set_mode((screen_w, screen_h))

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fonte
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)

# Função para carregar e redimensionar imagens
def load_and_scale_image(path, size):
    return pygame.transform.scale(pygame.image.load(path), size)

# Caminho para as imagens
image_path = 'C:\\Users\\JORDAN\\Downloads\\Racket pong\\Imagens\\'
ball_image = load_and_scale_image(image_path + 'ball.png', (20, 25))
racket_image = load_and_scale_image(image_path + 'racket.png', (40, 50))
red_shield_image = load_and_scale_image(image_path + 'red_shield.png', (40, 80))
blue_shield_image = load_and_scale_image(image_path + 'blue_shield.png', (40, 80))
game_over_image = load_and_scale_image(image_path + 'game_over.png', (300, 150))
you_win_image = load_and_scale_image(image_path + 'you_win.png', (300, 150))
lifes_image = load_and_scale_image(image_path + 'lifes.png', (10, 10))

# Tela inicial
def show_start_screen():
    screen.fill(BLACK)
    title_text = font.render("RACKET PONG", True, WHITE)
    prompt_text = small_font.render("Por favor digite seu nome:", True, WHITE)
    screen.blit(title_text, (screen_w // 2 - title_text.get_width() // 2, screen_h // 2 - title_text.get_height()))
    screen.blit(prompt_text, (screen_w // 2 - prompt_text.get_width() // 2, screen_h // 2 + title_text.get_height()))
    pygame.display.flip()

    name = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                else:
                    name += event.unicode
        screen.fill(BLACK)
        screen.blit(title_text, (screen_w // 2 - title_text.get_width() // 2, screen_h // 2 - title_text.get_height()))
        screen.blit(prompt_text, (screen_w // 2 - prompt_text.get_width() // 2, screen_h // 2 + title_text.get_height()))
        name_text = font.render(name, True, WHITE)
        screen.blit(name_text, (screen_w // 2 - name_text.get_width() // 2, screen_h // 2 + title_text.get_height() + 50))
        pygame.display.flip()

player_name = show_start_screen()
cpu_name = "ENEMY"

ball = pygame.Rect(screen_w / 2 - 7.5, screen_h / 2 - 7.5, 15, 15)
player = pygame.Rect(screen_w - 50, screen_h / 2 - 20, 20, 40)
opponent = pygame.Rect(10, screen_h / 2 - 20, 20, 40)


def generate_player_shield_position():
    x = random.randint(screen_w // 2 + 50, screen_w - 140)
    y = random.randint(100, screen_h - 180)
    return pygame.Rect(x, y, 40, 80)

def generate_opponent_shield_position():
    x = random.randint(100, screen_w // 2 - 90)
    y = random.randint(100, screen_h - 180)
    return pygame.Rect(x, y, 40, 80)


player_shields = [generate_player_shield_position() for _ in range(2)]
opponent_shields = [generate_opponent_shield_position() for _ in range(2)]

shield_speed = 3
shield_direction = 1


ball_speed_x, ball_speed_y = 3, 3
paddle_speed = 10
cpu_paddle_speed = 6  

player_lives, opponent_lives = 10, 10


start_time = time.time()
game_duration = 180


rebate_line = pygame.Rect(0, 100, screen_w, 10)
bottom_line = pygame.Rect(0, screen_h - 10, screen_w, 10)

game_active = True

def ball_movement():
    global ball_speed_x, ball_speed_y, player_lives, opponent_lives

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0:
        ball_speed_y *= -1

 
    if ball.bottom >= screen_h - 10:
        ball_speed_y *= -1
        ball.bottom = screen_h - 10

 
    if ball.left <= 0:
        opponent_lives -= 1
        ball_restart()
    
   
    elif ball.right >= screen_w:
        player_lives -= 1
        ball_restart()

   
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1
        if ball.colliderect(player):
            ball.right = player.left
        else:
            ball.left = opponent.right
        
        ball_speed_x *= 1.5
        ball_speed_y *= 1.5


    for shield in player_shields + opponent_shields:
        if ball.colliderect(shield):
            if abs(ball.bottom - shield.top) < 10 and ball_speed_y > 0:
                ball_speed_y *= -1
                ball.bottom = shield.top
            elif abs(ball.top - shield.bottom) < 10 and ball_speed_y < 0:
                ball_speed_y *= -1
                ball.top = shield.bottom
            else:
                ball_speed_x *= -1
                if shield in player_shields:
                    ball.right = shield.left
                else:
                    ball.left = shield.right

 
    if ball.colliderect(rebate_line):
        ball_speed_y *= -1

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_w / 2, screen_h / 2)
    ball_speed_x, ball_speed_y = 3, 3

def player_movement():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.top > 100:
        player.y -= paddle_speed
    if keys[pygame.K_DOWN] and player.bottom < screen_h - 10:
        player.y += paddle_speed

def opponent_movement():
    global opponent

    if random.random() < 0.1:  
        move_direction = random.choice([-1, 0, 1])
    else:
        if ball.centery < opponent.centery:
            move_direction = -1
        elif ball.centery > opponent.centery:
            move_direction = 1
        else:
            move_direction = 0

    if move_direction == -1 and opponent.top > 100:
        opponent.y -= cpu_paddle_speed
    elif move_direction == 1 and opponent.bottom < screen_h - 10:
        opponent.y += cpu_paddle_speed

def shield_movement():
    global player_shields, opponent_shields, shield_speed

   
    for shield in player_shields:
        shield.y += shield_speed
        if shield.top <= 100:  
            shield.y = 100
            shield_speed *= -1
        elif shield.bottom >= screen_h - 100:  
            shield.y = screen_h - 100 - shield.height
            shield_speed *= -1

   
    for shield in opponent_shields:
        shield.y += shield_speed
        if shield.top <= 100:  
            shield.y = 100
            shield_speed *= -1
        elif shield.bottom >= screen_h - 100:  
            shield.y = screen_h - 100 - shield.height
            shield_speed *= -1

def draw_lives():
    for i in range(player_lives):
        screen.blit(lifes_image, (screen_w - 180 + (i % 5) * 20, 60 + (i // 5) * 20))
    for i in range(opponent_lives):
        screen.blit(lifes_image, (50 + (i % 5) * 20, 60 + (i // 5) * 20))

    screen.blit(small_font.render(player_name, True, WHITE), (screen_w - 180, 30))
    screen.blit(small_font.render(cpu_name, True, WHITE), (20, 30))

def draw_timer():
    elapsed_time = time.time() - start_time
    remaining_time = max(0, game_duration - elapsed_time)
    timer_text = small_font.render(f'Tempo Restante: {int(remaining_time)}s', True, WHITE)
    screen.blit(timer_text, (screen_w // 2 - timer_text.get_width() // 2, 30))

def draw_elements():
    screen.fill(BLACK)
    screen.blit(ball_image, ball.topleft)
    screen.blit(racket_image, player.topleft)
    screen.blit(racket_image, opponent.topleft)
    
  
    for shield in player_shields:
        screen.blit(blue_shield_image, shield.topleft)
        
   
    for shield in opponent_shields:
        screen.blit(red_shield_image, shield.topleft)

    
    pygame.draw.rect(screen, WHITE, rebate_line)
    pygame.draw.rect(screen, WHITE, (screen_w // 2 - 5, 100, 10, screen_h - 200))
    pygame.draw.rect(screen, WHITE, (screen_w // 2 - 5, 100, 10, screen_h - 100))
    pygame.draw.rect(screen, WHITE, bottom_line)
    
    draw_lives()
    draw_timer()
    
    pygame.display.flip()

def game_over(is_player_winner=None):
    screen.fill(BLACK)
    if is_player_winner is None:
        screen.blit(game_over_image, (screen_w // 2 - game_over_image.get_width() // 2, screen_h // 2 - game_over_image.get_height() // 2))
    elif is_player_winner:
        screen.blit(you_win_image, (screen_w // 2 - you_win_image.get_width() // 2, screen_h // 2 - you_win_image.get_height() // 2))
    else:
        screen.blit(game_over_image, (screen_w // 2 - game_over_image.get_width() // 2, screen_h // 2 - game_over_image.get_height() // 2))
    
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    quit()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if game_active:
        player_movement()
        opponent_movement()
        ball_movement()
        shield_movement()

      
        if player_lives <= 0 or opponent_lives <= 0 or (time.time() - start_time >= game_duration):
            game_active = False
            if time.time() - start_time >= game_duration:
                game_over()  
            elif player_lives > 0:
                game_over(is_player_winner=True)  
            else:
                game_over(is_player_winner=False)  

    draw_elements()  

    pygame.display.flip()
    pygame.time.Clock().tick(60)
