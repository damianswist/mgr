from VideoSummarization.VIdeoSummarization import VideoSummarization


class TextBasedVideoSummarization(VideoSummarization):
    def __init__(self, file, summarization_time, fps=25):
        self.file = file
        video_id = self.get_video_id()
        super(TextBasedVideoSummarization, self).__init__(video_id, summarization_time, fps)

    def summarize_video(self):
        data = self.load_text_summarization()
        data = self.prepare_time_range_list(data)
        data = self.calculate_frames_range(data)
        self.prepare_summarization_recipe(data)

    def load_text_summarization(self):
        with open(self.file) as f:
            content = f.readlines()
        # removing newline character
        content = [x.strip() for x in content]
        return content

    def prepare_time_range_list(self, data):
        time_range_list = list()
        for line in data[1:]:
            words_array = line.split()
            tmp = {
                'start': float(words_array[0]),
                'end': float(words_array[1])
            }
            time_range_list.append(tmp)
        return time_range_list

    def calculate_frames_range(self, data):
        calculated_data = [
            {
                'frames_range': "{0}, {1}".format(int(word['start'] * self.fps), int(word['end'] * self.fps))
            } for word in data
        ]
        return calculated_data

    def get_video_id(self):
        # ToDo Rework that
        # video_id = file.split("_")[4]
        video_id = "zUVs6NAKzC0"
        return video_id


if __name__ == "__main__":
    file = "C:\\Users\\Damian\\Desktop\\mgr\\tmp_streszczenia\\english\\eval_en\\zUVs6NAKzC0\\zUVs6NAKzC0_summary.txt"
    vs = TextBasedVideoSummarization(file, 60)
    vs.summarize_video()
