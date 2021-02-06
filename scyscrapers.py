"""
Module which solves the scy scrapers problem using certain rules
github repo:
"""


def read_input(path: str):
    """
    Read game board file from path.
    Return list of str.

    >>> read_input("../check.txt")
    ['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***']
    """
    rows = []
    with open(path, 'r') as file:
        rows = [row for row in file.read().splitlines()]
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
    """
    hint = int(input_line[0])
    visible_buildings = 1
    buildings = input_line[1: -1]
    building = buildings[0]
    for other in buildings[1:]:
        if building < other:
            building = other
            visible_buildings += 1
    if visible_buildings == hint:
        return True
    return False


def check_not_finished_board(board: list):
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row in board:
        if '?' in row:
            return False
    return True


def check_uniqueness_in_rows(board: list):
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row in board:
        buildings = row[1: -1]
        buildings = buildings.replace('*', '')
        if len(buildings) != len(set(buildings)):
            return False
    return True


def check_horizontal_visibility(board: list):
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453t* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
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
    columns = []
    for i in range(1, 5 + 1):
        column = ''
        for row in board:
            column += row[i]
        columns.append(column)
    return columns


def check_columns(board: list):
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height) and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    return check_uniqueness_in_rows(get_board_columns(board))


def check_skyscrapers(input_path: str):
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    >>> check_skyscrapers("check.txt")
    True
    """
    with open(input_path, 'r') as file:
        board = file.read().splitlines()
        if check_uniqueness_in_rows(board) and check_columns(board) and \
                check_horizontal_visibility(board) and check_horizontal_visibility(get_board_columns(board)):
            return True
        return False
