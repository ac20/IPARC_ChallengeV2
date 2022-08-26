import numpy as np


def Process(img, num_colors=3, **param):
    """Converts a 2d image into to 3d image
    where each band corresponds to one colour.

    Note: Background is not considered a color.
    """
    n, m = img.shape
    img_cpy = np.zeros((n, m, num_colors))
    for color in range(0, num_colors):
        img_cpy[:, :, color] = (img == (color+1))*1
    return img_cpy


def Change_Colour(img, rule, *args):
    """
    The rule is a mapping {0,1}^k -> {0,1,2,...k}

    Implemented as n x (k+1) array where $k$ is the number of colors.

    -> row 'i' corresponds to rule 'i'.
    -> Each rule will be of the form  <0,1,0,1...,j>
    -> The last entry denotes the color to assign based on first 'k'
    entries.

    """
    if rule is None:
        m, n, no_colors = img.shape
        out_img = np.zeros((m, n), dtype=np.int32)
        for col in range(no_colors):
            out_img[img[:, :, col] == 1] = col + 1
        return out_img

    def func(arr, rule):
        ind = np.where(np.all(rule[:, :-1] == arr.reshape((1, -1)), axis=-1))[0]
        if len(ind) == 0:
            return 0
        elif len(ind) > 1:
            raise Exception("More than two Color_Change rules match the input")
        else:
            return rule[ind[0], -1]

    img = np.apply_along_axis(func, 2, img, rule)
    return img
