# IPARC_ChallengeV2


## Notes

All the code to generate the dataset is given in `GenerateDataset.py`. 

### Category A (Simple)

The challenge here is to identify the a sequence of operators which explains the input-output pairs. We follow the following process to generate the input-output pairs for each task:

1. Each task is assigned a random sequence of structuring elements (SE1-SE8). The sequence of operations is defined by alternating dilations and erosions.

2. To generate an input-output pair for each task, we start with a randomly generated base-image. This base-image is considered as input, and the output is generated using the sequence in (1)

3. The generated input-output pairs for each task are saved in `./Dataset/CatA_Simple/Task***.json`. The sequence is saved at `./Dataset/CatA_Simple/Task***_soln.txt` by default.

**Remark 1 :** To avoid empty input-output pairs, we dilate the base-image with structuring elements corresponding to the erosion operator. 

**Remark 2 :** Also, sometimes it can so happen due to chance that input-output pairs might be empty. These are filtered out.

### Category A (Hard)

The hard challenge of Category A includes 3 colors and a color change rule. (See the article for details). The following are the main difference compared to the simple challenge.

1. Each task is now assigned 3 random sequences (one for each colour) of structuring elements (SE1-SE8). The sequence is defined by alternating dilations and erosions.

2. To generate an input-output pair for each task, we start with a randomly generated base-image. This base-image is considered as input, and the output is generated using the sequence in (1).

3. The generated input-output pairs for each task are saved in `./Dataset/CatA_Hard/Task***.json`. The sequence and the color change rule is saved at `./Dataset/CatA_Hard/Task***_soln.txt` by default.


### Category B (Simple)

The idea of Category B tasks arose from the **structured program theorem** which states that three control structures - sequence, selection and iteration are sufficient to represent any program. So, it follows that if an algorithm can learn these three aspects from data, it can reconstruct the program. This is to be achieved by predicate invention.


#### Category B - Sequence

Here the aim is to invent sequence predicates. Each task has a set of subtasks (3) which share a common sequence. So, this subsequence should be identified and added to the background knowledge.

The generated input-output pairs for each task are saved in `./Dataset/CatB_Sequence/Task***.json`. The sequence for each subtask is saved at `./Dataset/CatB_Sequence/Task***_soln.txt` by default.

#### Category B - Selection

Here the aim is to invent conditional predicates. To simulate the conditional we use the `Hit_or_Miss` transform which selects a set of pixels based on the pattern. The pixels which correspond to the pattern are processed by a sequence differently from the pixels which do not correspond to the pattern. 

The generated input-output pairs for each task are saved in `./Dataset/CatB_Selection/Task***.json`. The sequence is saved at `./Dataset/CatB_Selection/Task***_soln.txt` by default.

#### Category B - Iteration

Here the aim is to invent "Iterate k times" predicate. "k" is to be learnt. Each task has a set of subtasks (3) which share a common iteration. This should be learnt.

The generated input-output pairs for each task are saved in `./Dataset/CatB_Iteration/Task***.json`. The sequence for each subtask is saved at `./Dataset/CatB_Iteration/Task***_soln.txt` by default.