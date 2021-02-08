"""
Module which solves the scy scrapers problem using certain rules
github repo: https://github.com/bohdaholas/scyscrapers/blob/main/scyscrapers.py
"""


def read_input(path: str):
    """
    Read game board file from path.
    Return list of str.
    """
    with open(path, 'r') as file:
        rows = list(file.read().splitlines())
    return rows


def left_to_right_check(input_line: str, pivot: int):
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    >>> left_to_right_check("132354*", 3)
    False
    """
    visible_buildings = 1
    buildings = input_line[1: -1]
    building = buildings[0]
    for other in buildings[1:]:
        if building < other:
            building = other
            visible_buildings += 1
    if visible_buildings == pivot:
        return True
    return False


def check_not_finished_board(board: list):
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', \
    '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', \
    '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', \
    '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row in board:
        if '?' in row:
            return False
    return True


def check_uniqueness_in_rows(board: list, row=True):
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', \
     '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', \
    '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', \
    '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', \
    '*35214*', '441532*', '*22222*'])
    True
    >>> check_uniqueness_in_rows(['***212*', '412453*', '423145*', '*543215', \
    '*35214*', '441532*', '*22222*'])
    True
    """
    board = board[1: -1] if row else board
    for row in board:
        buildings = row[1: -1]
        if len(buildings) != len(set(buildings)) or \
                row[0].isdigit() and row[-1].isdigit():
            return False
    return True


def check_horizontal_visibility(board: list, row=True):
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453t* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', '*543215', \
    '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215', \
    '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215', \
    '*35214*', '*41532*', '*2*1***'])
    False
    """
    board = board[1: -1] if row else board
    for row in board:
        left_to_right_direction = None
        if row[0] == '*' and row[-1] != '*':
            left_to_right_direction = False
            hint = int(row[-1])
        if row[0] != '*' and row[-1] == '*':
            left_to_right_direction = True
            hint = int(row[0])
        if left_to_right_direction is True and not left_to_right_check(row, hint):
            return False
        if left_to_right_direction is False and not left_to_right_check(row[::-1], hint):
            return False
    return True


def get_board_columns(board):
    """
    Get board columns
    >>> get_board_columns(['***21**', '412453*', '423145*', '*543215', \
    '*35214*', '*41532*', '*2*1***'])
    ['*125342', '*23451*', '2413251', '154213*', '*35142*']
    """
    columns = []
    for i in range(1, 5 + 1):
        column = ''
        for row in board:
            column += row[i]
        columns.append(column)
    return columns


def check_columns(board: list):
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height)
    and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', \
    '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', \
    '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', \
    '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_columns(['***22**', '412453*', '423145*', '*543215', \
    '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', \
    '*35214*', '*41532*', '*2*4***'])
    False
    """
    return check_uniqueness_in_rows(get_board_columns(board), False) and \
           check_horizontal_visibility(get_board_columns(board), False)


def check_skyscrapers(input_path: str):
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.
    """
    with open(input_path, 'r') as file:
        board = file.read().splitlines()
        if check_uniqueness_in_rows(board) and check_columns(board) and \
                check_horizontal_visibility(board) and \
                check_horizontal_visibility(get_board_columns(board)):
            return True
        return False
