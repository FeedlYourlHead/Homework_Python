def init():
    directions = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
    start_pos = (3, 3)
    exit_pos = (6, 2)


# TODO:Доделать функцию


def print_maze(maze):
    pass  # TODO:Сделать функцию


def find_exit(maze, x, y):
    pass  # TODO:Сделать функцию


def get_move(player_turn):
    pass  # TODO:Сделать функцию


def main():
    pass  # TODO:Сделать функцию


# NOTE:
# def get_moves(piece, position, board):
#     x, y = position
#     moves = [] #список возможных ходов
#     color = piece['color']
#     # [[{}, {}, {}], [{}, {}, {}], [{},{},{}]]
#     # dy dx -направления
#     symbol = piece['symbol'].upper()
#     if symbol == 'P':#пешка
#       if color == 'white':
#             direction = -1
#         else:
#             direction = 1
#         # direction = -1 if color=='white' else 1
#         #ход на одну клетку
#         if 0 <= y + direction < 8 and board[y+direction][x] is None:
#             moves.append((x, y+direction))
#             #ход на 2 первый ход
#             # if board[y][x]
#         #взятие по диагонали
#         for dx in [-1, 1]:
#             # nx, ny - новые координаты
#             nx, ny = x + dx, y + direction
#             if 0 <= nx < 8 and 0 <= ny < 8:
#                 target = board[ny][nx]#цель, новая позиция
#                 if target is None or target['color'] != color:
#                     moves.append((nx, ny))
#
