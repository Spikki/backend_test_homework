from random import choice
import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=SCREEN_CENTER, body_color=(0, 0, 255)):
        """Инициализирует объект с заданной позицией и цветом."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для отрисовки объекта."""
        pass

    def draw_rect(self, position):
        """Отрисовывает прямоугольник на экране в заданной позиции."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, представляющий яблоко, которое змейка может съесть."""

    def __init__(self, position=SCREEN_CENTER):
        """Инициализирует яблоко с заданной позицией и цветом."""
        super().__init__(position, APPLE_COLOR)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        self.draw_rect(self.position)

    def randomize_position(self, snake_positions):
        """Устанавливает случайную позицию для яблока."""
        free_positions = [
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x * GRID_SIZE, y * GRID_SIZE) not in snake_positions
        ]
        if not free_positions:
            raise SystemExit('No free positions left!')
        self.position = choice(free_positions)


class Snake(GameObject):
    """Класс, представляющий змейку, которой управляет игрок."""

    def __init__(self):
        """Инициализирует змейку."""
        super().__init__(SCREEN_CENTER, SNAKE_COLOR)
        self.positions = [self.position]
        self.direction = RIGHT
        self.length = 1

    def move(self):
        """Обновляет позицию змейки."""
        new_head = (
            (self.positions[0][0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (self.positions[0][1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        if new_head in self.positions:
            raise SystemExit('Game Over!')
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            self.draw_rect(position)

    def grow(self):
        """Увеличивает длину змейки на 1."""
        self.length += 1

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки, если это возможно."""
        if (new_direction == UP and self.direction != DOWN) or \
           (new_direction == DOWN and self.direction != UP) or \
           (new_direction == LEFT and self.direction != RIGHT) or \
           (new_direction == RIGHT and self.direction != LEFT):
            self.direction = new_direction

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    key_direction = {
        pg.K_UP: UP,
        pg.K_DOWN: DOWN,
        pg.K_LEFT: LEFT,
        pg.K_RIGHT: RIGHT
    }
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN and event.key in key_direction:
            snake.update_direction(key_direction[event.key])


def main():
    """Основная функция игры."""
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        try:
            snake.move()
        except SystemExit as e:
            break

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()
        pg.display.flip()


if __name__ == '__main__':
    main()
