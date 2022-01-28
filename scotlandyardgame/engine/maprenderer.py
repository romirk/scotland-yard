import numpy as np


def draw_subway_line(p1, p2):
    mid_point = None
    if abs(p1[0] - p2[0]) < abs(p1[1] - p2[1]):
        if p2[1] < p1[1]:
            # down
            m = -1
        else:
            # up
            m = 1
        mid_point = (p2[0], m * abs(p1[0]-p2[0]) + p1[1])
    else:
        if p2[0] < p1[0]:
            # left
            m = -1
        else:
            # right
            m = 1
        mid_point = (m * abs(p2[1] - p1[1]) + p1[0], p2[1])

    

def generate_board(shape, ones):
    size = np.product(shape)
    board = np.zeros(size, dtype=int)
    i = np.sort(np.random.choice(np.arange(size), ones, replace=False))
    print(i)
    board[i] = np.arange(1, 201)
    return board.reshape(shape)

def generate_coords(board):
    return np.argwhere(board)