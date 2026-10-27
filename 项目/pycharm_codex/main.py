import random
import tkinter as tk


CELL_SIZE = 24
GRID_WIDTH = 24
GRID_HEIGHT = 18
START_SPEED_MS = 130
MIN_SPEED_MS = 60
SPEED_STEP = 3

BACKGROUND = "#101820"
GRID_LINE = "#1d2a33"
SNAKE_HEAD = "#00c2a8"
SNAKE_BODY = "#6de5c4"
FOOD = "#ff5a5f"
TEXT = "#f4f7f5"
MUTED = "#95a3ad"


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("贪吃蛇")
        self.root.resizable(False, False)

        self.canvas_width = GRID_WIDTH * CELL_SIZE
        self.canvas_height = GRID_HEIGHT * CELL_SIZE

        self.score_var = tk.StringVar()
        self.state_var = tk.StringVar()

        header = tk.Frame(root, bg=BACKGROUND)
        header.pack(fill="x")

        tk.Label(
            header,
            textvariable=self.score_var,
            bg=BACKGROUND,
            fg=TEXT,
            font=("Microsoft YaHei UI", 14, "bold"),
            padx=12,
            pady=10,
        ).pack(side="left")

        tk.Label(
            header,
            textvariable=self.state_var,
            bg=BACKGROUND,
            fg=MUTED,
            font=("Microsoft YaHei UI", 10),
            padx=12,
            pady=10,
        ).pack(side="right")

        self.canvas = tk.Canvas(
            root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg=BACKGROUND,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<space>", lambda _event: self.toggle_pause())
        self.root.bind("<Return>", lambda _event: self.start_new_game())

        self.after_id = None
        self.start_new_game()

    def start_new_game(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.snake = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y),
        ]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food = self.create_food()
        self.score = 0
        self.speed_ms = START_SPEED_MS
        self.is_paused = False
        self.is_game_over = False
        self.update_labels()
        self.draw()
        self.schedule_next_tick()

    def create_food(self):
        empty_cells = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in self.snake
        ]
        return random.choice(empty_cells)

    def schedule_next_tick(self):
        self.after_id = self.root.after(self.speed_ms, self.tick)

    def tick(self):
        if self.is_paused or self.is_game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if self.has_collision(new_head):
            self.end_game()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.speed_ms = max(MIN_SPEED_MS, self.speed_ms - SPEED_STEP)
            self.food = self.create_food()
        else:
            self.snake.pop()

        self.update_labels()
        self.draw()
        self.schedule_next_tick()

    def has_collision(self, position):
        x, y = position
        outside_board = x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT
        hits_body = position in self.snake
        return outside_board or hits_body

    def end_game(self):
        self.is_game_over = True
        self.update_labels()
        self.draw()
        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2,
            text="游戏结束\n按 Enter 重新开始",
            fill=TEXT,
            font=("Microsoft YaHei UI", 22, "bold"),
            justify="center",
        )

    def toggle_pause(self):
        if self.is_game_over:
            return

        self.is_paused = not self.is_paused
        self.update_labels()
        if not self.is_paused:
            self.schedule_next_tick()

    def on_key_press(self, event):
        key_to_direction = {
            "Up": (0, -1),
            "w": (0, -1),
            "W": (0, -1),
            "Down": (0, 1),
            "s": (0, 1),
            "S": (0, 1),
            "Left": (-1, 0),
            "a": (-1, 0),
            "A": (-1, 0),
            "Right": (1, 0),
            "d": (1, 0),
            "D": (1, 0),
        }

        new_direction = key_to_direction.get(event.keysym)
        if new_direction is None:
            return

        dx, dy = self.direction
        next_dx, next_dy = new_direction
        if (dx + next_dx, dy + next_dy) == (0, 0):
            return

        self.next_direction = new_direction

    def update_labels(self):
        self.score_var.set(f"得分：{self.score}")
        if self.is_game_over:
            self.state_var.set("Enter 重新开始")
        elif self.is_paused:
            self.state_var.set("已暂停 · Space 继续")
        else:
            self.state_var.set("方向键/WASD 移动 · Space 暂停")

    def draw(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_cell(self.food, FOOD)

        for index, position in enumerate(self.snake):
            color = SNAKE_HEAD if index == 0 else SNAKE_BODY
            self.draw_cell(position, color)

    def draw_grid(self):
        for x in range(0, self.canvas_width, CELL_SIZE):
            self.canvas.create_line(x, 0, x, self.canvas_height, fill=GRID_LINE)
        for y in range(0, self.canvas_height, CELL_SIZE):
            self.canvas.create_line(0, y, self.canvas_width, y, fill=GRID_LINE)

    def draw_cell(self, position, color):
        x, y = position
        padding = 2
        left = x * CELL_SIZE + padding
        top = y * CELL_SIZE + padding
        right = (x + 1) * CELL_SIZE - padding
        bottom = (y + 1) * CELL_SIZE - padding
        self.canvas.create_rectangle(
            left,
            top,
            right,
            bottom,
            fill=color,
            outline="",
        )


if __name__ == "__main__":
    window = tk.Tk()
    SnakeGame(window)
    window.mainloop()
