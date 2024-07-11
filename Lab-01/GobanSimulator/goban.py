import pygame
import sys
import copy

class Goban:
    def __init__(self, size=19):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.current_player = 'B'  # Black starts
        self.move_history = []
        self.redo_stack = []
        self.ko_point = None

    def opponent(self):
        return 'W' if self.current_player == 'B' else 'B'

    def place_stone(self, row, col):
        if not self.is_valid_move(row, col):
            return False

        self.move_history.append((row, col, self.current_player, copy.deepcopy(self.board))) # the current player at current board place the stone at (row, col)

        self.board[row][col] = self.current_player
        captured = self.remove_captured_stones(row, col)

        if not captured and not self.has_liberties(row, col):
            self.board[row][col] = ' '  # Undo the move if it's a suicide
            self.move_history.pop() # history records nothing
            return False

        self.redo_stack.clear()  # Clear redo stack on a new move
        self.current_player = self.opponent()
        self.update_ko_point(row, col, captured)
        return True

    def is_valid_move(self, row, col):
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        if self.board[row][col] != ' ':
            return False
        if (row, col) == self.ko_point:
            return False
        return True

    def remove_captured_stones(self, row, col):
        captured = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            if 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == self.opponent():
                group = self.get_group(r, c)
                if not self.has_liberties_group(group):
                    captured.extend(group)

        for r, c in captured:
            self.board[r][c] = ' '

        return captured

    def get_group(self, row, col):
        color = self.board[row][col]
        group = set([(row, col)])
        frontier = [(row, col)]

        while frontier:
            r, c = frontier.pop()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == color and (nr, nc) not in group:
                    group.add((nr, nc))
                    frontier.append((nr, nc))

        return group

    def has_liberties_group(self, group):
        for row, col in group:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                r, c = row + dr, col + dc
                if 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == ' ':
                    return True
        return False

    def has_liberties(self, row, col):
        return self.has_liberties_group(self.get_group(row, col))

    def update_ko_point(self, row, col, captured):
        if len(captured) == 1 and len(self.get_group(row, col)) == 1:
            self.ko_point = captured[0]
        else:
            self.ko_point = None

    def undo_move(self):
        if self.move_history:
            last_move = self.move_history.pop()
            row, col, player, board_state = last_move
            self.redo_stack.append((row, col, self.current_player, copy.deepcopy(self.board)))
            self.board = board_state
            self.current_player = player
            self.ko_point = None
            return True
        return False

    def redo_move(self):
        if self.redo_stack:
            move = self.redo_stack.pop()
            row, col, player, board_state = move
            self.move_history.append((row, col, self.current_player, copy.deepcopy(self.board)))
            self.board = board_state
            self.current_player = player
            return True
        return False

    def new_game(self):
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = 'B'
        self.move_history.clear()
        self.redo_stack.clear()
        self.ko_point = None


class GobanGUI:
    def __init__(self, goban):
        self.goban = goban
        self.cell_size = 30
        self.margin = 20
        self.board_size = (goban.size - 1) * self.cell_size + 2 * self.margin
        self.window_width = self.board_size + 100
        self.window_height = self.board_size + 60

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Goban")

        self.board_color = (220, 179, 92)
        self.line_color = (0, 0, 0)
        self.black_stone_color = (0, 0, 0)
        self.white_stone_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.button_color = (100, 100, 255)
        self.button_hover_color = (150, 150, 255)

        self.font = pygame.font.Font(None, 24)

    def draw_board(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, self.board_color, (0, 0, self.board_size, self.board_size))
        for i in range(self.goban.size):
            pygame.draw.line(self.screen, self.line_color,
                             (self.margin + i * self.cell_size, self.margin),
                             (self.margin + i * self.cell_size, self.board_size - self.margin))
            pygame.draw.line(self.screen, self.line_color,
                             (self.margin, self.margin + i * self.cell_size),
                             (self.board_size - self.margin, self.margin + i * self.cell_size))

        self.draw_star_points()

    def draw_star_points(self):
        star_points = [(3, 3), (3, 9), (3, 15), (9, 3), (9, 9), (9, 15), (15, 3), (15, 9), (15, 15)]
        for row, col in star_points:
            pygame.draw.circle(self.screen, self.line_color,
                               (self.margin + col * self.cell_size, self.margin + row * self.cell_size),
                               4)

    def draw_stones(self):
        for row in range(self.goban.size):
            for col in range(self.goban.size):
                if self.goban.board[row][col] != ' ':
                    color = self.black_stone_color if self.goban.board[row][col] == 'B' else self.white_stone_color
                    pos = (self.margin + col * self.cell_size, self.margin + row * self.cell_size)
                    pygame.draw.circle(self.screen, color, pos, self.cell_size // 2 - 2)

    def draw_ui(self):
        current_player_color = self.black_stone_color if self.goban.current_player == 'B' else self.white_stone_color
        pos = (self.board_size // 2, self.window_height - 20)
        pygame.draw.circle(self.screen, current_player_color, pos, 10)
        if current_player_color == self.white_stone_color:
            pygame.draw.circle(self.screen, self.black_stone_color, pos, 10, 1)  # Outline

        undo_button = pygame.Rect(self.board_size + 10, 10, 80, 30)
        new_game_button = pygame.Rect(self.board_size + 10, 50, 80, 30)
        redo_button = pygame.Rect(self.board_size + 10, 90, 80, 30)

        mouse_pos = pygame.mouse.get_pos()
        button_color_undo = self.button_hover_color if undo_button.collidepoint(mouse_pos) else self.button_color
        button_color_new_game = self.button_hover_color if new_game_button.collidepoint(mouse_pos) else self.button_color
        button_color_redo = self.button_hover_color if redo_button.collidepoint(mouse_pos) else self.button_color

        pygame.draw.rect(self.screen, button_color_undo, undo_button)
        pygame.draw.rect(self.screen, self.text_color, undo_button, 2)
        text_surface = self.font.render("Undo", True, self.text_color)
        text_rect = text_surface.get_rect(center=undo_button.center)
        self.screen.blit(text_surface, text_rect)

        pygame.draw.rect(self.screen, button_color_new_game, new_game_button)
        pygame.draw.rect(self.screen, self.text_color, new_game_button, 2)
        text_surface = self.font.render("New", True, self.text_color)
        text_rect = text_surface.get_rect(center=new_game_button.center)
        self.screen.blit(text_surface, text_rect)

        pygame.draw.rect(self.screen, button_color_redo, redo_button)
        pygame.draw.rect(self.screen, self.text_color, redo_button, 2)
        text_surface = self.font.render("Redo", True, self.text_color)
        text_rect = text_surface.get_rect(center=redo_button.center)
        self.screen.blit(text_surface, text_rect)

        return undo_button, new_game_button, redo_button

    def get_board_pos(self, mouse_pos):
        x, y = mouse_pos
        row = round((y - self.margin) / self.cell_size)
        col = round((x - self.margin) / self.cell_size)
        return row, col

    def run_human_vs_human(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        undo_button, new_game_button, redo_button = self.draw_ui()
                        if undo_button.collidepoint(event.pos):
                            self.goban.undo_move()
                        elif new_game_button.collidepoint(event.pos):
                            self.goban.new_game()
                        elif redo_button.collidepoint(event.pos):
                            self.goban.redo_move()
                        else:
                            row, col = self.get_board_pos(event.pos)
                            self.goban.place_stone(row, col)

            self.draw_board()
            self.draw_stones()
            self.draw_ui()
            pygame.display.flip()
            clock.tick(60)

def main():
    goban = Goban()
    gui = GobanGUI(goban)
    gui.run_human_vs_human()

if __name__ == "__main__":
    main()
