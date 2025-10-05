# 10. Игра "Крестики-нолики" с искусственным интеллектом:
# Напишите игру "Крестики-нолики", в которой пользователь играет
# против компьютера. Для хранения текущего состояния игрового поля
# используйте список списков или множество. Компьютер должен иметь
# стратегию игры, чтобы противостоять пользователю. Для генерации ходов
# компьютера используйте модуль random.

import numpy as np
from random import randint


# Процедура вывода поля
def print_board(board):
    for line in board:
        print(line, end='\n')


# Ход человека
def human_step(board):
    print('Ходит игрок "X"')
    x, y = map(int, (input('Введите номер строки и столбца через пробел: ').split()))
    if board[x][y] == ' ':
        board[x][y] = 'X'
    else:
        while True:
            x, y = map(int, (input('Поле занято! Попробуйте еще раз: ').split()))
            if board[x][y] == ' ':
                board[x][y] = 'X'
                break
    return board


# Ход компьютера
def ai_step(board):
    print('Ходит игрок "O"')

    # Функция исключения победы по строкам
    for line in board:
        if line.count('X') == 2 and line.count(' ') == 1:
            for i in range(3):
                if line[i] == ' ':
                    line[i] = 'O'
                    return board
        # Функция победы по строкам
        elif line.count('O') == 2 and line.count(' ') == 1:
            for i in range(3):
                if line[i] == ' ':
                    line[i] = 'O'
                    return board

    # Функция исключения победы по столбцам
    board_rot_90 = rotate_matrix_90(board)
    for line in board_rot_90:
        if line.count('X') == 2 and line.count(' ') == 1:
            for i in range(3):
                if line[i] == ' ':
                    line[i] = 'O'
                    board = rotate_matrix_90(rotate_matrix_90(rotate_matrix_90(board_rot_90)))
                    return board
        # Функция победы по столбцам
        elif line.count('O') == 2 and line.count(' ') == 1:
            for i in range(3):
                if line[i] == ' ':
                    line[i] = 'O'
                    return board

    # Функция исключения победы по главной диагонали
    main_diag = [board[i][i] for i in range(3)]
    if main_diag.count('X') == 2 and main_diag.count(' ') == 1:
        for i in range(3):
            if board[i][i] == ' ':
                board[i][i] = 'O'
                return board
    # Функция победы по главной диагонали
    elif main_diag.count('O') == 2 and main_diag.count(' ') == 1:
        for i in range(3):
            if board[i][i] == ' ':
                board[i][i] = 'O'
                return board

    # Функция исключения победы по второстепенной диагонали
    board_rot_90 = rotate_matrix_90(board)
    second_diag = [board_rot_90[i][i] for i in range(3)]
    if second_diag.count('X') == 2 and second_diag.count(' ') == 1:
        for i in range(3):
            if board_rot_90[i][i] == ' ':
                board_rot_90[i][i] = 'O'
                board = rotate_matrix_90(rotate_matrix_90(rotate_matrix_90(board_rot_90)))
                return board
    # Функция победы по второстепенной диагонали
    elif main_diag.count('O') == 2 and main_diag.count(' ') == 1:
        for i in range(3):
            if board[i][i] == ' ':
                board[i][i] = 'O'
                return board

    # Функцию "занять центр"
    if board[1][1] == ' ':
        board[1][1] = 'O'
        return board

    while True:
        x, y = map(int, [randint(0, 2) for _ in range(2)])
        if board[x][y] == ' ':
            board[x][y] = 'O'
            break
    return board


# Функция проверки состояния поля на победу
def check_win(board):
    np_board = np.array(board)
    for k in range(2):
        np_rot = np.rot90(np_board, k)
        win_diag = set(np_rot.diagonal())
        if len(win_diag) == 1 and set(win_diag) != {' '}:
            return True
        for line in np_rot:
            if len(set(line)) == 1 and set(line) != {' '}:
                return True

    # Проверка на ничью
    list_temp = []
    for line in board:
        for elem in line:
            list_temp.append(elem)
    if ' ' not in list_temp:
        return None

    return False


def rotate_matrix_90(matrix):
    return [list(reversed(col)) for col in zip(*matrix)]


# Инициализация игры
game_board = [[' ' for _ in range(3)] for _ in range(3)]

active_user = 'X'
game_start = True

while game_start:
    # Выведем поле
    print_board(game_board)
    # Принимаем ход игрока
    if active_user == 'X':
        game_board = human_step(game_board)
    else:
        game_board = ai_step(game_board)
    # Проверка победы или ничьи
    if check_win(game_board):
        print(f'Игра окончена!\n'
              f'Победили: {active_user}')
        print_board(game_board)
        break
    elif check_win(game_board) is None:
        print('Ничья! Это почти победа!')
        print_board(game_board)
        break

    # Смена игрока
    active_user = 'O' if active_user == 'X' else 'X'
