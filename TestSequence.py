#!/usr/bin/python

"""
Possible shell commands

Dilation SEx
Erosion SEx
Hit-Or-Miss SEx
ChangeColor [[a1,a2,a3],[b1,b2,b3]]

Example 
fname.json band-Dilation-SE1-iterate band-Erosion-SE2-iterate band-HitorMiss-SE2-iterate band-ChangeColor-[[a1,a2,a3],[b1,b2,b3]]-iterate

./Dataset/CatB_Hard/Task000.json 1-HitOrMiss-SE8-1 1-Dilation-SE6-2 1-Erosion-SE6-2  2-Dilation-SE8-1 2-Dilation-SE7-1 2-Dilation-SE5-1 2-Dilation-SE7-1 2-Erosion-SE7-1 2-Erosion-SE5-1 2-Erosion-SE7-1 1-ChangeColor-[[0,0,0],[0,1,2],[1,0,1],[1,1,2]]-1

will check if the given sequence satisfies the tasks in <fname>.json

"""

import os.path
import sys
import numpy as np
import json
import pdb
from matplotlib import pyplot as plt
import os
from ast import literal_eval

# from skimage.morphology import binary_dilation, binary_erosion
from scipy.ndimage.morphology import binary_dilation, binary_erosion, binary_hit_or_miss
import random

from ListSelEm import *
from Utils import Process, Change_Colour


def perform_op(fname, list_ops):
    def _perform_task(img, k_iterate, op, se):
        for _ in range(k_iterate):
            list_se = ['SE1', 'SE2', 'SE3', 'SE4', 'SE5', 'SE6', 'SE7', 'SE8']
            if op == 'Dilation':
                list_se_idx = list_se.index(se)
                img = binary_dilation(img, list_se_3x3[list_se_idx])
            elif op == 'Erosion':
                list_se_idx = list_se.index(se)
                img = binary_erosion(img, list_se_3x3[list_se_idx])
            elif op == 'HitOrMiss':
                list_se_idx = list_se.index(se)
                tmp_img = binary_hit_or_miss(img, list_se_3x3[list_se_idx])
                img[tmp_img] = 2  # Add another color
                img = Process(img, num_colors=2)
            elif op == 'ChangeColor':
                img = Change_Colour(img, np.array(se, dtype=np.int32))
        return img

    # Load the dataset.
    with open(fname, 'r') as f:
        data = json.load(f)

    for d in data:
        img = np.array(d['input'], dtype=np.int32)
        if len(img.shape) == 2:
            sx, sy = img.shape
            img = img.reshape((sx, sy, 1))
        for band, k_iterate, op, se in list_ops:
            if op != 'HitOrMiss' and op != 'ChangeColor':
                img[:, :, band-1] = _perform_task(img[:, :, band-1], k_iterate, op, se)
            elif op == 'HitOrMiss':
                img = _perform_task(img[:, :, band-1], k_iterate, op, se)
            else:
                img = _perform_task(img, k_iterate, op, se)
        img = img*1
        out = np.array(d['output'], dtype=np.int32)
        check_same = np.all(img == out)
        if check_same:
            print("Program works!!")
        else:
            print("Something went wrong!!")


if __name__ == '__main__':
    fname = sys.argv[1]
    list_ops = []
    for arg in sys.argv[2:]:
        band, op, se, k_iterate = str(arg).split("-")
        band = int(band)
        k_iterate = int(k_iterate)
        if op == 'ChangeColor':
            se = np.array(literal_eval(se))
        list_ops.append((band, k_iterate, op, se))

    perform_op(fname, list_ops)
