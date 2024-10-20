import pygame
import random

# Global constants
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH = WIDTH // BLOCK_SIZE
GRID_HEIGHT = HEIGHT // BLOCK_SIZE
FPS = 30
FALL_SPEED = 500  # Milliseconds between falls

# Colors
COLORS = [
    (0, 0, 0),  # Black (background)
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
    (0, 255, 255)   # Cyan
]

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1, 1], [0, 1, 0]],  # T shape
    [[1, 1], [1, 1]],  # O shape
    [[1, 1, 0], [0, 1, 1]],  # Z shape
    [[0, 1, 1], [1, 1, 0]],  # S shape
    [[1, 1, 1], [1, 0, 0]],  # L shape
    [[1, 1, 1], [0, 0, 1]]   # J shape
]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH + 100, HEIGHT))  # Increase width for next piece display
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = COLORS[random.randint(1, len(COLORS) - 1)]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def get_shape(self):
        return self.shape

class Grid:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.score = 0

    def add_piece(self, piece):
        shape = piece.get_shape()
        for i, row in enumerate(shape):
            for j, value in enumerate(row):
                if value:
                    self.grid[piece.y + i][piece.x + j] = COLORS.index(piece.color)

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [0] * GRID_WIDTH)  # Insert a new empty line at the top
        self.score += len(lines_to_clear)  # Update score based on lines cleared

    def draw(self, surface):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                value = self.grid[y][x]
                if value:
                    rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(surface, COLORS[value], rect)

    def get_score(self):
        return self.score

def draw_grid(surface):
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, (200, 200, 200), rect, 1)

def draw_piece(surface, piece):
    shape = piece.get_shape()
    for i, row in enumerate(shape):
        for j, value in enumerate(row):
            if value:
                rect = pygame.Rect((piece.x + j) * BLOCK_SIZE, (piece.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(surface, piece.color, rect)

def draw_next_piece(surface, next_piece):
    shape = next_piece.get_shape()
    # Draw a rectangle for the next piece display
    pygame.draw.rect(surface, (50, 50, 50), (GRID_WIDTH * BLOCK_SIZE + 10, 10, 80, 80))  # Dark gray rectangle
    for i, row in enumerate(shape):
        for j, value in enumerate(row):
            if value:
                # Center the next piece in the rectangle
                rect = pygame.Rect((GRID_WIDTH * BLOCK_SIZE + 20 + j * BLOCK_SIZE),
                                   (20 + i * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(surface, next_piece.color, rect)

def draw_score(surface, score):
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    surface.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 20, 100))  # Draw score below next piece

def is_valid_position(piece, grid):
    shape = piece.get_shape()
    for i, row in enumerate(shape):
        for j, value in enumerate(row):
            if value:
                x = piece.x + j
                y = piece.y + i
                if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT or grid.grid[y][x]:
                    return False
    return True

def main():
    running = True
    grid = Grid()
    current_piece = Piece()
    next_piece = Piece()  # Store the next piece
    last_fall_time = pygame.time.get_ticks()  # Initialize last fall time

    while running:
        screen.fill((0, 0, 0))
        draw_grid(screen)
        grid.draw(screen)
        draw_piece(screen, current_piece)
        draw_next_piece(screen, next_piece)  # Draw the next piece
        draw_score(screen, grid.get_score())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not is_valid_position(current_piece, grid):
                        current_piece.x += 1  # Revert move if not valid
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not is_valid_position(current_piece, grid):
                        current_piece.x -= 1  # Revert move if not valid
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not is_valid_position(current_piece, grid):
                        current_piece.y -= 1  # Revert move if not valid
                elif event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not is_valid_position(current_piece, grid):
                        current_piece.rotate()  # Revert rotation if not valid
                elif event.key == pygame.K_SPACE:
                    # Make the piece fall all the way down
                    while is_valid_position(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1  # Set it to the last valid position

        # Check if it's time for the piece to fall
        if pygame.time.get_ticks() - last_fall_time > FALL_SPEED:
            current_piece.y += 1
            if not is_valid_position(current_piece, grid):
                current_piece.y -= 1
                grid.add_piece(current_piece)
                grid.clear_lines()
                current_piece = next_piece  # Update current piece to next piece
                next_piece = Piece()  # Generate a new next piece
                # Check for game over condition
                if any(grid.grid[0]):
                    print("Game Over!")
                    running = False
            last_fall_time = pygame.time.get_ticks()  # Reset the fall timer

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
