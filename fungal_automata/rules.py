from utils import *
from cells import *

"""
Cellular Automata Rules
"""

# 1 cell -> 0.25mm

CELL_SIZE = 0.25

def rule_1(board, neighbors, time, growth_count=0, growth_rate=None):
    """
    Fungi Cellular Spread. Hyphae Speed

    If the current cell is fungi, grow towards the strongest fungal woodcell.
    """

    # if neighbors['current'].growth_rate

    if growth_rate != None:
        if growth_count > growth_rate:
            return

    max_neighbor = None
    if isinstance(neighbors['current'], FungiCell):
        max_neighbor = None
        for key, value in neighbors.items():

            if (value != None) and (max_neighbor == None) and (key != 'current') and (not isinstance(value, FungiCell)):
                max_neighbor = value

            else:
                if not isinstance(value, FungiCell) and value != None:

                    new_temp = value.temperature
                    max_n_temp = max_neighbor.temperature

                    tg_rate = neighbors['current'].calculate_total_growth(
                                neighbors['current'].get_temp_growth(new_temp)
                            )

                    tmg_rate = neighbors['current'].calculate_total_growth(
                                neighbors['current'].get_temp_growth(max_n_temp)
                            )

                    strength_check = max_neighbor.strength <= value.strength
                    heat_check = tg_rate >= tmg_rate

                    if heat_check and strength_check:
                        max_neighbor = value

                    # if max_neighbor.strength <= value.strength:
                        # max_neighbor = value

        if max_neighbor != None:
            new_cell = type(neighbors['current'])
            # print("max_neighbor: ", max_neighbor.temperature)
            # print("max_neighbor: ", max_neighbor)

            food_str = max_neighbor.strength

            hyphal = new_cell(
                        max_neighbor.row, max_neighbor.col, 0.25*max_neighbor.strength,
                        max_neighbor.temperature,
                        max_neighbor.moisture, max_neighbor.strength,
                        wood_growth=max_neighbor.wood_ext_rate
                    )

            total_growth = hyphal.get_total_growth()
            # print("total_growth: ", total_growth)
            board[max_neighbor.row][max_neighbor.col] = hyphal
            # print("growth_count: ", growth_count)
            # print("round(total_growth): ", round(total_growth))
            rule_1(
                    board,
                    get_surroundings(
                            board, hyphal.row, hyphal.col
                        ),
                    time,
                    growth_count+1,
                    round(total_growth)
                )
            

    # print(board)

def rule_2(board, neighbors, time):
    """
    Fungi Cellular growth

    If the current cell is fungi and is not full, grow in strength
    """

    if isinstance(neighbors['current'], FungiCell):

        new_cell = type(neighbors['current'])

        cur_cell = neighbors['current']
        if neighbors['current'].strength < 1:

            growth = 0
            for key, value in neighbors.items():
                if key != 'current':
                    if isinstance(value, FungiCell):
                        growth += value.strength/9

            new_time = cur_cell.time_born + 1

            # new_strength = neighbors['current'].strength + growth + cur_cell.get_total_growth()*new_time+neighbors['current'].avg_density*CELL_SIZE

            new_strength = neighbors['current'].strength + growth*cur_cell.wood_strength

            # print("new_strength: ", new_strength)

            # print("new_strength: ", new_strength)


            if new_strength >= 1:

                hyphal = new_cell(
                        cur_cell.row, cur_cell.col,1,
                        cur_cell.temperature,
                        cur_cell.moisture, wood_strength=cur_cell.wood_strength,
                        wood_growth=cur_cell.wood_growth
                    )

                hyphal.time_born = new_time

                # print("large hyphal: ", hyphal)


                # neighbors['current'].update_strength(1)
                board[cur_cell.row][cur_cell.col] = hyphal

            else:
                # print("new_strength: ", new_strength)
                hyphal = new_cell(
                        cur_cell.row, cur_cell.col, new_strength,
                        cur_cell.temperature,
                        cur_cell.moisture,
                        wood_strength=cur_cell.wood_strength,
                        wood_growth=cur_cell.wood_growth
                    )

                # print("small hyphal: ", hyphal)
                hyphal.time_born = new_time



                board[cur_cell.row][cur_cell.col] = hyphal


def rule_3(board, neighbors, time):
    """
    Fungal decomposition
    """

    pass

def rule_4(board, neighbors, time):
    """
    Wood decomposition
    """
    pass


def rule_5(board, neighbors, time):
    """
    Temperature decomposition
    """
    pass


def rule_6(board, neighbors, time):
    """
    Fungal attack
    """

    def win_lose(friend, enemy):
        """
        Returns true if wins
        """

        # print("friend: ", friend)
        # print("enemy: ", enemy)

        prob_win = 1/(1+10**((friend*2500 - enemy*2500)/400))
        # print("prob_win: ", prob_win)

        if random.random() <= prob_win:
            return True


    current_cell = neighbors['current']
    if isinstance(current_cell, FungiCell):

        for key, value in neighbors.items():
            if key != 'current' and isinstance(value, FungiCell) and not isinstance(value, type(current_cell)):
                enemy = value.comp_rank
                friend = current_cell.comp_rank

                win = win_lose(friend, enemy)

                if win:
                    dying = value.strength - current_cell.get_total_growth()*0.50
                    # print("dying: ", dying)
                    if dying <= 0:
                        value.strength = 0
                        new_cell = type(current_cell)
                        # new_cell()
                        hyphal = new_cell(
                            value.row, value.col, 0.25*value.strength,
                            value.temperature,
                            value.moisture, wood_strength=value.wood_strength,
                            wood_growth=value.wood_growth
                        )

                        board[value.row][value.col] = hyphal

                    else:
                        value.strength = dying


def rule_7(board, neighbors, time):
    """
    Fungal defense
    """
    pass
