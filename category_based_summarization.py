import sys

from VideoSummarization.CategorySummarization import CategorySummarization

if __name__ == "__main__":

    if len(sys.argv) < 3:
        video = CategorySummarization('YswnulN_q0w', 60)
        video.prepare_recipe()
    elif len(sys.argv) == 3:

        ############################################
        # arg1 = time in [s]
        # arg2 = video id
        ############################################

        video = CategorySummarization(sys.argv[2], int(sys.argv[1]))
        video.summarize_A_category_video()
    else:
        ############################################
        # arg1 = time in [s]
        # arg2 = video id
        # arg3 = fps rate
        ############################################

        video = CategorySummarization(sys.argv[2], int(sys.argv[1]), int(sys.argv[3]))
        video.prepare_recipe()