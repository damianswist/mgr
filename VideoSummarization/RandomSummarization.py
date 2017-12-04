from VideoSummarization.VIdeoSummarization import VideoSummarization

import random


class RandomSummarization(VideoSummarization):
    def summarize_video(self):
        data = self.prepare_minimized_shots_data()
        data = self.sort_shots_randomly(data)
        data = self.select_number_of_shots_depending_on_expected_video_time(data)
        data = self.sort_shots_based_on_shot_number(data)
        self.prepare_summarization_recipe(data)

    def sort_shots_randomly(self, shots_data):
        '''
        Sorts shots in random order
        :param shots_data: list of dicts in below format:
            {
                'shot_number': number of selected shots,
                'frames_range': frames range of selected shot,
            }
        :return: list of dicts in below format:
            {
                'shot_number': number of selected shots,
                'frames_range': frames range of selected shot,
            }
        '''
        calculated_data = [
            {
                'shot_number': shot['shot_number'],
                'frames_range': shot['frames_range'],
            }
            for shot in shots_data]

        sorted_shots = list()

        shots_amount = len(calculated_data)
        for x in range(shots_amount):
            choice = random.choice(calculated_data)
            sorted_shots.append(choice)
            calculated_data.remove(choice)

        return sorted_shots

if __name__ == "__main__":
    vs = RandomSummarization('YswnulN_q0w', 60)
    vs.summarize_video()
