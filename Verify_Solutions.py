import numpy as np
import json
import pdb
from matplotlib import pyplot as plt
import os

# from skimage.morphology import binary_dilation, binary_erosion
from scipy.ndimage.morphology import binary_dilation, binary_erosion, binary_hit_or_miss
import random

from ListSelEm import *
from Utils import Process, Change_Colour


"""
Example program for Category A Simple
"""

print("--------------------------")
print("------ CAT A SIMPLE ------")
print("--------------------------")


def _perform_CatA_Simple(img, op, se):
    list_se = ['SE1', 'SE2', 'SE3', 'SE4', 'SE5', 'SE6', 'SE7', 'SE8']
    list_se_idx = list_se.index(se)
    if op == 'Dilation':
        return binary_dilation(img, list_se_3x3[list_se_idx])
    elif op == 'Erosion':
        return binary_erosion(img, list_se_3x3[list_se_idx])


idx_select = np.random.randint(100)  # Example Number

# Load the dataset.
with open("./Dataset/CatA_Simple/Task{:03d}.json".format(idx_select), 'r') as f:
    data = json.load(f)

# Load the solution.
with open("./Dataset/CatA_Simple/Task{:03d}_soln.txt".format(idx_select), 'r') as f:
    list_ops = f.readlines()
list_ops = [x.split() for x in list_ops]

for d in data:
    img = np.array(d['input'], dtype=np.int32)
    for op, se in list_ops:
        img = _perform_CatA_Simple(img, op, se)
    img = img*1

    out = np.array(d['output'], dtype=np.int32)
    check_same = np.all(img == out)
    if check_same:
        print("Program works!!")
    else:
        print("Something went wrong!!")


"""
Example program for Category A Hard
"""

print("--------------------------")
print("------- CAT A HARD -------")
print("--------------------------")


def _perform_CatA_Hard(img, band, op, se):
    if band is not None:
        list_se = ['SE1', 'SE2', 'SE3', 'SE4', 'SE5', 'SE6', 'SE7', 'SE8']
        list_se_idx = list_se.index(se)
        if op == 'Dilation':
            return binary_dilation(img, list_se_3x3[list_se_idx])
        elif op == 'Erosion':
            return binary_erosion(img, list_se_3x3[list_se_idx])

    else:
        return Change_Colour(img, np.array(se, dtype=np.int32))


idx_select = np.random.randint(100)  # Example Number

# Load the dataset.
with open("./Dataset/CatA_Hard/Task{:03d}.json".format(idx_select), 'r') as f:
    data = json.load(f)

# Load the Solution.
with open("./Dataset/CatA_Hard/Task{:03d}_soln.json".format(idx_select), 'r') as f:
    list_ops = json.load(f)

for d in data:
    img = np.array(d['input'], dtype=np.int32)
    img = Process(img, num_colors=3)
    for band, op, se in list_ops:
        if band is not None:
            img[:, :, band-1] = _perform_CatA_Hard(img[:, :, band-1], band, op, se)
        else:
            img = _perform_CatA_Hard(img, band, op, se)
    img = img*1

    out = np.array(d['output'], dtype=np.int32)
    check_same = np.all(img == out)
    if check_same:
        print("Program works!!")
    else:
        print("Something went wrong!!")

"""
Example program for Category B Iteration
"""

print("---------------------------")
print("------ CAT B ITERATE ------")
print("---------------------------")


def _perform_CatB_Iteration(img, n_iterate, op, se):
    for _ in range(n_iterate):
        list_se = ['SE1', 'SE2', 'SE3', 'SE4', 'SE5', 'SE6', 'SE7', 'SE8']
        list_se_idx = list_se.index(se)
        if op == 'Dilation':
            img = binary_dilation(img, list_se_3x3[list_se_idx])
        elif op == 'Erosion':
            img = binary_erosion(img, list_se_3x3[list_se_idx])
    return img


# Load the dataset.
idx_select = 0
with open("./Dataset/CatB_Iteration/Task{:03d}.json".format(idx_select), 'r') as f:
    data = json.load(f)

# Load the Solution.
with open("./Dataset/CatB_Iteration/Task{:03d}_soln.json".format(idx_select), 'r') as f:
    list_ops = json.load(f)

for d in data:
    img = np.array(d['input'], dtype=np.int32)
    for subtask, n_iterate, op, se in list_ops:
        if d['subtask'] == subtask:
            img = _perform_CatB_Iteration(img, n_iterate, op, se)
    img = img*1

    out = np.array(d['output'], dtype=np.int32)
    check_same = np.all(img == out)
    if check_same:
        print("Program works!!")
    else:
        print("Something went wrong!!")

"""
Example program for Category B Sequence
"""

print("---------------------------")
print("------ CAT B Sequence ------")
print("---------------------------")


def _perform_CatB_sequence(img, op, se):
    list_se = ['SE1', 'SE2', 'SE3', 'SE4', 'SE5', 'SE6', 'SE7', 'SE8']
    list_se_idx = list_se.index(se)
    if op == 'Dilation':
        img = binary_dilation(img, list_se_3x3[list_se_idx])
    elif op == 'Erosion':
        img = binary_erosion(img, list_se_3x3[list_se_idx])

    return img


# Load the dataset.
idx_select = 0
with open("./Dataset/CatB_Sequence/Task{:03d}.json".format(idx_select), 'r') as f:
    data = json.load(f)

# Load the Solution.
with open("./Dataset/CatB_Sequence/Task{:03d}_soln.json".format(idx_select), 'r') as f:
    list_ops = json.load(f)

for d in data:
    img = np.array(d['input'], dtype=np.int32)
    for subtask, op, se in list_ops:
        if d['subtask'] == subtask:
            img = _perform_CatB_sequence(img, op, se)
    img = img*1

    out = np.array(d['output'], dtype=np.int32)
    check_same = np.all(img == out)
    if check_same:
        print("Program works!!")
    else:
        print("Something went wrong!!")


"""
Example program for Category B Selection
"""

print("-----------------------------")
print("------ CAT B Selection ------")
print("-----------------------------")


def _perform_CatB_selection(img, op, se):
    list_se = ['SE1', 'SE2', 'SE3', 'SE4', 'SE5', 'SE6', 'SE7', 'SE8']
    if op == 'Dilation':
        list_se_idx = list_se.index(se)
        img = binary_dilation(img, list_se_3x3[list_se_idx])
    elif op == 'Erosion':
        list_se_idx = list_se.index(se)
        img = binary_erosion(img, list_se_3x3[list_se_idx])
    elif op == 'Hit-Or-Miss':
        list_se_idx = list_se.index(se)
        tmp_img = binary_hit_or_miss(img, list_se_3x3[list_se_idx])
        img[tmp_img] = 2  # Add another color
        img = Process(img, num_colors=2)
    elif op == 'change_color':
        img = Change_Colour(img, np.array(se, dtype=np.int32))
    return img


# Load the dataset.
with open("./Dataset/CatB_Selection/Task{:03d}.json".format(idx_select), 'r') as f:
    data = json.load(f)

# Load the Solution.
with open("./Dataset/CatB_Selection/Task{:03d}_soln.json".format(idx_select), 'r') as f:
    list_ops = json.load(f)

for d in data:
    img = np.array(d['input'], dtype=np.int32)
    for band, op, se in list_ops:
        if band is not None:
            img[:, :, band-1] = _perform_CatB_selection(img[:, :, band-1], op, se)
        else:
            img = _perform_CatB_selection(img, op, se)
    img = img*1
    out = np.array(d['output'], dtype=np.int32)
    check_same = np.all(img == out)
    if check_same:
        print("Program works!!")
    else:
        print("Something went wrong!!")


"""
Example program for Category B Hard
"""

print("-----------------------------")
print("------ CAT B Hard ------")
print("-----------------------------")


def _perform_CatB_hard(img, k_iterate, op, se):
    for _ in range(k_iterate):
        list_se = ['SE1', 'SE2', 'SE3', 'SE4', 'SE5', 'SE6', 'SE7', 'SE8']
        if op == 'Dilation':
            list_se_idx = list_se.index(se)
            img = binary_dilation(img, list_se_3x3[list_se_idx])
        elif op == 'Erosion':
            list_se_idx = list_se.index(se)
            img = binary_erosion(img, list_se_3x3[list_se_idx])
        elif op == 'Hit-Or-Miss':
            list_se_idx = list_se.index(se)
            tmp_img = binary_hit_or_miss(img, list_se_3x3[list_se_idx])
            img[tmp_img] = 2  # Add another color
            img = Process(img, num_colors=2)
        elif op == 'change_color':
            img = Change_Colour(img, np.array(se, dtype=np.int32))
    return img


# Load the dataset.
with open("./Dataset/CatB_Hard/Task{:03d}.json".format(idx_select), 'r') as f:
    data = json.load(f)

# Load the Solution.
with open("./Dataset/CatB_Hard/Task{:03d}_soln.json".format(idx_select), 'r') as f:
    list_ops = json.load(f)

for d in data:
    img = np.array(d['input'], dtype=np.int32)
    for band, k_iterate, op, se in list_ops:
        if band is not None:
            img[:, :, band-1] = _perform_CatB_hard(img[:, :, band-1], k_iterate, op, se)
        else:
            img = _perform_CatB_hard(img, k_iterate, op, se)
    img = img*1
    out = np.array(d['output'], dtype=np.int32)
    check_same = np.all(img == out)
    if check_same:
        print("Program works!!")
    else:
        print("Something went wrong!!")
