import cv2
import os
from shutil import copy, rmtree

import subprocess


class MoviesHandler(object):
    def extractImagesFromVideo(self, pathIn, pathOut):
        vidcap = cv2.VideoCapture(pathIn)
        cnt = 0
        while True:
            success, image = vidcap.read()
            if not success:
                break
            cv2.imwrite(pathOut + "\\frame{:05d}.jpg".format(cnt), image)
            cnt += 1

    def makeMovie(self):
        command = "ffmpeg -f image2 -r 25 -i summarization_frames/frame%05d.jpg -vb 20M -vcodec mpeg4 -y video.mp4"
        # command = "ffmpeg -f image2 -r 25 -i test/frame%05d.jpg -vcodec libvpx  -y movie.webm"
        os.system(command)


    def getRecipe(self):
        with open('recipe.txt', 'r') as f:
            content = f.readlines()
        content = [line.strip() for line in content]
        return content

    def extractFramesForSummarization(self):
        number = 0
        dest_folder = "summarization_frames"
        intervals = self.getRecipe()
        for interval in intervals:
            first_frame,last_frame = interval.split(", ")
            first_frame = int(first_frame)
            last_frame = int(last_frame)
            for frame_number in range(first_frame, last_frame):
                image = "all_frames/frame{:05d}.jpg".format(frame_number-1)
                copy(image, dest_folder)
                os.rename("summarization_frames/frame{:05d}.jpg".format(frame_number-1),
                          "summarization_frames/frame{:05d}.jpg".format(number))
                number += 1

    def createSummarization(self, video_path):
        images_path = "all_frames"
        os.mkdir(images_path)
        self.extractImagesFromVideo(video_path, images_path)

        selected_frames_path = "summarization_frames"
        os.mkdir(selected_frames_path)
        self.extractFramesForSummarization()

        rmtree(images_path)

        self.makeMovie()
        rmtree(selected_frames_path)

    def extractAudio(self, filepath):
        file_path_output = 'audio.wav'
        subprocess.call(
            ['ffmpeg', '-i', filepath, '-codec:a', 'pcm_s16le', '-ac', '1', file_path_output])

    def extractAudioIntervals(self, fps):
        cnt = 0
        intervals = self.getRecipe()
        for interval in intervals:
            first_frame,last_frame = interval.split(", ")
            start_time = float(int(first_frame)/fps)
            end_time = float(int(last_frame)/fps)
            total_time = end_time - start_time

            command = "ffmpeg -ss {0} -t {1} -i audio.wav audios/file{2}.wav".format(start_time, total_time, cnt)
            os.system(command)
            cnt += 1
        return cnt

    def prepare_audio_file(self, filepath, fps):
        self.extractAudio(filepath)
        os.mkdir("audios")
        number_of_files = self.extractAudioIntervals(fps)
        self.connect_audio_files(number_of_files)
        rmtree("audios")
        os.remove('audio.wav')

    def connect_audio_files(self, number_of_files):
        audio_files_list = ["file 'audios/file{0}.wav'".format(x) for x in range(number_of_files+1)]
        with open('mylist.txt', 'a+') as f:
            for file in audio_files_list:
                f.write(file)
                f.write("\n")
        command = "ffmpeg -f concat  -i mylist.txt -c copy output.wmv"
        os.system(command)
        os.remove('mylist.txt')

    def connect_movie_with_audio(self):
        # command = "ffmpeg -i output.wmv -i movie.mp4 -acodec copy -vcodec copy summarization.mp4"
        command = "ffmpeg -i video.mp4 -i output.wmv -c:v copy -c:a aac -strict experimental output.mp4"
        os.system(command)

if __name__ == "__main__":
    folder = 'test'
    # os.mkdir(folder)
    path = "movie.webm"
    mh = MoviesHandler()

    mh.createSummarization(path)
    mh.prepare_audio_file(path, 25)
    mh.connect_movie_with_audio()
