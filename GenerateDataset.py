from GenerateCatA_Simple import generate_100_tasks_CatA_Simple
from GenerateCatA_Hard import generate_100_tasks_CatA_Hard
from GenerateCatB_Selection import generate_100_tasks_CatB_Selection
from GenerateCatB_Sequence import generate_100_tasks_CatB_Sequence
from GenerateCatB_Iteration import generate_100_tasks_CatB_Iteration
from GenerateCatB_Hard import generate_100_tasks_CatB_Hard

param = {}
param['img_size'] = 15
param['se_size'] = 5  # Size of the structuring element
param['seq_length'] = 4  # Number of primitives would be 2*param['seq_length']
param['no_examples_per_task'] = 4
param['no_colors'] = 3

generate_100_tasks_CatA_Simple(32, **param)
generate_100_tasks_CatA_Hard(32, **param)
generate_100_tasks_CatB_Selection(32, **param)
generate_100_tasks_CatB_Sequence(32, **param)
generate_100_tasks_CatB_Iteration(32, **param)
generate_100_tasks_CatB_Hard(32, **param)
