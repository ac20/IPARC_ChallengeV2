import os
import numpy as np
import json
import pdb
from matplotlib import pyplot as plt

# from skimage.morphology import binary_dilation, binary_erosion
from scipy.ndimage import binary_dilation, binary_erosion, binary_hit_or_miss
import random

from ListSelEm import *
from Utils import Process, Change_Colour


def generate_inp_out_catB_Selection(list_se, **param):
    """
    SE0/SE1 - Hit-Or-Miss
    SE2/3 - Dilate (SE0)
    SE2/3 - Erode (SE0)
    SE4/5 - Dilate (SE1)
    SE4/5 - Erode (SE1)
    """

    sz = np.random.randint(2, 4)

    # Select 1/2 pixels and dilate by SE0
    base_img1 = np.zeros((param['img_size'], param['img_size']), dtype=np.int32)
    idx1 = np.random.randint(0, param['img_size']//2, size=sz)
    idx2 = np.random.randint(0, param['img_size']//2, size=sz)
    base_img1[idx1, idx2] = 1
    base_img1 = binary_dilation(base_img1, list_se_3x3[list_se[0]])

    # Select 1/2 pixels and dilate by SE1
    base_img2 = np.zeros((param['img_size'], param['img_size']), dtype=np.int32)
    idx1 = np.random.randint(param['img_size']//2, param['img_size'], size=sz)
    idx2 = np.random.randint(param['img_size']//2, param['img_size'], size=sz)
    base_img2[idx1, idx2] = 1
    base_img2 = binary_dilation(base_img2, list_se_3x3[list_se[1]])

    # Combine the above images to get the base image.
    base_img = np.logical_or(base_img1, base_img2)*1

    # Copy the base_img for input/output
    inp_img = np.array(base_img*1, copy=True)
    out_img = np.array(base_img*1, copy=True)

    # Next we have a hit_or_miss which selects a pixel and adds another color
    tmp_img = binary_hit_or_miss(out_img, list_se_3x3[list_se[0]])
    out_img[tmp_img] = 2  # Add another color
    out_img = Process(out_img, num_colors=2)

    # First color will be processed differently
    out_img[:, :, 0] = binary_dilation(out_img[:, :, 0], list_se_3x3[list_se[2]])
    out_img[:, :, 0] = binary_dilation(out_img[:, :, 0], list_se_3x3[list_se[3]])
    out_img[:, :, 0] = binary_erosion(out_img[:, :, 0], list_se_3x3[list_se[2]])
    out_img[:, :, 0] = binary_erosion(out_img[:, :, 0], list_se_3x3[list_se[3]])

    # Second color will be processed differently
    out_img[:, :, 1] = binary_dilation(out_img[:, :, 1], list_se_3x3[list_se[0]])
    out_img[:, :, 1] = binary_dilation(out_img[:, :, 1], list_se_3x3[list_se[4]])
    out_img[:, :, 1] = binary_dilation(out_img[:, :, 1], list_se_3x3[list_se[5]])
    out_img[:, :, 1] = binary_erosion(out_img[:, :, 1], list_se_3x3[list_se[4]])
    out_img[:, :, 1] = binary_erosion(out_img[:, :, 1], list_se_3x3[list_se[5]])

    # Resolve the color by the rule
    rule = np.array([[0, 0, 0], [0, 1, 2], [1, 0, 1], [1, 1, 2]], dtype=np.int32)
    out_img = Change_Colour(out_img, rule)
    return inp_img, out_img


def generate_one_task_CatB_Selection(**param):
    """
    """
    k_example = 0
    list_se_idx = np.random.randint(0, 8, size=6)
    data = []
    while k_example < param['no_examples_per_task']:
        inp_img, out_img = generate_inp_out_catB_Selection(list_se_idx, **param)

        # Check if both input and output images are non-trivial
        FLAG = False
        if np.all(inp_img*1 == 1) or np.all(inp_img*1 == 0):
            FLAG = True
        elif np.all(out_img*1 == 1) or np.all(out_img*1 == 0):
            FLAG = True

        if FLAG:
            # If trivial regenerate the list of se's
            # And reset all variables!!
            data = []
            list_se_idx = np.random.randint(0, 8, size=6)
            k_example = -1
        else:
            data.append((inp_img, out_img))

        # Increment k_example
        k_example += 1

    return data, list_se_idx


def write_dict_json_CatB_Selection(data, fname):
    """
    """
    dict_data = []
    for (inp, out) in data:
        inp = [[int(y) for y in x] for x in inp]
        out = [[int(y) for y in x] for x in out]
        dict_data.append({"input": inp, "output": out})

    with open(fname, "w") as f:
        f.write(json.dumps(dict_data))


def write_solution_CatB_Selection(list_se_idx, fname):
    """
    """
    color_rule = np.array([[0, 0, 0], [0, 1, 2], [1, 0, 1], [1, 1, 2]], dtype=np.int32)
    with open(fname, 'w') as f:
        f.write("Hit-Or-Miss SE{} \n".format(list_se_idx[0]))
        f.write("Band 1 - Dilation SE{} \n".format(list_se_idx[2]+1))
        f.write("Band 1 - Dilation SE{} \n".format(list_se_idx[3]+1))
        f.write("Band 1 - Erosion SE{} \n".format(list_se_idx[2]+1))
        f.write("Band 1 - Erosion SE{} \n".format(list_se_idx[3]+1))
        f.write("Band 2 - Dilation SE{} \n".format(list_se_idx[0]+1))
        f.write("Band 2 - Dilation SE{} \n".format(list_se_idx[4]+1))
        f.write("Band 2 - Dilation SE{} \n".format(list_se_idx[5]+1))
        f.write("Band 2 - Erosion SE{} \n".format(list_se_idx[4]+1))
        f.write("Band 2 - Erosion SE{} \n".format(list_se_idx[5]+1))
        f.write("Color rule : {}".format(json.dumps([[int(y) for y in x] for x in color_rule])))
        f.write("\n")


def write_solution_CatB_Selection_json(list_se_idx, fname):
    """
    """
    color_rule = np.array([[0, 0, 0], [0, 1, 2], [1, 0, 1], [1, 1, 2]], dtype=np.int32)
    data = []
    data.append((None, "Hit-Or-Miss", "SE{}".format(list_se_idx[0]+1)))
    data.append((1, "Dilation", "SE{}".format(list_se_idx[2]+1)))
    data.append((1, "Dilation", "SE{}".format(list_se_idx[3]+1)))
    data.append((1, "Erosion", "SE{}".format(list_se_idx[2]+1)))
    data.append((1, "Erosion", "SE{}".format(list_se_idx[3]+1)))
    data.append((2, "Dilation", "SE{}".format(list_se_idx[0]+1)))
    data.append((2, "Dilation", "SE{}".format(list_se_idx[4]+1)))
    data.append((2, "Dilation", "SE{}".format(list_se_idx[5]+1)))
    data.append((2, "Erosion", "SE{}".format(list_se_idx[4]+1)))
    data.append((2, "Erosion", "SE{}".format(list_se_idx[5]+1)))
    data.append((None, "change_color", [[int(y) for y in x] for x in color_rule]))

    with open(fname, "w") as f:
        f.write(json.dumps(data))


def generate_100_tasks_CatB_Selection(seed, **param):
    """
    """
    np.random.seed(seed)
    os.makedirs("./Dataset/CatB_Selection", exist_ok=True)
    for task_no in range(100):
        data, list_se_idx = generate_one_task_CatB_Selection(**param)
        fname = './Dataset/CatB_Selection/Task{:03d}.json'.format(task_no)
        write_dict_json_CatB_Selection(data, fname)

        fname = './Dataset/CatB_Selection/Task{:03d}_soln.txt'.format(task_no)
        write_solution_CatB_Selection(list_se_idx, fname)

        fname = './Dataset/CatB_Selection/Task{:03d}_soln.json'.format(task_no)
        write_solution_CatB_Selection_json(list_se_idx, fname)


if __name__ == "__main__":
    param = {}
    param['img_size'] = 15
    param['se_size'] = 3  # Size of the structuring element
    param['seq_length'] = 4  # Number of primitives would be 2*param['seq_length']
    param['no_examples_per_task'] = 4
    param['no_colors'] = 3

    generate_100_tasks_CatB_Selection(32, **param)
