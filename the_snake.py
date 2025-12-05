from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для всех игровых объектов"""

    def __init__(self, position=None):
        """
        Инициализирует игровой объект.

        Args:
            position (tuple): Начальная позиция объекта. Если None,
                                устанавливается в центр экрана
        """
        if position is None:
            self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        else:
            self.position = position
        self.body_color = None

    def draw(self):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс для яблока в игре."""

    def __init__(self):
        """Инициализирует яблоко со случайной позицией."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию для яблока в пределах поля."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):

    def __init__(self):
        """Инициализирует змейку в начальном состоянии"""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None  # Для хранения позиции последнего сегмента
        self.grow_next_move = False  # ФЛАГ: нужно ли вырасти на следующем ходу

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещает змейку на одну клетку в текущем направлении."""
        # Текущая позиция головы
        head_x, head_y = self.get_head_position()

        # Вычисление новой позиции головы
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT

        # Сохраняем старую позицию хвоста
        self.last = self.positions[-1] if self.positions else None

        # Добавляем новую голову в начало списка
        self.positions.insert(0, (new_x, new_y))

        # Если не нужно расти на этом ходу, удаляем хвост
        if not self.grow_next_move:
            if self.positions:
                self.positions.pop()
        else:
            # Сбрасываем флаг роста
            self.grow_next_move = False

        return (new_x, new_y)

    def check_collision(self):
        """Проверяет не столкнулась ли змейка сама с собой"""
        head_position = self.get_head_position()

        # Проверяем все сегменты, кроме головы от 1 индекса
        for segment in self.positions[1:]:
            if head_position == segment:
                return True  # Столкновение
        return False  # Змейка жива

    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
    return True


def main():
    """Основная логика игры."""
    pygame.init()

    # Создаем объекты
    snake = Snake()
    apple = Apple()

    print('Игра запущена! Змейка создана.')
    print(f'Позиция змейки: {snake.positions}')
    print(f'Позиция яблока: {apple.position}')

    # Основной игровой цикл
    running = True
    while running:
        # Обработка событий
        running = handle_keys(snake)

        # Обновления направления
        snake.update_direction()

        # Движение змейки
        new_head_position = snake.move()

        # Проверка съедания яблока
        if new_head_position == apple.position:
            snake.length += 1  # Увеличиваем длину змейки
            snake.grow_next_move = True  # Установка флага роста
            apple.randomize_position()  # Создаем новое яблоко
            print(f"Съедено яблоко! Длина змейки: {snake.length}")
            print(f"Позиций в списке: {len(snake.positions)}")  # Для отладки

        # Проверка столкновения с собой
        if snake.check_collision():
            print("Столкновение! Игра начинается заново.")
            snake.reset()

        # Очищаем экран
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Отрисовывем объекты
        apple.draw()
        snake.draw()

        # Обноваляем экран
        pygame.display.update()

        # Ограничиваем FPS
        clock.tick(SPEED)

    pygame.quit()


if __name__ == '__main__':
    main()
