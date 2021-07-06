import pygame
import os

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

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Frames per second 
FPS = 60

MIDDLE_BORDER = pygame.Rect(
    WIDTH // 2 - 5, 0, 10, HEIGHT)

# Starship Movement velocity
VELOCITY = 5

# Speed of players bullet
LASER_SPEED = 7

# Number of bullets player has
NUM_OF_LASERS = 5

def draw_window(red, yellow, red_lasers, yellow_lasers):
    WINDOW.fill(WHITE)
    pygame.draw.rect(WINDOW, BLACK, MIDDLE_BORDER)
    WINDOW.blit(YELLOW_STARSHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_STARSHIP, (red.x, red.y))

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

def handle_lasers(yellow_lasers, red_lasers, yellow,red):
    for laser in yellow_lasers:
        laser.x += LASER_SPEED
        if red.colliderect(laser):
            pygame.event.post(pygame.event.Event(RED_HIT)) # Make a new event to show red player was hit
            yellow_lasers.remove(laser)

    for laser in red_lasers:
        laser.x -= LASER_SPEED
        if yellow.colliderect(laser):
            pygame.event.post(pygame.event.Event(YELLOW_HIT)) # Make a new event to show yellow player was hit
            yellow_lasers.remove(laser)

def main():
    yellow = pygame.Rect(100, 300, STARSHIP_WIDTH, STARSHIP_HEIGHT)
    red = pygame.Rect(700, 300, STARSHIP_WIDTH, STARSHIP_HEIGHT)

    # Player ammo
    red_lasers = []
    yellow_lasers = []

    clock = pygame.time.Clock()
    start = True 
    while start:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False

            if event.type == pygame.KEYDOWN:
                # Fire bullets from yellow 
                if event.key == pygame.K_LCTRL and len(yellow_lasers) < NUM_OF_LASERS:
                    laser = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_lasers.append(laser)
                # Fire bullets from red
                if event.key == pygame.K_RCTRL and len(red_lasers) < NUM_OF_LASERS:
                    laser = pygame.Rect(
                        red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_lasers.append(laser)
        
        keys_pressed = pygame.key.get_pressed() 
        yellow_starship_movement(keys_pressed, yellow)
        red_starship_movement(keys_pressed, red)

        handle_lasers(yellow_lasers, red_lasers, yellow, red)

        draw_window(red, yellow, red_lasers, yellow_lasers)

    pygame.quit()

if __name__ == "__main__":
    main()