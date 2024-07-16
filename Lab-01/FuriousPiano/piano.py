import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Piano Music Go")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TILE_COLOR = (0, 0, 255)
KEY_COLORS = [WHITE] * 8  # Default colors for keys
KEY_TIMERS = [0] * 8  # Timer for each key to reset color

# Load sounds
sounds = {
    0: pygame.mixer.Sound("sounds/piano-C4.wav"),
    1: pygame.mixer.Sound("sounds/piano-D4.wav"),
    2: pygame.mixer.Sound("sounds/piano-E4.wav"),
    3: pygame.mixer.Sound("sounds/piano-F4.wav"),
    4: pygame.mixer.Sound("sounds/piano-G4.wav"),
    5: pygame.mixer.Sound("sounds/piano-A4.wav"),
    6: pygame.mixer.Sound("sounds/piano-B4.wav"),
    7: pygame.mixer.Sound("sounds/piano-C5.wav")
}

# Define tile properties
num_keys = 8
tile_width = width // num_keys
tile_height = 150
tile_speed = 5

# Define key bindings and labels
key_bindings = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_SEMICOLON]
key_labels = ['A', 'S', 'D', 'F', 'J', 'K', 'L', ';']

# Generate initial tiles
tiles = []
for i in range(5):
    x = random.randint(0, num_keys - 1) * tile_width
    y = -tile_height - i * (tile_height + 20)
    tiles.append(pygame.Rect(x, y, tile_width, tile_height))

# Function to draw piano keys at the bottom
def draw_piano_keys():
    for i in range(num_keys):
        x = i * tile_width
        rect = pygame.Rect(x, height - tile_height, tile_width, tile_height)
        pygame.draw.rect(window, KEY_COLORS[i], rect)
        pygame.draw.rect(window, BLACK, rect, 2)
        font = pygame.font.SysFont(None, 40)
        label = font.render(key_labels[i], True, BLACK)
        label_rect = label.get_rect(center=(x + tile_width // 2, height - tile_height // 2))
        window.blit(label, label_rect)

# Game loop
score = 0
running = True
while running:
    window.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            keys = pygame.key.get_pressed()
            for i, key in enumerate(key_bindings):
                if event.key == key:
                    hit = False
                    for tile in tiles:
                        if tile.collidepoint(i * tile_width + tile_width // 2, height - tile_height):
                            sounds[i].play()
                            tiles.remove(tile)
                            KEY_COLORS[i] = GREEN
                            KEY_TIMERS[i] = pygame.time.get_ticks() + 200  # Reset color after 200ms
                            score += 1
                            hit = True
                            break
                    if not hit:
                        KEY_COLORS[i] = RED
                        KEY_TIMERS[i] = pygame.time.get_ticks() + 200  # Reset color after 200ms

    # Move tiles down
    for tile in tiles:
        tile.y += tile_speed

    # Check for missed tiles
    tiles = [tile for tile in tiles if tile.y <= height]

    # Generate new tiles
    while len(tiles) < 5:
        x = random.randint(0, num_keys - 1) * tile_width
        y = random.randint(-tile_height * 5, -tile_height)
        tiles.append(pygame.Rect(x, y, tile_width, tile_height))

    # Reset key colors after the timer expires
    current_time = pygame.time.get_ticks()
    for i in range(num_keys):
        if KEY_COLORS[i] in [GREEN, RED] and current_time >= KEY_TIMERS[i]:
            KEY_COLORS[i] = WHITE

    # Draw tiles
    for tile in tiles:
        pygame.draw.rect(window, TILE_COLOR, tile)
    
    # Draw piano keys
    draw_piano_keys()

    # Display score
    font = pygame.font.SysFont(None, 55)
    score_text = font.render(f"Score: {score}", True, WHITE)
    window.blit(score_text, (10, 10))

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
sys.exit()
