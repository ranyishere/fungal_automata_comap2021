import random
import pprint
import matplotlib.pyplot as plt
import numpy as np
from cells import *

pp = pprint.PrettyPrinter(indent=2)

random.seed(5)

def get_image_from_state(cells, time, debug=False):
    """
    Generates an image from the cell states
    """

    # print("time: ", time)

    img = []
    for rix, row in enumerate(cells):
        img_row = []
        for cix, col in enumerate(row):

            img_row.append(col.color)

        img.append(img_row)


    if debug == True:

        plt.imshow(np.array(img), origin='lower')
        plt.show()

    return img

def get_heatmap_of_temp(cells, optimal=31.5, debug=False):

    img = []
    optimal_pts = []
    for rix, row in enumerate(cells):
        img_row = []
        for cix, col in enumerate(row):

            # if rix == 2 and cix == 4:
            # print("rix: {0} cix: {1}".format(rix, cix))
            # print(col.color)
            # if col.temperature <= optimal+0.1 and col.temperature >= optimal-0.1:
                # print("col.temperature: ", col.temperature)
                # optimal_pts.append([rix,cix])

            img_row.append(col.temperature)
            # img_row.append(col.color[3])

        img.append(img_row)
        # print("img: ", img)

    if debug == True:

        for opt in optimal_pts:
            plt.plot(opt, marker='x')

        heatmap = plt.imshow(np.array(img), origin='lower', cmap='hot')
        plt.colorbar(heatmap)
        plt.show()
        print("showing")

    return img

def get_heatmap_of_food(cells, debug=False):

    img = []
    for rix, row in enumerate(cells):
        img_row = []
        for cix, col in enumerate(row):
            # if rix == 2 and cix == 4:
            # print("rix: {0} cix: {1}".format(rix, cix))
            # print(col.color)
            img_row.append(col.color[3])
            # img_row.append(col.color[3])

        img.append(img_row)

    if debug == True:

        plt.imshow(np.array(img), origin='lower')
        plt.show()

    return img

def get_moistmap(cells, debug=False):

    img = []
    for rix, row in enumerate(cells):
        img_row = []
        for cix, col in enumerate(row):
            # if rix == 2 and cix == 4:
            # print("rix: {0} cix: {1}".format(rix, cix))
            # print(col.color)
            img_row.append(col.moisture)
            # img_row.append(col.color[3])

        img.append(img_row)

    if debug == True:

        plt.imshow(np.array(img), origin='lower', cmap='Blues')
        plt.show()

    return img
