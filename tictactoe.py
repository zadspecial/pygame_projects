dictDactDoe = {
    'tl': ' ', 't': ' ', 'tr': ' ',
    'l': ' ', 'm': ' ', 'r': ' ',
    'bl': ' ', 'b': ' ', 'br': ' '
}

def mark(dictDactDoe, pos, sign):
    """
    assigns a mark on dictDactDoe
    :param dictDactDoe: dict
    :param pos: str
    :param sign: str
    :return: bool
    """
    if dictDactDoe[pos] == ' ':
        dictDactDoe[pos] = sign
        return True
    else:
        print("You can't replace another mark. Please pick another position.")
        return False

# testMark
# print(dictDactDoe)
# mark(dictDactDoe, 'l', 'o')
# print(dictDactDoe)

def showGrid(dictDactDoe):
    """
    prints the tic-tac-toe grid
    :param dictDactDoe: dict
    :return: None
    """
    count = 0
    for val in dictDactDoe.values():
        count += 1
        print(val, end='')
        if count == 3 or count == 6 or count == 9:
            print()
            if count == 3 or count == 6:
                print('---------')
        else:
            print(' | ', end='')
    print()

def isOver(dictDactDoe):
    """
    returns win, draw or not over
    :param dictDactDoe: dict
    :return: str
    """
    # shortcuts
    tl = dictDactDoe['tl']
    t = dictDactDoe['t']
    tr = dictDactDoe['tr']
    l = dictDactDoe['l']
    m = dictDactDoe['m']
    r = dictDactDoe['r']
    bl = dictDactDoe['bl']
    b = dictDactDoe['b']
    br = dictDactDoe['br']

    # boolean variables
    row1 = (tl == 'X' and t == 'X' and tr == 'X') or (tl == 'O' and t == 'O' and tr == 'O')
    row2 = (l == 'X' and m == 'X' and r == 'X') or (l == 'O' and m == 'O' and r == 'O')
    row3 = (bl == 'X' and b == 'X' and br == 'X') or (bl == 'O' and b == 'O' and br == 'O')

    col1 = (tl == 'X' and l == 'X' and bl == 'X') or (tl == 'O' and l == 'O' and bl == 'O')
    col2 = (t == 'X' and m == 'X' and b == 'X') or (t == 'O' and m == 'O' and b == 'O')
    col3 = (tr == 'X' and r == 'X' and br == 'X') or (tr == 'O' and r == 'O' and br == 'O')

    diag1 = (tl == 'X' and m == 'X' and br == 'X') or (tl == 'O' and m == 'O' and br == 'O')
    diag2 = (tr == 'X' and m == 'X' and bl == 'X') or (tr == 'O' and m == 'O' and bl == 'O')

    draw = tl != ' ' and t != ' ' and tr != ' ' and l != ' ' and m != ' ' and r != ' ' and bl != ' ' and b != ' ' and br != ' '
    # final statement
    if row1 or row2 or row3 or col1 or col2 or col3 or diag1 or diag2:
        return 'win'
    elif draw:
        return 'draw'
    else:
        return 'notOver'

def isDraw(dictDactDoe):
    draw = tl != ' ' and t != ' ' and tr != ' ' and l != ' ' and m != ' ' and r != ' ' and bl != ' ' and b != ' ' and br != ' '
    return draw

def playGame(dictDactDoe):
    playerTurn = 1
    while isOver(dictDactDoe) == 'notOver':
        # assigning sign to players
        if playerTurn == 1:
            sign = 'X'
        else:
            sign = 'O'

        showGrid(dictDactDoe)
        print("Player " + str(playerTurn) + "'s turn.")
        while True:
            pos = input("Enter the position in the grid: ")
            if mark(dictDactDoe, pos, sign) == True:
                break

        # change playerTurn
        if playerTurn == 1:
            playerTurn = 2
        else:
            playerTurn = 1

    # change playerTurn after game ends
    showGrid(dictDactDoe)
    if isOver(dictDactDoe) == 'win':
        if playerTurn == 1:
            playerTurn = 2
        else:
            playerTurn = 1
        print("Player " + str(playerTurn) + " wins!")
    else:
        print("It's a draw.")

    # gotta make sure no one replaces
# showGrid(dictDactDoe)
# mark(dictDactDoe, 'l', 'X')
# mark(dictDactDoe, 'm', 'X')
# mark(dictDactDoe, 'r', 'X')
#
# showGrid(dictDactDoe)
# print(isOver(dictDactDoe))

playGame(dictDactDoe)