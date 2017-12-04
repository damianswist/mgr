import sys


from VideoSummarization.RandomSummarization import RandomSummarization

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Error: Not enough arguments")

    elif len(sys.argv) == 3:

        ############################################
        # arg1 = time in [s]
        # arg2 = video id
        ############################################

        video = RandomSummarization(sys.argv[2], int(sys.argv[1]))
        video.summarize_video()
    elif len(sys.argv) == 4:
        ############################################
        # arg1 = time in [s]
        # arg2 = video id
        # arg3 fps rate
        ############################################

        video = RandomSummarization(sys.argv[2], int(sys.argv[1]), int(sys.argv[3]))
        video.summarize_video()