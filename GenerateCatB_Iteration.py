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


def generate_inp_out_catB_Iteration(list_se_idx, k_iterate, **param):
    """
    """
    base_img = np.zeros((param['img_size'], param['img_size']), dtype=np.int32)
    sz = np.random.randint(3, 6)
    idx1 = np.random.randint(0, param['img_size'], size=sz)
    idx2 = np.random.randint(0, param['img_size'], size=sz)
    base_img[idx1, idx2] = 1

    for _ in range(2):
        idx = np.random.randint(0, 8)
        base_img = binary_dilation(base_img, list_se_3x3[idx])

    inp_img = np.array(base_img, copy=True)
    out_img = np.array(base_img, copy=True)

    for idx in range(2):
        out_img = binary_dilation(out_img, list_se_3x3[list_se_idx[idx]])

    for idx in range(2):
        out_img = binary_erosion(out_img, list_se_3x3[list_se_idx[idx]])

    for idx in range(k_iterate):
        out_img = binary_dilation(out_img, list_se_3x3[list_se_idx[-1]])

    for idx in range(k_iterate):
        out_img = binary_erosion(out_img, list_se_3x3[list_se_idx[-1]])

    return inp_img, out_img


def generate_one_task_CatB_Iteration(**param):
    """
    """
    number_subtasks = 3
    list_se_idx = np.random.randint(0, 8, 3)
    k_iterate = np.random.randint(2, 5)

    data_tot = []
    list_se_tot = []
    k_subtask = 0
    while k_subtask < number_subtasks:
        data_subtask = []
        k_example = 0
        list_se_subtask = np.array(list_se_idx, copy=True)
        for idx in [0, 1]:
            idx_tmp = np.random.randint(0, 8)
            list_se_subtask[idx] = idx_tmp

        while k_example < param['no_examples_per_task']:
            inp_img, out_img = generate_inp_out_catB_Iteration(list_se_subtask, k_iterate, **param)

            # Check if both input and output images are non-trivial
            FLAG = False
            if np.all(inp_img*1 == 1) or np.all(inp_img*1 == 0):
                FLAG = True
            elif np.all(out_img*1 == 1) or np.all(out_img*1 == 0):
                FLAG = True

            if FLAG:
                # If trivial regenerate the list of se's
                # And reset all variables!!
                data_subtask = []
                k_example = -1
                list_se_subtask = np.array(list_se_idx, copy=True)
                for idx in [0, 1]:
                    idx_tmp = np.random.randint(0, 8)
                    list_se_subtask[idx] = idx_tmp
            else:
                # If not trivial proceed.
                data_subtask.append((inp_img, out_img, k_subtask))
            k_example += 1

        data_tot += data_subtask
        list_se_tot.append(list_se_subtask)
        k_subtask += 1

    return data_tot, list_se_tot, k_iterate


def write_dict_json_CatB_Iteration(data, fname):
    """
    """
    dict_data = []
    for (inp, out, subtask) in data:
        inp = [[int(y) for y in x] for x in inp]
        out = [[int(y) for y in x] for x in out]
        dict_data.append({"input": inp, "output": out, "subtask": subtask})

    with open(fname, "w") as f:
        f.write(json.dumps(dict_data))


def write_solution_CatB_Iteration(list_se_idx, k_iterate, fname):
    """
    """
    with open(fname, 'w') as f:
        for list_se_idx_subtask in list_se_idx:
            f.write("Subtask \n")
            f.write("-------- \n")
            i = 0
            while i < 2:
                f.write("Dilation SE{}\n".format(list_se_idx_subtask[i]+1))
                i += 1
            i = 0
            while i < 2:
                f.write(" Erosion SE{}\n".format(list_se_idx_subtask[i]+1))
                i += 1
            i = 2
            f.write("Iterate {} Dilation SE{}\n".format(k_iterate, list_se_idx_subtask[i]+1))
            f.write("Iterate {}  Erosion SE{}\n".format(k_iterate, list_se_idx_subtask[i]+1))
            f.write("\n")


def write_solution_CatB_Iteration_json(list_se_idx, k_iterate, fname):
    """
    Solution written in format:
    subtask - 
    n_iterate -
    op - Dilation/Erosion/Color_Change
    SE = SE0-SE7
    """
    data = []
    subtask = 0
    for list_se_idx_subtask in list_se_idx:
        i = 0
        while i < 2:
            data.append((subtask, 1, 'Dilation', 'SE{}'.format(list_se_idx_subtask[i]+1)))
            i += 1
        i = 0
        while i < 2:
            data.append((subtask, 1, 'Erosion', 'SE{}'.format(list_se_idx_subtask[i]+1)))
            i += 1
        data.append((subtask, k_iterate, 'Dilation', 'SE{}'.format(list_se_idx_subtask[i]+1)))
        data.append((subtask, k_iterate, 'Erosion', 'SE{}'.format(list_se_idx_subtask[i]+1)))
        subtask += 1

    with open(fname, "w") as f:
        f.write(json.dumps(data))


def generate_100_tasks_CatB_Iteration(seed, **param):
    """
    """
    np.random.seed(seed)

    os.makedirs("./Dataset/CatB_Iteration", exist_ok=True)

    for task_no in range(100):
        data, list_se_idx, k_iterate = generate_one_task_CatB_Iteration(**param)
        fname = './Dataset/CatB_Iteration/Task{:03d}.json'.format(task_no)
        write_dict_json_CatB_Iteration(data, fname)

        fname = './Dataset/CatB_Iteration/Task{:03d}_soln.txt'.format(task_no)
        write_solution_CatB_Iteration(list_se_idx, k_iterate, fname)

        fname = './Dataset/CatB_Iteration/Task{:03d}_soln.json'.format(task_no)
        write_solution_CatB_Iteration_json(list_se_idx, k_iterate, fname)


if __name__ == "__main__":
    param = {}
    param['img_size'] = 15
    param['se_size'] = 5  # Size of the structuring element
    param['seq_length'] = 4  # Number of primitives would be 2*param['seq_length']
    param['no_examples_per_task'] = 4
    param['no_colors'] = 3

    generate_100_tasks_CatB_Iteration(32, **param)
