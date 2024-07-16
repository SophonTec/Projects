import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Piano EDM')

# Note settings
NOTE_WIDTH = 50
NOTE_HEIGHT = 20
NOTE_SPEED = 5

# Scoring zone
SCORING_ZONE_Y = SCREEN_HEIGHT - 100

# Font
font = pygame.font.Font(None, 36)

# Note class
class Note:
    def __init__(self, x, y, length=1):
        self.rect = pygame.Rect(x, y, NOTE_WIDTH, NOTE_HEIGHT * length)
        self.length = length

    def update(self):
        self.rect.y += NOTE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)

# Generate random notes
def generate_note():
    x = random.randint(0, SCREEN_WIDTH - NOTE_WIDTH)
    length = random.choice([1, 2, 3])  # Note lengths
    return Note(x, -NOTE_HEIGHT * length, length)

# Main game loop
def game_loop():
    clock = pygame.time.Clock()
    notes = [generate_note() for _ in range(10)]
    score = 0
    running = True
    held_note = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for note in notes:
                        if scoring_zone_y <= note.rect.y + note.rect.height <= scoring_zone_y + NOTE_HEIGHT:
                            score += 10 * note.length
                            held_note = note
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    held_note = None

        screen.fill(BLACK)

        for note in notes:
            note.update()
            note.draw(screen)
            if note.rect.y > SCREEN_HEIGHT:
                notes.remove(note)
                notes.append(generate_note())

        # Handle held notes
        if held_note:
            held_note.update()
            if held_note.rect.y > SCREEN_HEIGHT:
                held_note = None

        # Draw scoring zone
        pygame.draw.rect(screen, GREEN, (0, SCORING_ZONE_Y, SCREEN_WIDTH, NOTE_HEIGHT), 2)

        # Display score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    game_loop()
