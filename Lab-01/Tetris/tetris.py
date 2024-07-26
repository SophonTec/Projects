import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Shapes
SHAPES = [
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1, 1]],          # I
    [[1, 1], [1, 1]],        # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

# Colors for shapes
SHAPE_COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, MAGENTA, RED]

class Tetris:
    def __init__(self, screen):
        self.screen = screen
        self.grid = [[BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.current_shape = self.get_new_shape()
        self.current_shape_color = random.choice(SHAPE_COLORS)
        self.shape_x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(self.current_shape[0]) // 2
        self.shape_y = 0
        self.fall_time = 0
        self.score = 0
        self.font = pygame.font.SysFont('comicsans', 30)

    def get_new_shape(self):
        return random.choice(SHAPES)

    def draw_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                pygame.draw.rect(self.screen, self.grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(self.screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, val in enumerate(row):
                if val == 1:
                    pygame.draw.rect(self.screen, self.current_shape_color,
                                     ((self.shape_x + x) * BLOCK_SIZE, (self.shape_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                    pygame.draw.rect(self.screen, WHITE,
                                     ((self.shape_x + x) * BLOCK_SIZE, (self.shape_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def valid_space(self):
        for y, row in enumerate(self.current_shape):
            for x, val in enumerate(row):
                if val == 1:
                    if (self.shape_y + y >= len(self.grid) or
                            self.shape_x + x >= len(self.grid[0]) or
                            self.shape_x + x < 0 or
                            self.grid[self.shape_y + y][self.shape_x + x] != BLACK):
                        return False
        return True

    def lock_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, val in enumerate(row):
                if val == 1:
                    self.grid[self.shape_y + y][self.shape_x + x] = self.current_shape_color
        self.current_shape = self.get_new_shape()
        self.current_shape_color = random.choice(SHAPE_COLORS)
        self.shape_x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(self.current_shape[0]) // 2
        self.shape_y = 0
        if not self.valid_space():
            self.__init__(self.screen)

    def clear_rows(self):
        new_grid = [row for row in self.grid if BLACK in row]
        cleared_rows = len(self.grid) - len(new_grid)
        self.score += cleared_rows * 10  # Add score
        new_grid = [[BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(cleared_rows)] + new_grid
        self.grid = new_grid

    def rotate_shape(self):
        self.current_shape = [list(row) for row in zip(*self.current_shape[::-1])]
        if not self.valid_space():
            self.current_shape = [list(row) for row in zip(*self.current_shape[::-1])][::-1]

    def move_shape(self, dx):
        self.shape_x += dx
        if not self.valid_space():
            self.shape_x -= dx

    def update(self):
        self.fall_time += 1
        if self.fall_time >= 10:
            self.shape_y += 1
            if not self.valid_space():
                self.shape_y -= 1
                self.lock_shape()
                self.clear_rows()
            self.fall_time = 0

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_shape()
        self.draw_score()
        pygame.display.update()

    def draw_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = Tetris(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_shape(-1)
                if event.key == pygame.K_RIGHT:
                    game.move_shape(1)
                if event.key == pygame.K_DOWN:
                    game.shape_y += 1
                    if not game.valid_space():
                        game.shape_y -= 1
                        game.lock_shape()
                        game.clear_rows()
                if event.key == pygame.K_UP:
                    game.rotate_shape()

        game.update()
        game.draw()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
