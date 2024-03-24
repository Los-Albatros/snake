import pygame
import random
import sys
import asyncio

from pygame.locals import JOYHATMOTION

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CELL_SIZE = 20
SNAKE_SPEED = 10
SNAKE_INIT_SIZE = 5


def quit_game():
    pygame.quit()
    sys.exit()


class Snake:
    def __init__(self):
        self.length = SNAKE_INIT_SIZE
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0], point[1]) == (-self.direction[0], -self.direction[1]):
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * CELL_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * CELL_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = SNAKE_INIT_SIZE
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
                elif event.key == pygame.K_ESCAPE:
                    main_menu()
            elif event.type == JOYHATMOTION:
                if event.value == LEFT:  # left
                    self.turn(LEFT)
                elif event.value == RIGHT:  # right
                    self.turn(RIGHT)
                elif event.value == (0, 1):  # up
                    self.turn(UP)
                elif event.value == (0, -1):  # down
                    self.turn(DOWN)


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font_small = pygame.font.Font(None, 36)


async def game():
    pygame.display.set_caption('Snake Game')

    # Initialisation du jeu
    snake = Snake()
    food = Food(snake)

    # Boucle de jeu
    while True:
        snake.handle_keys()

        snake.move()

        if snake.get_head_position() == food.position:
            snake.length += 1
            while snake.get_head_position() == food.position:
                food.randomize_position()

        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        pygame.display.update()
        await asyncio.sleep(0)
        pygame.time.Clock().tick(SNAKE_SPEED)


class Food:
    def __init__(self, snake):
        self.position = (0, 0)
        self.color = WHITE
        self.randomize_position()
        while snake.get_head_position() == self.position:
            self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE)) * CELL_SIZE,
                         random.randint(0, (SCREEN_HEIGHT // CELL_SIZE)) * CELL_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, BLACK, r, 1)


async def main_menu():
    clock = pygame.time.Clock()
    buttons = []
    button_width = 200
    button_height = 50
    button_left = SCREEN_WIDTH // 2 - button_width // 2
    button_top = 200
    button_play = pygame.Rect(button_left, button_top, button_width, button_height)
    button_exit = pygame.Rect(button_left, button_top + 200, button_width, button_height)
    buttons.append((button_play, (0, 0, 155)))
    buttons.append((button_exit, (155, 0, 0)))
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    while True:
        screen.fill(BLACK)
        text_play = font_small.render("Play", True, (255, 255, 255))
        text_exit = font_small.render("Exit", True, (255, 255, 255))
        mx, my = pygame.mouse.get_pos()

        for button in buttons:
            pygame.draw.rect(screen, button[1], button[0])

        screen.blit(text_play,
                    text_play.get_rect(center=(button_left + button_width // 2, button_top + button_height // 2)))

        screen.blit(text_exit,
                    text_exit.get_rect(center=(button_left + button_width // 2, button_top + 200 + button_height // 2)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.collidepoint(mx, my):
                    await game()
                if button_exit.collidepoint(mx, my):
                    quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()
                if event.key == pygame.K_g:
                    await game()
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main_menu())
