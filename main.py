import pygame
import os
pygame.font.init() # Pygame library for fonts
pygame.mixer.init() # Pygame library for sound

# Set the game window
WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle Starships")

# Load starship images
YELLOW_STARSHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
RED_STARSHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))

STARSHIP_WIDTH, STARSHIP_HEIGHT = 55, 40

# User events for collisions. Each event has a unique event ID
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Resize the starship images and there facing directions
YELLOW_STARSHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_STARSHIP_IMAGE, (STARSHIP_WIDTH, STARSHIP_HEIGHT)), 90)
RED_STARSHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_STARSHIP_IMAGE, (STARSHIP_WIDTH, STARSHIP_HEIGHT)), 270)

# Load background image
SPACE_BACKGROUND = pygame.transform.scale(
    pygame.image.load(os.path.join(
        'Assets', 'space.png')), (WIDTH, HEIGHT))

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Sounds
LASER_HIT_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'Grenade+1.mp3'))
LASER_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'Gun+Silencer.mp3'))

# Frames per second 
FPS = 60

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Battlefield border
MIDDLE_BORDER = pygame.Rect(
    WIDTH // 2 - 5, 0, 10, HEIGHT)

# Starship Movement velocity
VELOCITY = 5

# Speed of players bullet
LASER_SPEED = 7

# Number of bullets player has
NUM_OF_LASERS = 5

# Draw the background, starships, border and lasers onto the screen. 
def draw_window(red, yellow, red_lasers, yellow_lasers, red_health, yellow_health):
    WINDOW.blit(SPACE_BACKGROUND, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, MIDDLE_BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))

    WINDOW.blit(YELLOW_STARSHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_STARSHIP, (red.x, red.y))

    # Loop through the lasers list and draw onto the screen
    for laser in red_lasers:
        pygame.draw.rect(WINDOW, RED, laser)

    for laser in yellow_lasers:
        pygame.draw.rect(WINDOW, YELLOW, laser)

    pygame.display.update()

def yellow_starship_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0: # Left movement
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < MIDDLE_BORDER.x: # Right movement
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 15: # Down movement
        yellow.y += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0: # Up movement
        yellow.y -= VELOCITY

def red_starship_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > MIDDLE_BORDER.x + MIDDLE_BORDER.width: # Left movement
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH: # Right movement
        red.x += VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT - 15: # Down movement
        red.y += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0: # Up movement
        red.y -= VELOCITY

def handle_lasers(yellow_lasers, red_lasers, yellow, red):
    for laser in yellow_lasers:
        laser.x += LASER_SPEED
        if red.colliderect(laser):
            pygame.event.post(pygame.event.Event(RED_HIT)) # Make a new event to show red player was hit
            yellow_lasers.remove(laser)
        elif laser.x > WIDTH: # Check if laser moves off the screen. If it does, remove it.
            yellow_lasers.remove(laser)

    for laser in red_lasers:
        laser.x -= LASER_SPEED
        if yellow.colliderect(laser):
            pygame.event.post(pygame.event.Event(YELLOW_HIT)) # Make a new event to show yellow player was hit
            red_lasers.remove(laser)
        elif laser.x < 0: # Check if laser moves off the screen. If it does, remove it.
            red_lasers.remove(laser)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(draw_text, (
        WIDTH/2 - draw_text.get_width() / 2, HEIGHT 
        / 2 - draw_text.get_height())) # Show's winner messasge in the middle of the screen

    pygame.display.update()
    pygame.time.delay(5000)

def main():
    yellow = pygame.Rect(100, 300, STARSHIP_WIDTH, STARSHIP_HEIGHT)
    red = pygame.Rect(700, 300, STARSHIP_WIDTH, STARSHIP_HEIGHT)

    # Player ammo
    red_lasers = []
    yellow_lasers = []

    # Starship health
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    start = True 
    while start:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                # Fire bullets from yellow 
                if event.key == pygame.K_LCTRL and len(yellow_lasers) < NUM_OF_LASERS:
                    laser = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_lasers.append(laser)
                    LASER_FIRE_SOUND.play()
                # Fire bullets from red
                if event.key == pygame.K_RCTRL and len(red_lasers) < NUM_OF_LASERS:
                    laser = pygame.Rect(
                        red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_lasers.append(laser)
                    LASER_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health = red_health - 1
                LASER_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health = yellow_health - 1
                LASER_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
        
        keys_pressed = pygame.key.get_pressed() 
        yellow_starship_movement(keys_pressed, yellow)
        red_starship_movement(keys_pressed, red)

        handle_lasers(yellow_lasers, red_lasers, yellow, red)

        draw_window(red, yellow, red_lasers, yellow_lasers, 
                    red_health, yellow_health)

    main()

if __name__ == "__main__":
    main()