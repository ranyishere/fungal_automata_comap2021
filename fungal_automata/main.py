import random
import matplotlib.pyplot as plt
import  copy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import imageio
from tqdm import tqdm

from rules import *
from cells import *
from board import Board
from utils import *


# Max Search and Max Food (Greedy search in essence)
def apply_rules(board, neighbors, time):
    """
    Apply rules based on the neighbor
    """

    rule_2(board, neighbors, time)
    rule_1(board, neighbors, time)
    rule_6(board, neighbors, time)


def generate_board(width, height):
    """
    Generates the Board
    """

    board = []
    for row in range(height):
        cur_row = []
        for col in range(width):
            # cell_strength = random.random()
            cell_strength = random.uniform(0.0, 0.5)
            # cell_strength = 1
            # wood_cell = WoodCell(row=row, col=col, strength=cell_strength)
            wood_cell = Qalba(row=row, col=col, strength=cell_strength)
            cur_row.append(wood_cell)
        board.append(cur_row)

    return board

def generate_temp_gradient(width, height):
    """
    Generates temp gradient
    """

    board = []
    for row in range(height):
        cur_row = []

        # Row based gradient
        gradient = round(row/width, 2)

        for col in range(width):
            col_gradient = round(col/width, 2)

            temperature = 25*gradient+25*col_gradient

            # cell_strength = random.random()
            cell_strength = random.uniform(0.0, 1.0)
            # cell_strength = 1
            # wood_cell = WoodCell(row=row, col=col, strength=cell_strength)
            wood_cell = Qalba(row=row, col=col, strength=cell_strength, temperature=temperature)
            cur_row.append(wood_cell)

        board.append(cur_row)

    # get_heatmap_of_temp(board, debug=True)
    # exit()

    return board


def generate_moist_gradient(width, height):
    """
    Generates temp gradient
    """

    board = []
    for row in range(height):
        cur_row = []

        # Row based gradient
        gradient = round(row/width, 2)

        for col in range(width):
            col_gradient = round(col/width, 2)

            moisture = -2.5*gradient+-2.5*col_gradient

            # cell_strength = random.random()
            cell_strength = random.uniform(0.0, 1.0)
            # cell_strength = 1
            # wood_cell = WoodCell(row=row, col=col, strength=cell_strength)
            wood_cell = Qalba(row=row, col=col, strength=cell_strength, moisture=moisture)
            cur_row.append(wood_cell)

        board.append(cur_row)

    # get_heatmap_of_temp(board, debug=True)
    # exit()

    return board




def place_fungus(board, row, col, fungi_type):
    """
    Place Fungus
    """

    fungal_board = board
    fungal_board[row][col] = fungi_type(row, col, 1)


def place_food(board, row, col, radius, dist, strength):

    # print("col: ", col)
    # print("dist: ", dist)

    if row > len(board) or row < 0:
        return

    if col < 0 or col > len(board[row]):
        return

    if dist > radius:
        return

    if isinstance(board[row][col], FoodCell):
        return

    # print("row: ", row)
    # print("col: ", col)

    board[row][col] = FoodCell(row, col, strength)

    cur_row = row
    cur_col = col
    gradient = 1/radius

    neighbors = get_surroundings(board, cur_row, cur_col)

    for key, value in neighbors.items():
        if value != None and not isinstance(value, FungiCell):
            place_food(board, row+1, col, radius, dist+1, 1-dist*gradient)
            place_food(board, row-1, col, radius, dist+1, 1-dist*gradient)

            # place_food(board, row+1, col+1, radius, dist+1, 1-dist*gradient)
            # place_food(board, row-1, col-1, radius, dist+1, 1-dist*gradient)
            # place_food(board, row+1, col-1, radius, dist+1, 1-dist*gradient)
            # place_food(board, row-1, col+1, radius, dist+1, 1-dist*gradient)

            place_food(board, row, col+1, radius, dist+1, 1-dist*gradient)
            place_food(board, row, col-1, radius, dist+1, 1-dist*gradient)
            # print("dist: ", dist)
            # board[value.row][value.col] = WoodCell(value.row, value.col, dist*gradient)
    return

def mono_culture(fungi_1, fungi_2, file_dir, reference):
    """
    Main
    """

    trial_name = fungi_1.name+'_'+fungi_2.name+'_'+reference

    fig = plt.figure()

    WIDTH = 100
    HEIGHT = 100
    TIME = 30


    # cells = generate_board(WIDTH,HEIGHT)
    cells = generate_temp_gradient(WIDTH,HEIGHT)
    # cells = generate_moist_gradient(WIDTH, HEIGHT)
    # get_moistmap_of_food(cells, debug=True)

    # exit()

    # Fungi one
    # fungi_row = random.choice(range(HEIGHT))
    # fungi_col = random.choice(range(WIDTH))
    fungi_row = 50
    fungi_col = 50
    place_fungus(cells, fungi_row, fungi_col, fungi_1)

    # Fungi Two
    fungi_row = 70
    fungi_col = 70
    place_fungus(cells, fungi_row, fungi_col, fungi_2)

    # fungi_row = random.choice(range(HEIGHT))
    # fungi_col = random.choice(range(WIDTH))
    # place_fungus(cells, fungi_row, fungi_col, Prufa)
    # place food
    # place_food(cells, fungi_row+(HEIGHT-fungi_row)-5, fungi_col+(WIDTH-fungi_col)-5, fungi_row//10, 1, 1)

    RADIUS = WIDTH//10
    print("RADIUS: ", RADIUS)
    # place_food(cells, 10, 10, RADIUS, 1, 1)

    # place_food(cells, 50, 30, RADIUS+2, 1, 1)

    main_board = Board(cells)

    # img = get_image_from_state(cells, '-1', debug=True)

    # get_heatmap_of_temp(cells, debug=True)

    heat_data = get_heatmap_of_temp(main_board.state)
    heatmap = plt.imshow(heat_data, origin='lower', cmap='hot')
    plt.colorbar(heatmap)
    plt.title("heatmap_{0}".format(trial_name))
    plt.savefig(file_dir+'/heatmap_{0}.png'.format(trial_name))
    plt.clf()

    heat_data = get_moistmap(main_board.state)
    heatmap = plt.imshow(heat_data, origin='lower', cmap='Blues')
    plt.colorbar(heatmap)
    plt.title("moistmap_{0}".format(trial_name))
    plt.savefig(file_dir+'/moistmap_{0}.png'.format(trial_name))
    plt.clf()

    heat_data = get_heatmap_of_food(main_board.state)
    heatmap = plt.imshow(heat_data, origin='lower', cmap='hot')
    plt.colorbar(heatmap)
    plt.title("foodmap_{0}".format(trial_name))
    plt.savefig(file_dir+'/foodmap_{0}.png'.format(trial_name))
    plt.clf()



    # Moisture data

    # exit()
    # exit()

    # img = get_heatmap_of_food(cells)
    # plt.imshow(img, origin='lower', cmap='hot', interpolation='nearest')
    # plt.show()
    # plt.clf()
    
    time = 0
    file_names = []

    for i in tqdm(range(TIME)):
        temp_board = Board(main_board.state)
        # while tqdm(time) <= TIME:

        # new_cells = copy.deepcopy(board)
        for rix, row in enumerate(cells):

            # new_row_state = []
            for cix, col in enumerate(row):
                # Get surrounding for main board
                neighbors = get_surroundings(main_board.state, rix, cix)
                # Update the new temp board state
                apply_rules(temp_board.state, neighbors, time)
                # get_image_from_state(temp_board.state, neighbors, time)

            # new_cells.append(new_row_state)

        time += 1
        # Update main board to temp board
        main_board = temp_board

        img = get_image_from_state(main_board.state, time)
        plt.imshow(img, origin='lower', vmin=0)
        file_name = file_dir+'/images/{1}_test_{0}.png'.format(time,trial_name)
        file_names.append(file_name)
        plt.title("{1} time: {0}".format(time, trial_name))

        plt.savefig(file_name)
        plt.clf()

    data = []
    for fname in file_names:
        data.append(imageio.imread(fname))

    imageio.mimsave(file_dir+'/{0}_test_complete.gif'.format(trial_name), data, duration=1)

    
def main():
    """
    Main
    """

    types = ['mono_culture', 'multi_culture_norm', 'multi_culture_temp', 'multi_culture_moist', 'multi_culture_temp_moist']

    seen =[]

    fungi = [Pgilv, Xsub, Ppend, Mtrem, Tchion,Prufa]
    dirs = ['gilv', 'xsub', 'ppend', 'mtrem', 'tchion', 'prufa']
    dirs_1 = ['gilv', 'xsub', 'ppend', 'mtrem', 'tchion', 'prufa']

    # mono_culture(Pgilv, Xsub, 'fungi/'+'gilv', 'multi_culture_temp')

    names_ix_1 = 0
    for fungus_1 in tqdm(fungi):

        names_ix_1 += 1
        names_ix_2 = 0
        for fungus_2 in tqdm(fungi):

            current_duel = {dirs[names_ix_1], dirs_1[names_ix_2]}
            if fungus_1.name == fungus_2.name or current_duel in seen:
                continue

            else:
                mono_culture(fungus_1, fungus_2, 'fungi/'+dirs[names_ix_1], 'multi_culture_temp')
                names_ix_2 += 1
                seen.append(current_duel)


if __name__ == '__main__':
    main()
