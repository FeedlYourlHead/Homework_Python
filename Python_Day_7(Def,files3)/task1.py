def print_maze(maze):
    """Выводит текущее состояние лабиринта на экран"""
    for row in maze:
        print(" ".join(row))


def find_exit(maze, x, y):
    """Основная функция"""
    steps = 0

    while True:
        print_maze(maze)

        if maze[y][x] == "0":
            print(f"Поздравляем! Вы нашли выход за {steps} шагов!")
            return

        move = input("Введите направление (WASD): ").upper()
        nx, ny = x, y

        if move == "W":
            ny -= 1
        elif move == "S":
            ny += 1
        elif move == "A":
            nx -= 1
        elif move == "D":
            nx += 1
        else:
            print("Неверная команда! Используйте W, A, S, D")
            continue
        if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and maze[ny][nx] != "#":
            maze[y][x] = "-"

            x, y = nx, ny
            steps += 1

            if maze[y][x] != "0":
                maze[y][x] = "E"
        else:
            print(
                "Нельзя двигаться в этом направлении! Здесь стена или граница лабиринта."
            )


if __name__ == "__main__":
    maze = [
        ["#", "#", "#", "#", "#", "#", "#"],
        ["#", " ", " ", " ", " ", " ", "#"],
        ["#", " ", "#", "#", "#", " ", "#"],
        ["#", " ", "#", "E", " ", " ", "#"],
        ["#", " ", "#", "#", "#", " ", "#"],
        ["#", " ", " ", " ", "#", " ", "#"],
        ["#", "#", "0", "#", "#", "#", "#"],
    ]

    find_exit(maze, 3, 3)
