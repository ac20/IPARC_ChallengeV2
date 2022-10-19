import numpy as np
import json
import pdb
from matplotlib import pyplot as plt
import os

# from skimage.morphology import binary_dilation, binary_erosion
from scipy.ndimage import binary_dilation, binary_erosion, binary_hit_or_miss
import random

from ListSelEm import *
from Utils import Process, Change_Colour


def generate_color_change_rule(no_colors):
    """
    """
    arr = np.zeros((2**no_colors, no_colors+1), dtype=np.int32)
    for i in range(2**no_colors):
        str_binary = ("0"*no_colors + bin(i)[2:])[-no_colors:]
        arr[i, :-1] = np.array([int(x) for x in str_binary])
    arr[:, -1] = np.random.randint(1, no_colors+1, 2**no_colors)
    arr[0, -1] = 0
    return arr


def generate_inp_out_catA_Hard(list_se_idx, color_rule, **param):
    """
    """
    base_img = np.zeros((param['img_size'], param['img_size']), dtype=np.int32)
    sz = np.random.randint(2, 4)
    for color in range(1, param['no_colors']+1):
        idx1 = np.random.randint(0, param['img_size'], size=sz)
        idx2 = np.random.randint(0, param['img_size'], size=sz)
        base_img[idx1, idx2] = color

    # Process the base image to make it random!
    base_img = Process(base_img, num_colors=param['no_colors'])
    for color in range(param['no_colors']):
        idx = np.random.randint(0, 8)
        base_img[:, :, color] = binary_dilation(base_img[:, :, color], list_se_3x3[idx])
    base_img = Change_Colour(base_img, rule=None)  # Default color change!

    inp_img = np.array(base_img, copy=True)
    out_img = np.array(base_img, copy=True)
    out_img = Process(out_img, num_colors=param['no_colors'])

    for (color, list_se_color) in zip(range(0, param['no_colors']), list_se_idx):
        for idx in list_se_color:
            out_img[:, :, color] = binary_dilation(out_img[:, :, color], list_se_3x3[idx])

    for (color, list_se_color) in zip(range(0, param['no_colors']), list_se_idx):
        for idx in list_se_color:
            out_img[:, :, color] = binary_erosion(out_img[:, :, color], list_se_3x3[idx])

    out_img = Change_Colour(out_img, color_rule)

    return inp_img, out_img


def generate_one_task_CatA_Hard(**param):
    """
    """
    list_se_idx = []
    for _ in range(param['no_colors']):
        list_se_idx.append(np.random.randint(0, 8, 4))

    color_rule = generate_color_change_rule(param['no_colors'])

    data = []
    k = 0
    while k < param['no_examples_per_task']:
        inp_img, out_img = generate_inp_out_catA_Hard(list_se_idx, color_rule, **param)

        # Check if both input and output images are non-trivial
        FLAG = False

        for col in range(param['no_colors']+1):
            if np.all(inp_img == col):
                FLAG = True
            if np.all(out_img == col):
                FLAG = True

        if FLAG:
            # If trivial, reset all data points!
            list_se_idx = []
            for _ in range(param['no_colors']):
                list_se_idx.append(np.random.randint(0, 8, 4))

            color_rule = generate_color_change_rule(param['no_colors'])
            data = []
            k = -1
        else:
            # If not trivial proceed.
            data.append((inp_img, out_img))
        k += 1

    return data, list_se_idx, color_rule


def write_dict_json_CatA_Hard(data, fname):
    """
    """
    dict_data = []
    for (inp, out) in data:
        inp = [[int(y) for y in x] for x in inp]
        out = [[int(y) for y in x] for x in out]
        dict_data.append({"input": inp, "output": out})

    with open(fname, "w") as f:
        f.write(json.dumps(dict_data))


def write_solution_CatA_Hard(list_se_idx, color_rule, fname):
    """
    """
    with open(fname, 'w') as f:
        band = 1
        for list_se_color in list_se_idx:
            f.write("Sequence for Band {}\n".format(band))
            f.write("---------------------- \n")
            for idx in list_se_color:
                f.write("Dilation SE{}\n".format(idx+1))
            for idx in list_se_color:
                f.write("Erosion SE{}\n".format(idx+1))

            band += 1

            f.write("\n")

        f.write("\n Color Change Rule \n")
        f.write("------------------\n")
        f.write(json.dumps([[int(y) for y in x] for x in color_rule]))


def write_solution_CatA_Hard_json(list_se_idx, color_rule, fname):
    """
    Solution written in format:
    band - 1/2/3/None
    op - Dilation/Erosion/Color_Change
    SE = SE0-SE7
    """
    data = []
    band = 1
    for list_se_color in list_se_idx:
        for idx in list_se_color:
            data.append((band, 'Dilation', 'SE{}'.format(idx+1)))
        for idx in list_se_color:
            data.append((band, 'Erosion', 'SE{}'.format(idx+1)))
        band += 1

    data.append((None, 'color_rule', (([[int(y) for y in x] for x in color_rule]))))
    with open(fname, "w") as f:
        f.write(json.dumps(data))


def generate_100_tasks_CatA_Hard(seed, **param):
    """
    """
    np.random.seed(seed)
    os.makedirs("./Dataset/CatA_Hard", exist_ok=True)
    for task_no in range(100):
        data, list_se_idx, color_rule = generate_one_task_CatA_Hard(**param)
        fname = './Dataset/CatA_Hard/Task{:03d}.json'.format(task_no)
        write_dict_json_CatA_Hard(data, fname)

        fname = './Dataset/CatA_Hard/Task{:03d}_soln.txt'.format(task_no)
        write_solution_CatA_Hard(list_se_idx, color_rule, fname)

        fname = './Dataset/CatA_Hard/Task{:03d}_soln.json'.format(task_no)
        write_solution_CatA_Hard_json(list_se_idx, color_rule, fname)


if __name__ == "__main__":
    param = {}
    param['img_size'] = 15
    param['se_size'] = 5  # Size of the structuring element
    param['seq_length'] = 4  # Number of primitives would be 2*param['seq_length']
    param['no_examples_per_task'] = 4
    param['no_colors'] = 3

    generate_100_tasks_CatA_Hard(32, **param)
