from operator import itemgetter

from VideoSummarization.VIdeoSummarization import VideoSummarization


class CategorySummarization(VideoSummarization):
    def summarize_A_category_video(self):
        data = self.get_data_from_database()
        data = self.prepare_shots_data(data)
        data = self.sort_shots_of_A_category_video(data)
        data = self.select_number_of_shots_depending_on_expected_video_time(data)
        data = self.sort_shots_based_on_shot_number(data)
        self.prepare_summarization_recipe(data)

    def summarize_B_category_video(self):
        data = self.get_data_from_database()
        data = self.prepare_shots_data(data)
        data = self.sort_shots_of_B_category_video(data)
        data = self.select_number_of_shots_depending_on_expected_video_time(data)
        data = self.sort_shots_based_on_shot_number(data)
        self.prepare_summarization_recipe(data)

    def summarize_C_category_video(self):
        data = self.get_data_from_database()
        data = self.prepare_shots_data(data)
        data = self.sort_shots_of_C_category_video(data)
        data = self.select_number_of_shots_depending_on_expected_video_time(data)
        data = self.sort_shots_based_on_shot_number(data)
        self.prepare_summarization_recipe(data)

    def sort_shots_of_A_category_video(self, shots_data):
        calculated_data = [
            {
                'shot_number': shot['shot_number'],
                'frames_range': shot['frames_range'],
                'coefficient': shot['SA'] * shot['TA']
            }
            for shot in shots_data]
        sorted_shots = list()
        sorted_shots.append(calculated_data[0])
        calculated_data = sorted(calculated_data[1:], key=itemgetter('coefficient'))[::-1]
        sorted_shots += calculated_data
        return sorted_shots

    def sort_shots_of_B_category_video(self, shots_data):
        pass

    def sort_shots_of_C_category_video(self, shots_data):
        calculated_data = [
            {
                'shot_number': shot['shot_number'],
                'frames_range': shot['frames_range'],
                'coefficient': shot['SA'] * shot['TA']
            }
            for shot in shots_data]
        sorted_shots = list()
        calculated_data = sorted(calculated_data, key=itemgetter('coefficient'))[::-1]
        sorted_shots += calculated_data
        return sorted_shots

if __name__ == "__main__":
    vs = CategorySummarization('YswnulN_q0w', 60)
    vs.summarize_A_category_video()
