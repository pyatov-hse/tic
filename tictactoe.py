# Реализация игры крестики-нолики (tic-tac-toe)
from os import write
import string
from datetime import datetime
import argparse

letters = string.ascii_lowercase
digits = string.digits

def create_board(size: int) -> list:
    """ Возвращает многомерный массив (list) размера size с пустыми элементами (None) """
    board = [] # пустой список
    for x in range (size): # в каждой строке матрицы
        board.append([None]*size) # создаем size пустых элементов
    return board

def get_formatted_board (board: list) -> str:
    """ Возвращает строку для вывода поля на экране на основе входящего многомерного массива с ячейками поля"""
    formatted_board = ""
    size = len(board) # размер поля
    cell_size = 3 # размер ячейки поля в символах (не считая границ ячейки) - нечетное число, дабы с каждой стороны символа было равное число пробелов
    spaces_num = (cell_size//2) # число пробелов с каждой стороны символа
    side_length = size * (cell_size+1) + 1 # длина верхней стороны строки поля (вывод "-")
    space = " " # разделитель для вывода поля
    divider = "-" * side_length
    tab = space * 4 # отбивка слева (от номеров строк)
    letters = "abcdefghijklmonpqrstuvwxyz"
    header = tab + space

    for i in range (size): # вывод заголовка
        header += f"{space*spaces_num}{letters[i]}{space*spaces_num}{space}"

    formatted_board += "\n" + header + "\n"

    for y in range (size):
        offset_cell = ' ' if y+1 < 10 else '' # если строк будет больше 10, потребуется смещение на 1 пробел вправо для номеров строк менее 10, чтобы верстка поля не уезжала
        offset_divider = ' ' if y+1 >= 10 else '' # если номер строки больше 10, добавить смещение слева к разделителю строки
        offset = offset_cell + offset_divider
        row = tab + (offset + divider) + "\n" + (offset_cell + f"{y+1}{tab[:-1]}") + "|"
        for x in range(size):
            sym = board[y][x] if board[y][x] else " "
            row += f"{space*spaces_num}{sym}{space*spaces_num}|"
        formatted_board += row + "\n"
    formatted_board += tab + (offset + divider) + "\n\n" # завершающая черта и +1 пустая строка

    return formatted_board

def check_coords (board: list, coords: tuple) -> bool:
    """ Проверяет координаты на корректность ввода и соответствие размерам поля.
        Возвращает True, если координаты введены правильно, и False во всех остальных случаях.
    """
    global letters
    global digits
    coords_ok = False
    board_horizontal_size = len(board) # размер доски в клетках по горизонтали
    board_vertical_size = len(board[0]) # размер доски в клетках по вертикали

    if len(coords) == 2:
        if coords[0] in letters[:board_horizontal_size] and coords[1] in digits[1:board_vertical_size+1]:
            coords_ok = True

    return coords_ok

def decrypt_coords (coords_string: str) -> tuple:
    """ Расшифровывает координаты из строки типа "a1" и возвращает кортеж с координатами (y,x) в матрице поля"""
    global letters
    global digits

    coord_x, coord_y = coords_string[0], coords_string[1]
    x = letters.find(coord_x)
    y = digits.find(coord_y) - 1
    if (y>=0 and x>=0):
        coords_decrypted = (y,x)
    else:
        coords_decrypted = (0,0)

    return coords_decrypted

def make_move (board: list, coords: tuple, side: str):
    """Ставит символ side по координатам coords на поле board """
    newb = board
    y,x = coords
    newb[y][x] = side
    return newb

def choose_first_side(sides: dict, sides_variants: dict) -> str:
    """Запрашивает ввод стороны - кто будет ходить первым. Принимает на вход словарь с символами сторон и вариантами их возможного ввода пользователем (рус, англ, цифра)"""
    side = False
    while not side:
        side = str(input (f"Кто ходит первым? - {sides['cross']} или {sides['nought']}: "))
        if side not in sides_variants['crosses'] and side not in sides_variants['noughts']:
            side = False
        elif side in sides_variants['crosses']:
            side = sides['cross']
        elif side in sides_variants['noughts']:
            side = sides['nought']
    return side

def change_side (sides, current_side):
    if current_side == sides['cross']:
        next_side = sides['nought']
    else:
        next_side = sides['cross']
    return next_side

def check_win(board: list, symbol, in_a_row: int) -> bool:
    """Оценивает позицию на поле, принимая поле board, символ и количество символов в ряд для победы (in_a_row). Возвращает True, если найден выигрыш (иначе - False)"""
    win = False

    # собрать все возможные согласно размерам поля варианты: горизонтали, вертикали, диагонали.
    board_size_y = len(board)
    board_size_x = len(board[0])
    win_diags_num = 2 + 4*(board_size_x-in_a_row) # число диагоналей для расчета выигрышных комбинаций

    rows = [[] for _ in range(board_size_y)]
    cols = [[] for _ in range(board_size_x)]
    fdiags = [[] for _ in range(board_size_y + board_size_x - 1)]
    bdiags = [[] for _ in range(len(fdiags))]
    min_bdiag = -board_size_y + 1

    for x in range(board_size_x):
        for y in range(board_size_y):
            item = board[y][x] if board[y][x] != None else ' '
            rows[y].append(item) # собираем горизонтали
            cols[x].append(item) # собираем вертикали
            fdiags[x+y].append(item) # собираем прямые диагонали
            bdiags[x-y-min_bdiag].append(item) # собираем обратные диагонали

    diags = fdiags + bdiags # объединяем все диагонали в один список

    # получаем списки подряд идущих символов по горизонталям, вертикалям и диагоналям
    rows_catx = ["".join(x) for x in rows]
    cols_catx = ["".join(x) for x in cols]
    diags_catx = ["".join(x) for x in diags if len(x)>=in_a_row]
    assert len(diags_catx) == win_diags_num, "too much diags" # проверяем, что число диагоналей равно расчетному числу диагоналей с длиной не менее in_a_row
    all_combinations = rows_catx + cols_catx + diags_catx

    # проходим по всем собранным вариантам и ищем в них выигрышные комбинации
    win_combinations = [combination for combination in all_combinations if symbol * in_a_row in combination]
    win = True if len(win_combinations) > 0 else False # если найдена хотя бы 1 выигрышная комбинация

    return win

def check_no_empty_cells (board: list) -> bool:
    empty_cells = 0
    for row in board:
        for col in row:
            empty_cells += 1 if col == None else 0
    no_empty_cells = True if empty_cells == 0 else False
    return no_empty_cells

def is_cell_empty (board: list, coords: tuple) -> bool:
    y,x = coords
    if board[y][x] == None:
        return True
    else:
        return False

def check_tie (board: list, in_a_row: int):
    board
    in_a_row
    return False

def write_list_into_file (filename: str, content: list):
    try:
        with open (filename, 'w', encoding='utf-8') as w_file: # записываем ходы в файл
            w_file.write("\n".join(content))
            result = True
    except:
        result = False
    return result

def main():

    # основные параметры игры
    sides = {'cross': 'x', 'nought': 'o'} # стороны
    sides_variants = {'crosses': ('x','X','Х','х'), 'noughts': ('0','o','O','о','О')} # варианты записи сторон
    board_size = 3
    in_a_row = 3 # выигрышная комбинация (сколько символов подряд по горизонтали, вертикали или диагонали)
    #
    # считываем аргументы из командной строки (если есть)
    my_parser = argparse.ArgumentParser(description='X-IN-A-ROW Game')
    my_parser.add_argument('-b', '--board_size',
                        metavar='X',
                        type=int,
                        help='size of the board (# of cells)')
    my_parser.add_argument('-i', '--in_a_row',
                        metavar='N',
                        type=int,
                        help='how many symbols should be found in a row for a win')
    args = my_parser.parse_args()
    board_size = args.board_size if args.board_size else board_size
    in_a_row = args.in_a_row if args.in_a_row else in_a_row
    #
    assert board_size >= in_a_row, f"заданный размер поля ({board_size}) меньше, чем нужно подряд идущих символов для победы ({in_a_row})"
    assert board_size <= 26, f"заданный размер поля ({board_size}) слишком велик (максимум - 26, по числу букв в английском алфавите - для обозначения координат)"

    # инициализация переменных для хранения флагов победы, ничьи и списка сделанных ходов
    win = False
    tie = False
    moves = []

    game_started_datetime = datetime.now().strftime("%y%m%d_%H%M%S") # время начала игры
    gamelog_filename = game_started_datetime + '_tictactoe_game.md.log' # имя файла для записи лога игры

    game_title = f'\"{in_a_row}-in-a-row\" game'
    game_title += ' (Tic-tac-toe)' if in_a_row == 3 and board_size == 3 else ''
    print (game_title)

    board = create_board(board_size) # генерация поля
    print (get_formatted_board(board)) # вывод изначального поля
    side = choose_first_side(sides, sides_variants)

    move_number = 1

    while not (win or tie): # основной цикл игры (пока нет победы)

        print (f"Ход {move_number}.", end=" ") # документируем номер хода

        coords_ok = False
        while not coords_ok:
            coords_string = input(f"Куда поставить {side} ? : ").lower() # запрашиваем координаты хода
            if check_coords(board, coords_string):
                coords = decrypt_coords(coords_string) # переводим их в приемлемый формат
                coords_ok = is_cell_empty (board, coords) # провереяем, не занята ли клетка
                if not coords_ok: # если клетка занята:
                    print ("Клетка уже занята.", end = " ")
            else:
                print ("Ошибочные координаты.", end = " ")
        moves.append(str(move_number) + ". " + ",".join([side,coords_string])) # записываем ход
        board = make_move(board, coords, side) # делаем ход согласно параметрам и получить новое состояние поля
        print (get_formatted_board(board)) # выводим обновленное поле
        win = check_win (board, side, in_a_row) # оцениваем позицию (есть ли выигрыш) - и ставим win = True, если одна из сторон выиграла
        if win:
            status = f'{side} wins!'
        else:
            if check_no_empty_cells(board): # все клетки заполнены, но никто не выиграл
                tie = True
                status = 'tie'
                # нужно в будущем расчет варианта ничьи, когда уже элементарно не хватает клеток, чтобы построить N in a row.
            else: # если нет ни выигрыша, ни ничьи, меняем сторону и начинаем новый ход
                side = change_side(sides, side) # меняем игровую сторону
                move_number += 1 # обновляем счетчик ходов

    print (status)
    game_finished_datetime = datetime.now().strftime("%y%m%d_%H%M%S") # время окончания игры

    # что пишем в лог игры:
    log_content = [f'# {game_title}\n', \
                    '## Parameters:', f'- board_size:{board_size}', f'- in_a_row{in_a_row}', \
                    '\n## Time:',f'- game started: {game_started_datetime}', f'- game finished: {game_finished_datetime}', \
                    '\n## Moves:', *moves
                  ]
    is_game_log_written = write_list_into_file(gamelog_filename, log_content)

    if is_game_log_written:
        print (f'game log was written into {gamelog_filename}')
    else:
        print (f'oops, game log wasn\'t written into {gamelog_filename}')

    print ("\nThat's all, folks!")

if __name__ == "__main__":
    main()
