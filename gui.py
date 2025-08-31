import tkinter as tk
import time

from game_env import GameEnv

"""
Graphical Visualiser for Cheese Hunter. You may modify this file if desired.

COMP3702 Assignment 1 "Cheese Hunter" Support Code, 2025
"""


class Viewer:
    TILE_W = 32
    TILE_H = 32
    TILE_W_SMALL = 16
    TILE_H_SMALL = 16

    UPDATE_DELAY = 0.5
    TWEEN_STEPS = 16
    TWEEN_DELAY = 0.005

    def __init__(self, game_env):
        self.lever_images = None
        self.trap_images = None
        self.game_env = game_env
        init_state = game_env.get_init_state()
        self.last_state = init_state

        # Choose small or large mode
        self.window = tk.Tk()
        screen_width, screen_height = (
            self.window.winfo_screenwidth(),
            self.window.winfo_screenheight(),
        )
        if (screen_width < self.game_env.n_cols * self.TILE_W) or (
            screen_height < self.game_env.n_rows * self.TILE_H
        ):
            small_mode = True
            self.tile_w = self.TILE_W_SMALL
            self.tile_h = self.TILE_H_SMALL
        else:
            small_mode = False
            self.tile_w = self.TILE_W
            self.tile_h = self.TILE_H

        self.window.title("Cheese Hunter Visualiser")
        self.window.geometry(
            f"{self.game_env.n_cols * self.tile_w}x{self.game_env.n_rows * self.tile_h}"
        )

        self.canvas = tk.Canvas(self.window)
        self.canvas.configure(bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Load images
        if small_mode:
            self.background = tk.PhotoImage(file="gui_assets/Small/background_wall.png")
            self.tile_player = tk.PhotoImage(file="gui_assets/Small/player_mouse.png")
            self.tile_cheese = tk.PhotoImage(file="gui_assets/Small/goal_cheese.png")
            self.tile_ladder = tk.PhotoImage(file="gui_assets/Small/ladder.png")
            self.tile_stone = tk.PhotoImage(file="gui_assets/Small/solid_wall.png")
            self.trapdoors_closed = tk.PhotoImage(
                file="gui_assets/Small/trapdoors/closed_trapdoor.png"
            )
            self.trapdoors_open = tk.PhotoImage(
                file="gui_assets/Small/trapdoors/open_trapdoor.png"
            )

        else:
            self.background = tk.PhotoImage(file="gui_assets/background_wall.png")
            self.tile_player = tk.PhotoImage(file="gui_assets/player_mouse.png")
            self.tile_cheese = tk.PhotoImage(file="gui_assets/goal_cheese.png")
            self.tile_ladder = tk.PhotoImage(file="gui_assets/ladder.png")
            self.tile_stone = tk.PhotoImage(file="gui_assets/solid_wall.png")
            self.trapdoors_closed = tk.PhotoImage(
                file="gui_assets/trapdoors/closed_trapdoor.png"
            )
            self.trapdoors_open = tk.PhotoImage(
                file="gui_assets/trapdoors/open_trapdoor.png"
            )

        # Draw background (all permanent features, i.e. everything except player, traps, and levers)
        for r in range(self.game_env.n_rows):
            for c in range(self.game_env.n_cols):
                if self.game_env.grid_data[r][c] == GameEnv.SOLID_TILE:
                    self.canvas.create_image(
                        (c * self.tile_w),
                        (r * self.tile_h),
                        image=self.tile_stone,
                        anchor=tk.NW,
                    )
                elif self.game_env.grid_data[r][c] == GameEnv.LADDER_TILE:
                    self.canvas.create_image(
                        (c * self.tile_w),
                        (r * self.tile_h),
                        image=self.background,
                        anchor=tk.NW,
                    )
                    self.canvas.create_image(
                        (c * self.tile_w),
                        (r * self.tile_h),
                        image=self.tile_ladder,
                        anchor=tk.NW,
                    )
                elif self.game_env.grid_data[r][c] in (
                    GameEnv.AIR_TILE,
                    GameEnv.TRAPDOOR,
                ):
                    self.canvas.create_image(
                        (c * self.tile_w),
                        (r * self.tile_h),
                        image=self.background,
                        anchor=tk.NW,
                    )
                if r == self.game_env.goal_row and c == self.game_env.goal_col:
                    self.canvas.create_image(
                        (c * self.tile_w),
                        (r * self.tile_h),
                        image=self.tile_cheese,
                        anchor=tk.NW,
                    )

        self.trap_images = []
        self.draw_traps(init_state.row, init_state.col)

        # Draw player for initial state
        self.player_image = None
        self.draw_player(init_state.row, init_state.col)

        self.window.update()
        self.last_update_time = time.time()


    def update_state(self, state):
        # Delete then redraw all traps
        for trap in self.trap_images:
            self.canvas.delete(trap)
        self.draw_traps(state.row, state.col)

        # Remove and re-draw player
        self.canvas.delete(self.player_image)
        self.draw_player(state.row, state.col)

        # Tween player to new position
        for i in range(1, self.TWEEN_STEPS + 1):
            time.sleep(self.TWEEN_DELAY)
            self.canvas.delete(self.player_image)
            r1 = self.last_state.row + (i / self.TWEEN_STEPS) * (
                state.row - self.last_state.row
            )
            c1 = self.last_state.col + (i / self.TWEEN_STEPS) * (
                state.col - self.last_state.col
            )
            # Remove old player position, draw new player position
            self.draw_player(r1, c1)
            self.window.update()
        self.last_state = state

        # Delay until next update
        self.window.update()

        time_since_last_update = time.time() - self.last_update_time
        time.sleep(max(self.UPDATE_DELAY - time_since_last_update, 0))
        self.last_update_time = time.time()

    def draw_traps(self, player_row, player_col):
        self.trap_images = []
        for row, col in self.game_env.trap_positions:
            if (row, col) == (player_row, player_col):
                self.trap_images.append(
                    self.canvas.create_image(
                        (col * self.tile_w),
                        (row * self.tile_h),
                        image=self.trapdoors_open,
                        anchor=tk.NW,
                    )
                )
            else:
                self.trap_images.append(
                    self.canvas.create_image(
                        (col * self.tile_w),
                        (row * self.tile_h),
                        image=self.trapdoors_closed,
                        anchor=tk.NW,
                    )
                )

    def draw_player(self, row, col):
        self.player_image = self.canvas.create_image(
            (col * self.tile_w),
            (row * self.tile_h),
            image=self.tile_player,
            anchor=tk.NW,
        )