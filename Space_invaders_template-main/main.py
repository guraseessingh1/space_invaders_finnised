
import pygame

pygame.font.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("space invaders")
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
border = pygame.Rect(WIDTH//2-5,0,10,HEIGHT)

HEALTH_FONT =  pygame.font.SysFont("ariel",45)
WINNER_FONT =  pygame.font.SysFont("comicsans",100)

FPS = 60
VELOCITY = 1

BULLET_VELOCITY = 5
MAX_BULLET = 3
SHIP_WIDTH = 55
SHIP_HEIGHT = 40

y_ship_image = pygame.image.load("assets/spaceship_yellow.png")
y_ship_image = pygame.transform.scale(y_ship_image,(SHIP_WIDTH,SHIP_HEIGHT))
yellow_ship = pygame.transform.rotate(y_ship_image,90)

r_ship_image = pygame.image.load("assets/spaceship_red.png")
r_ship_image = pygame.transform.scale(r_ship_image,(SHIP_WIDTH,SHIP_HEIGHT))
red_ship = pygame.transform.rotate(r_ship_image,270)

space_image = pygame.image.load("assets/space.png")
space = pygame.transform.scale(space_image,(WIDTH,HEIGHT))

yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2


def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    screen.blit(space,(0,0))
    pygame.draw.rect(screen,BLACK,border)
    red_health_text = HEALTH_FONT.render("health:"+str(red_health),1,WHITE)
    yellow_health_text = HEALTH_FONT.render("Health:"+str(yellow_health),1,WHITE)
    screen.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
    screen.blit(yellow_health_text,(10,10))
    screen.blit(red_ship,(red.x,red.y))
    screen.blit(yellow_ship,(yellow.x,yellow.y))

    for bullet in red_bullets:
        pygame.draw.rect(screen,RED,bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(screen,YELLOW,bullet)
    pygame.display.update()
# yellow awsd

def yellow_movement(keys_pressed,yellow_ship):
    if keys_pressed[pygame.K_a] and yellow_ship.x - VELOCITY > 0:
        yellow_ship.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow_ship.x + VELOCITY + yellow_ship.width < border.x :
        yellow_ship.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow_ship.y - VELOCITY > 0:
        yellow_ship.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow_ship.y + VELOCITY + yellow_ship.height < HEIGHT-15:
        yellow_ship.y += VELOCITY
    
# red  up,down,left,right keys

def red_movement(keys_pressed,red_ship):
    if keys_pressed[pygame.K_LEFT] and red_ship.x - VELOCITY > border.x + border.width:
        red_ship.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red_ship.x + VELOCITY + red_ship.width < WIDTH:
        red_ship.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red_ship.y - VELOCITY > 0:
        red_ship.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red_ship.y + VELOCITY + red_ship.height < HEIGHT-15:
        red_ship.y += VELOCITY

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH :
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x < 0 :
            red_bullets.remove(bullet)

def draw_winner(winner_text):
    winner_text = WINNER_FONT.render(winner_text,1,WHITE)
    screen.blit(winner_text,(WIDTH//2 - winner_text.get_width()//2,HEIGHT//2 - winner_text.get_height()//2 ))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    #creating a hit box for both of the ship
    red = pygame.Rect(700,300,SHIP_WIDTH,SHIP_HEIGHT)
    yellow = pygame.Rect(100,300,SHIP_WIDTH,SHIP_HEIGHT)

    red_bullet = []
    yellow_bullet = []

    red_health = 10
    yellow_health = 10

    is_running = True

    while is_running :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and  len(yellow_bullet ) < MAX_BULLET:
                    bullet = pygame.Rect(yellow.x + SHIP_WIDTH,yellow.y + SHIP_HEIGHT//2,10,5)
                    yellow_bullet.append(bullet)                   
                if event.key == pygame.K_RCTRL and len(red_bullet) < MAX_BULLET:
                    bullet = pygame.Rect(red.x,red.y + SHIP_HEIGHT//2,10,5)
                    red_bullet.append(bullet)
            
            if event.type == red_hit:
                red_health -=  1
            if event.type == yellow_hit:
             yellow_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "yellow wins"
        if yellow_health <= 0:
            winner_text = "red_wins"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()

        yellow_movement(keys_pressed,yellow)
        red_movement(keys_pressed,red)
        handle_bullets(yellow_bullet,red_bullet,yellow,red)
        draw_window(red,yellow,red_bullet,yellow_bullet,red_health,yellow_health)

main()







