import sys

from VideoSummarization.CategorySummarization import CategorySummarization

if __name__ == "__main__":

    if len(sys.argv) == 4:

        ############################################
        # arg1 = time in [s]
        # arg2 = video id
        # arg3 = category (A, B or C)
        ############################################

        video = CategorySummarization(sys.argv[2], int(sys.argv[1]))
        if sys.argv[3] == "A":
            video.summarize_A_category_video()
        elif sys.argv[3] == "B":
            video.summarize_A_category_video()
        elif sys.argv[3] == "C":
            video.summarize_C_category_video()
    elif len(sys.argv) == 5:
        ############################################
        # arg1 = time in [s]
        # arg2 = video id
        # arg3 = category(A, B or C)
        # arg4 = fps rate
        ############################################

        video = CategorySummarization(sys.argv[2], int(sys.argv[1]), int(sys.argv[3]))
        if sys.argv[3] == "A":
            video.summarize_A_category_video()
        elif sys.argv[3] == "B":
            video.summarize_A_category_video()
        elif sys.argv[3] == "C":
            video.summarize_C_category_video()
