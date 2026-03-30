import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 400
ROWS, COLS = 4, 4
CARD_SIZE = WIDTH // COLS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 48)

# Create pairs
numbers = list(range(1, 9)) * 2
random.shuffle(numbers)

# Game state
revealed = [False] * 16
first_card = None
second_card = None
lock = False

def draw_board():
    screen.fill(WHITE)
    for i in range(ROWS * COLS):
        x = (i % COLS) * CARD_SIZE
        y = (i // COLS) * CARD_SIZE

        if revealed[i]:
            pygame.draw.rect(screen, GREEN, (x, y, CARD_SIZE, CARD_SIZE))
            text = font.render(str(numbers[i]), True, BLACK)
            text_rect = text.get_rect(center=(x + CARD_SIZE//2, y + CARD_SIZE//2))
            screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_SIZE, CARD_SIZE))

        pygame.draw.rect(screen, BLACK, (x, y, CARD_SIZE, CARD_SIZE), 2)

def get_card_index(pos):
    x, y = pos
    col = x // CARD_SIZE
    row = y // CARD_SIZE
    return row * COLS + col

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    draw_board()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not lock:
            idx = get_card_index(pygame.mouse.get_pos())

            if not revealed[idx]:
                revealed[idx] = True

                if first_card is None:
                    first_card = idx
                elif second_card is None:
                    second_card = idx
                    lock = True

    if first_card is not None and second_card is not None:
        pygame.time.delay(500)

        if numbers[first_card] != numbers[second_card]:
            revealed[first_card] = False
            revealed[second_card] = False

        first_card = None
        second_card = None
        lock = False

    # Check win condition
    if all(revealed):
        pygame.time.delay(1000)
        random.shuffle(numbers)
        revealed = [False] * 16

    clock.tick(30)
