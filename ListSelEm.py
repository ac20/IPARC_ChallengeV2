"""
Here we define the structuring elements which are used to generate the tasks.

To make it more "ARC"-like, we have used some well known human understandable
patterns. 

We define two sizes of structuring elements - 3x3 and 5x5.

List: 
Disk, Square(filled), cross, plus, rhombus, square(empty), line-to-right
line-to-left, line-to-top, line-to-bottom.

"""

import numpy as np
from skimage.morphology import disk

# Square
SE1_3x3 = np.ones((3, 3), dtype=np.int32)
SE1_5x5 = np.ones((5, 5), dtype=np.int32)

# Disk
SE2_3x3 = np.array(disk(1), dtype=np.int32)
SE2_5x5 = np.array(disk(2), dtype=np.int32)

# Cross
SE3_3x3 = np.zeros((3, 3), dtype=np.int32)
SE3_3x3[(0, 1, 2), (0, 1, 2)] = 1
SE3_3x3[(0, 1, 2), (2, 1, 0)] = 1
SE3_5x5 = np.zeros((5, 5), dtype=np.int32)
SE3_5x5[(0, 1, 2, 3, 4), (0, 1, 2, 3, 4)] = 1
SE3_5x5[(0, 1, 2, 3, 4), (4, 3, 2, 1, 0)] = 1

# Plus
SE4_3x3 = np.zeros((3, 3), dtype=np.int32)
SE4_3x3[1, :] = 1
SE4_3x3[:, 1] = 1
SE4_5x5 = np.zeros((5, 5), dtype=np.int32)
SE4_5x5[2, :] = 1
SE4_5x5[:, 2] = 1

# Rhombus
SE5_3x3 = np.array(disk(1), dtype=np.int32)
SE5_3x3[1, 1] = 0
SE5_5x5 = np.array(disk(2), dtype=np.int32)
SE5_5x5[(1, 2, 2, 2, 3), (2, 1, 2, 3, 3)] = 0

# Square (Empty)
SE7_3x3 = np.ones((3, 3), dtype=np.int32)
SE7_3x3[1, 1] = 0
SE7_5x5 = np.ones((5, 5), dtype=np.int32)
SE7_5x5[1:4, 1:4] = 0

# Line to right
SE8_3x3 = np.zeros((3, 3), dtype=np.int32)
SE8_3x3[:, 2] = 1
SE8_5x5 = np.zeros((5, 5), dtype=np.int32)
SE8_5x5[:, 4] = 1

# Line to left
SE9_3x3 = np.zeros((3, 3), dtype=np.int32)
SE9_3x3[:, 0] = 1
SE9_5x5 = np.zeros((5, 5), dtype=np.int32)
SE9_5x5[:, 0] = 1

# Line to Top
SE10_3x3 = np.zeros((3, 3), dtype=np.int32)
SE10_3x3[0, :] = 1
SE10_5x5 = np.zeros((5, 5), dtype=np.int32)
SE10_5x5[0, :] = 1

# Line to Bottom
SE11_3x3 = np.zeros((3, 3), dtype=np.int32)
SE11_3x3[-1, :] = 1
SE11_5x5 = np.zeros((5, 5), dtype=np.int32)
SE11_5x5[-1, :] = 1

list_se_3x3 = [SE3_3x3, SE4_3x3, SE5_3x3, SE7_3x3, SE8_3x3, SE9_3x3, SE10_3x3, SE11_3x3]
list_se_3x3_names = ['SE3_3x3', 'SE4_3x3', 'SE5_3x3', 'SE7_3x3', 'SE8_3x3', 'SE9_3x3', 'SE10_3x3', 'SE11_3x3']
list_se_5x5 = [SE3_5x5, SE4_5x5, SE5_5x5, SE7_5x5, SE8_5x5, SE9_5x5, SE10_5x5, SE11_5x5]
