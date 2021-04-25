# coding=utf-8
import numpy as np

from lib.RandomLib import random


class MazeBuilder:
    @classmethod
    def build_prime_maze(self, num_rows, num_cols):  # 扭曲迷宫
        random.seed()
        # (5个参数的含义：左，上，右，下，参数)
        m = np.zeros((num_rows, num_cols, 5), dtype=np.uint8)
        r, c = 0, 0
        trace = [(r, c)]
        while trace:
            r, c = random.choice(trace)
            m[r, c, 4] = 1	# 标记为通路
            trace.remove((r, c))
            check = []
            if c > 0:
                if m[r, c - 1, 4] == 1:
                    check.append('L')
                elif m[r, c - 1, 4] == 0:
                    trace.append((r, c - 1))
                    m[r, c - 1, 4] = 2	# 标记为已访问
            if r > 0:
                if m[r - 1, c, 4] == 1:
                    check.append('U')
                elif m[r - 1, c, 4] == 0:
                    trace.append((r - 1, c))
                    m[r - 1, c, 4] = 2
            if c < num_cols - 1:
                if m[r, c + 1, 4] == 1:
                    check.append('R')
                elif m[r, c + 1, 4] == 0:
                    trace.append((r, c + 1))
                    m[r, c + 1, 4] = 2
            if r < num_rows - 1:
                if m[r + 1, c, 4] == 1:
                    check.append('D')
                elif m[r + 1, c, 4] == 0:
                    trace.append((r + 1, c))
                    m[r + 1, c, 4] = 2
            if len(check):
                direction = random.choice(check)
                if direction == 'L':	# 打通一面墙
                    m[r, c, 0] = 1
                    c = c - 1
                    m[r, c, 2] = 1
                if direction == 'U':
                    m[r, c, 1] = 1
                    r = r - 1
                    m[r, c, 3] = 1
                if direction == 'R':
                    m[r, c, 2] = 1
                    c = c + 1
                    m[r, c, 0] = 1
                if direction == 'D':
                    m[r, c, 3] = 1
                    r = r + 1
                    m[r, c, 1] = 1
        m[0, 0, 0] = 1
        m[num_rows - 1, num_cols - 1, 2] = 1
        return m.tolist()

    @classmethod
    def build_tortuous_maze(self, num_rows, num_cols):  # 曲折迷宫
        random.seed()
        m = np.zeros((num_rows, num_cols, 5), dtype=np.uint8)
        r = 0
        c = 0
        trace = [(r, c)]
        while trace:
            m[r, c, 4] = 1  # 标记为已访问
            check = []
            if c > 0 and m[r, c - 1, 4] == 0:
                check.append('L')
            if r > 0 and m[r - 1, c, 4] == 0:
                check.append('U')
            if c < num_cols - 1 and m[r, c + 1, 4] == 0:
                check.append('R')
            if r < num_rows - 1 and m[r + 1, c, 4] == 0:
                check.append('D')
            if len(check):
                trace.append([r, c])
                direction = random.choice(check)
                if direction == 'L':
                    m[r, c, 0] = 1
                    c = c - 1
                    m[r, c, 2] = 1
                if direction == 'U':
                    m[r, c, 1] = 1
                    r = r - 1
                    m[r, c, 3] = 1
                if direction == 'R':
                    m[r, c, 2] = 1
                    c = c + 1
                    m[r, c, 0] = 1
                if direction == 'D':
                    m[r, c, 3] = 1
                    r = r + 1
                    m[r, c, 1] = 1
            else:
                r, c = trace.pop()
        m[0, 0, 0] = 1
        m[num_rows - 1, num_cols - 1, 2] = 1
        return m.tolist()