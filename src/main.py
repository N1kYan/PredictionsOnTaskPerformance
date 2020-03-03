# Main Python File
import os
import sys
import numpy as np
import pdf2image
import pandas as pd
from src.discrete_distribution_reader import DiscreteDistributionReader as DDR
from src.read_pdfs import extract_pdfs

# TODO: Yannik, bitte teste mal, ob das bei dir jetzt funktioniert

'''
    Because the working directory is dependent on the configuration of the 
    python IDE each person is using, we make sure that the current
    working directory is set to the 'PredictionsOnTaskPerformance' folder
    and not the 'src' folder.
'''
current_folder = os.path.basename(os.getcwd())
if current_folder == f'src':
    os.chdir(f'..')


# --------------- Scoring Function --------------- #

def score(answers, points_per_task):
    """ This function returns a discrete score for an input numpy array of actual answer positions for a sorting task.
        E.g. if a subjects answer for a task is a sorting of [A, C, E, B, D], we pass the correct positions
        [1, 3, 5, 2, 4] to the function.
        The method then calculates the 2-norm between the right answer [1, 2, 3, 4, 5]
        and the given answer [1, 3, 5, 2, 4].
        The interval [0, max-2-norm] is split into an array of a fixed amount of equidistant numbers (e.g. 5 or 10).
        The discrete rating for this task is the 'id' of the closes value of that array compared to the norm
        of the answer.
        E.g. if the subjects answer got a norm of 3.16 and we have a max-2-norm of 6.32 (worst possible answer) and we
        split the task into 5 possible ratings (1-5 points), we get the intervals [0, 1.27, 2.53, 3.79, 5.06, 6.32].
        The function would return a rating of 5 - 3 = 2.
    """
    def find_nearest(array, value):
        """ Returns entry of array that is closest to value.
        """
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    task_norm = np.linalg.norm(x=(np.array([1, 2, 3, 4, 5]) - answers), ord=2)
    print("Task norm: ", task_norm)
    max_norm = np.linalg.norm(x=(np.array([1, 2, 3, 4, 5]) - np.array([5, 4, 3, 2, 1])), ord=2)
    print("Max norm: ", max_norm)
    # We use a min 0 points and a max of points_per_task
    intervals = np.linspace(0, max_norm, points_per_task+1)
    print("Intervals: ", intervals)
    rating = points_per_task - np.where(intervals == find_nearest(intervals, task_norm))[0][0]
    print("Rating: ", rating)
    return rating


# score(answers=np.array([1, 3, 5, 2, 4]), points_per_task=5)
# TODO: Use score function to calculate the brier score for the answers.

# --------------- Folder & File Names --------------- #

# Specify all the file suffixes (difference between folder name and file name)
# for each file that should be read. The pdfs will be read and annotated
# in the order the files appear in the array.
file_suffixes = [f'_p1.jpg', f'_p2.jpg', f'_p3.jpg']

# Getting all the subdirectory names in the subjects folder
subjects_folder_path = f'assets/subjects/'
subject_dirs_ = os.listdir(subjects_folder_path)

# Delete folders that do not start with "subject" (e.g. Apple hidden .DS_Store)
subject_dirs = []
for sd in subject_dirs_:
    if sd.startswith("subject_"):
        subject_dirs.append(sd)

# --------------- Read PDFs --------------- #

# Iterate over all subjects and read the pdfs
for sd in subject_dirs:

    # Create array with a seperate string for each file that we
    # want to read for this subject.
    images_array = []
    for fs in file_suffixes:
        images_array.append(f'{subjects_folder_path}'
                            f'{sd}/raw/{sd}{fs}')

    # Convert pdf to jpg if it is not already available in jpg
    # Note: The "poppler" package needs to be installed
    for img in images_array:
        if not os.path.exists(img):
            print(f'{img[:-3]}pdf')
            files = pdf2image.convert_from_path(f'{img[:-3]}pdf')
            files[0].save(img, f'jpeg')

    # Path where we save the probability density functions
    dst_path = f'{subjects_folder_path}{sd}/pdfs/'

    # Create 'pdfs'-folder if it does not exist
    if not os.path.exists(dst_path):
        os.mkdir(dst_path)

    # Extract pdfs and save
    extract_pdfs(image_path_array=images_array, dst_folder=dst_path)


# --------------- Read Answer CSV --------------- #
'''
    Read the answers of the csv file and put them into a dictionary.
    The keys are 'task_1', 'task_2', ... and each entry is a list of
    the correct position of each answer for the specific task in
    ascending order.
    Example: subject wrote [A, C, E, B, D] correct would be 
    [A, B, C, D, E] so the list for that task is [1, 3, 5, 2, 4].
'''

# 2D array with subject dir as first entry and answers dictionary as second
subject_answers = []

for subject_dir in subject_dirs:
    path_to_csv = f'{subjects_folder_path}{subject_dir}/' \
                  f'{subject_dir}_answers.csv'
    if os.path.exists(path_to_csv):
        answers = pd.read_csv(path_to_csv, sep=',')
        answers = answers.set_index('task').T.to_dict(f'list')

        subject_answers.append([subject_dir, answers])

# --------------- Print Scoring --------------- #

for subject_dir, answers in subject_answers:
    for i in range(1, 9):
        print(score(answers[f'task_{i}'], 5))

# --------------- Simulate Distribution --------------- #
#
# dr = DDR(subject_code)
# dr.plot(task_id=1)
# dr.plot(task_id=2)
# dr.plot(task_id=3)
# dr.plot(task_id=4)
# dr.plot(task_id=5)
# dr.plot(task_id=6)
# dr.plot(task_id=7)
# dr.plot(task_id=8)



