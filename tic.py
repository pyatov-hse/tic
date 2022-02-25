# Реализация игры крестики-нолики (tic-tac-toe)

def create_board(size: int) -> list:
    """ Возвращает многомерный массив (list) размера size с пустыми элементами (None) """
    board = [] # пустой список
    for x in range (size): # в каждой строке матрицы
        board.append([None]*size) # создаем size пустых элементов
    return board

def show_board (board: list):
    """ Отображает поле на экране (board - многомерный массив с ячейками поля)"""
    print (board)
    return 1

def ask_for_move():
    """ Запрашивает ход игрока и возвращает ход в пригодном для использования формате (y,x)"""
    move = (0,0)
    return move

def score_position(board):
    """Оценивает позицию на поле и возвращает True, если найден выигрыш (иначе - False)"""
    if len(board) > 0:
        return True
    else:
        return False

def make_move (board: list, move: tuple):
    """Делает ход move на поле board """
    newb = board
    newb.append(move)
    return newb

def main():

    board_size = 3
    win = False
    board = create_board(board_size) # генерация поля

    show_board(board) # вывод поля

    while not win: # основной цикл игры (пока нет победы)
        move = ask_for_move() # запросить ход
        board = make_move(board, move) # сделать ход
        show_board(board) # вывод поля
        win = score_position (board) # оценить позицию (есть ли выигрыш) - и установить win = True, если одна из сторон выиграла

    print ("That's all, folks!")

if __name__ == "__main__":
    main()
