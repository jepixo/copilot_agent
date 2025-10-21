
import tkinter as tk
import random
import time
import os

os.environ['DISPLAY'] = ':0'  # Handle potential display issues

class FlappyBirdGame:
    def __init__(self, master):
        self.master = master
        master.title("Flappy Bird")
        self.width = 600
        self.height = 400
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="skyblue")
        self.canvas.pack()

        self.bird_x = 50
        self.bird_y = self.height // 2
        self.bird_radius = 15
        self.bird_velocity = 0
        self.gravity = 0.2  # Reduced gravity
        self.jump_strength = -6  # Reduced jump strength
        self.bird = self.canvas.create_oval(self.bird_x - self.bird_radius, self.bird_y - self.bird_radius,
                                            self.bird_x + self.bird_radius, self.bird_y + self.bird_radius, fill="yellow")

        self.pipe_width = 50
        self.pipe_gap = 150
        self.pipe_speed = 3
        self.pipes = []

        self.score = 0
        self.high_score = self.load_high_score()
        self.score_label = self.canvas.create_text(100, 20, text=f"Score: {self.score}", font=("Arial", 20), fill="white")
        self.high_score_label = self.canvas.create_text(300, 20, text=f"High Score: {self.high_score}", font=("Arial", 20), fill="white")


        self.start_button = tk.Button(master, text="Start Game", command=self.start_game)
        self.start_button.pack()
        self.jump_button = tk.Button(master, text="Jump", command=self.jump, state=tk.DISABLED)
        self.jump_button.pack()
        self.is_running = False

        self.game_over_text = None

    def start_game(self):
        self.is_running = True
        self.score = 0
        self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")
        self.bird_y = self.height // 2
        self.bird_velocity = 0
        self.canvas.move(self.bird, self.bird_x - self.canvas.coords(self.bird)[0] - self.bird_radius, self.bird_y - self.canvas.coords(self.bird)[1] - self.bird_radius)

        # Clear existing pipes
        for top_pipe, bottom_pipe in self.pipes:
            self.canvas.delete(top_pipe)
            self.canvas.delete(bottom_pipe)
        self.pipes = []

        if self.game_over_text:
            self.canvas.delete(self.game_over_text)
            self.game_over_text = None

        self.start_button.config(state=tk.DISABLED)
        self.jump_button.config(state=tk.NORMAL)
        self.master.after(20, self.game_loop)

    def jump(self):
        self.bird_velocity = self.jump_strength

    def create_pipe(self):
        pipe_height = random.randint(50, self.height - self.pipe_gap - 50)
        bottom_pipe_height = self.height - pipe_height - self.pipe_gap
        pipe_x = self.width
        top_pipe = self.canvas.create_rectangle(pipe_x, 0, pipe_x + self.pipe_width, pipe_height, fill="green")
        bottom_pipe = self.canvas.create_rectangle(pipe_x, self.height - bottom_pipe_height, pipe_x + self.pipe_width, self.height, fill="green")
        self.pipes.append((top_pipe, bottom_pipe))

    def move_pipes(self):
        for i, (top_pipe, bottom_pipe) in enumerate(self.pipes):
            self.canvas.move(top_pipe, -self.pipe_speed, 0)
            self.canvas.move(bottom_pipe, -self.pipe_speed, 0)
            if self.canvas.coords(top_pipe)[2] < 0:
                self.canvas.delete(top_pipe)
                self.canvas.delete(bottom_pipe)
                self.pipes.pop(i)
                self.score += 1
                self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")

    def check_collision(self):
        bird_coords = self.canvas.coords(self.bird)
        if bird_coords[1] <= 0 or bird_coords[3] >= self.height:
            return True

        for top_pipe, bottom_pipe in self.pipes:
            top_coords = self.canvas.coords(top_pipe)
            bottom_coords = self.canvas.coords(bottom_pipe)

            if top_coords[0] < self.bird_x + self.bird_radius < top_coords[2]:
                if bird_coords[1] < top_coords[3] or bird_coords[3] > bottom_coords[1]:
                    return True
        return False

    def game_loop(self):
        if self.is_running:
            self.bird_velocity += self.gravity
            self.bird_y += self.bird_velocity
            self.canvas.move(self.bird, 0, self.bird_velocity)

            if len(self.pipes) == 0 or self.canvas.coords(self.pipes[-1][0])[0] < self.width - 200:
                self.create_pipe()

            self.move_pipes()

            if self.check_collision():
                self.game_over()
                return

            self.master.after(20, self.game_loop)

    def game_over(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.start_button.config(relief=tk.RAISED, bg='green', fg='white')  # Light up the button
        self.jump_button.config(state=tk.DISABLED)

        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score(self.high_score)
            self.canvas.itemconfig(self.high_score_label, text=f"High Score: {self.high_score}")
            message = f"Game Over! New High Score: {self.high_score}!"
        else:
            message = f"Game Over! Score: {self.score}, High Score: {self.high_score}"

        self.game_over_text = self.canvas.create_text(self.width // 2, self.height // 2, text=message, font=("Arial", 24), fill="red")

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self, score):
        with open("highscore.txt", "w") as f:
            f.write(str(score))

root = tk.Tk()
game = FlappyBirdGame(root)
root.mainloop()
