import numpy as np
import time
import sys
import tkinter as tk


MAZE_UNIT = 40   # pixels
MAZE_H = 8      # grid height
MAZE_W = 8      # grid width


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.bomb = []
        self.action_space = ['up', 'down', 'left', 'right']
        self.len_actions = len(self.action_space)
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_H * MAZE_UNIT, MAZE_H * MAZE_UNIT))    # create 8 * 8 grid
        self._build_maze()

    def _build_maze(self): 
        # create 8 * 8 grid
        self.canvas = tk.Canvas(self, bg='white',
                                height=MAZE_H * MAZE_UNIT,
                                width=MAZE_W * MAZE_UNIT)

        # create grids
        for col in range(0, MAZE_W * MAZE_UNIT, MAZE_UNIT):
            x0, y0, x1, y1 = col, 0, col, MAZE_H * MAZE_UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for row in range(0, MAZE_H * MAZE_UNIT, MAZE_UNIT):
            x0, y0, x1, y1 = 0, row, MAZE_W * MAZE_UNIT, row
            self.canvas.create_line(x0, y0, x1, y1)

        # get the top-left point as origin
        start = np.array([20, 20])

        # ending if meet bomb1
        bomb1_center = start + np.array([MAZE_UNIT * 7, MAZE_UNIT * 5])
        self.bomb1 = self.canvas.create_oval(
            bomb1_center[0] - 15, bomb1_center[1] - 15,
            bomb1_center[0] + 15, bomb1_center[1] + 15,
            fill='black')

        bomb2_center = start + np.array([MAZE_UNIT * 5, MAZE_UNIT * 6])
        self.bomb2 = self.canvas.create_oval(
            bomb2_center[0] - 15, bomb2_center[1] - 15,
            bomb2_center[0] + 15, bomb2_center[1] + 15,
            fill='black')

        bomb3_center = start + np.array([MAZE_UNIT * 0, MAZE_UNIT * 2])
        self.bomb3 = self.canvas.create_oval(
            bomb3_center[0] - 15, bomb3_center[1] - 15,
            bomb3_center[0] + 15, bomb3_center[1] + 15,
            fill='black')

        bomb4_center = start + np.array([MAZE_UNIT * 2, MAZE_UNIT * 5])
        self.bomb4 = self.canvas.create_oval(
            bomb4_center[0] - 15, bomb4_center[1] - 15,
            bomb4_center[0] + 15, bomb4_center[1] + 15,
            fill='black')

        bomb5_center = start + np.array([MAZE_UNIT * 4, MAZE_UNIT * 4])
        self.bomb5 = self.canvas.create_oval(
            bomb5_center[0] - 15, bomb5_center[1] - 15,
            bomb5_center[0] + 15, bomb5_center[1] + 15,
            fill='black')

        # winning point
        win_center = start + MAZE_UNIT * 7
        self.win = self.canvas.create_oval(
            win_center[0] - 15, win_center[1] - 15,
            win_center[0] + 15, win_center[1] + 15,
            fill='blue')

        # the "robot"
        self.robot = self.canvas.create_rectangle(
            start[0] - 15, start[1] - 15,
            start[0] + 15, start[1] + 15,
            fill='yellow')

        # pack all
        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.robot)
        start = np.array([20, 20])
        self.robot = self.canvas.create_rectangle(
            start[0] - 15, start[1] - 15,
            start[0] + 15, start[1] + 15,
            fill='yellow')
        # return observation
        return self.canvas.coords(self.robot)

    def step(self, cur_action):
        s = self.canvas.coords(self.robot)
        next_move = np.array([0, 0])
        if cur_action == 0:     # up
            if s[1] > MAZE_UNIT:
                next_move[1] -= MAZE_UNIT
        elif cur_action == 1:   # down
            if s[1] < (MAZE_H - 1) * MAZE_UNIT:
                next_move[1] += MAZE_UNIT
        elif cur_action == 2:   # right
            if s[0] < (MAZE_W - 1) * MAZE_UNIT:
                next_move[0] += MAZE_UNIT
        elif cur_action == 3:   # left
            if s[0] > MAZE_UNIT:
                next_move[0] -= MAZE_UNIT

        self.canvas.move(self.robot, next_move[0], next_move[1])

        s_ = self.canvas.coords(self.robot)  # switch to next state

        # reward function

        if s_ == self.canvas.coords(self.win):
            reward = 100
            done = True
            s_ = 'END'
        elif s_ in [self.canvas.coords(self.bomb1), self.canvas.coords(self.bomb2), self.canvas.coords(self.bomb3), self.canvas.coords(self.bomb4), self.canvas.coords(self.bomb5)]:
            reward = -1
            done = True
            s_ = 'END'
        else:
            reward = 0
            done = False

        return s_, reward, done

    def render(self):
        time.sleep(0.1)
        self.update()


def update():
    for t in range(10):
        s = env.reset()
        while True:
            env.render()
            # set initial move is down
            act = 1

            s, r, done = env.step(act)
            if done:
                break

if __name__ == '__main__':
    env = Maze()
    env.after(50, update)
    env.mainloop()