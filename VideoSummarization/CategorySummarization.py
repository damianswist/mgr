from operator import itemgetter

from VideoSummarization.VIdeoSummarization import VideoSummarization


class CategorySummarization(VideoSummarization):
    def summarize_A_category_video(self):
        data = self.get_data_from_database()
        data = self.prepare_shots_data(data)
        coef = self.calculate_coeficients(data)
        data = self.sort_shots_of_A_category_video(data, coef)
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
        coef = self.calculate_coeficients(data)
        data = self.sort_shots_of_C_category_video(data, coef)
        data = self.select_number_of_shots_depending_on_expected_video_time(data)
        data = self.sort_shots_based_on_shot_number(data)
        self.prepare_summarization_recipe(data)

    def sort_shots_of_A_category_video(self, shots_data, coef):
        # calculated_data = [
        #     {
        #         'shot_number': shot['shot_number'],
        #         'frames_range': shot['frames_range'],
        #         'coefficient': shot['SA'] * shot['TA']
        #     }
        #     for shot in shots_data]

        calculated_data = list()

        for shot in shots_data:
            x = dict()
            x['shot_number'] = shot['shot_number']
            x['frames_range'] = shot['frames_range']

            coefficient = shot['SA'] * shot['TA']

            if not(coef['blockiness']['min'] <= shot['blockiness'] <= coef['blockiness']['max']) and not((coef['blockiness']['mean'] - coef['blockiness']['std']) <= shot['blockiness'] <= (coef['blockiness']['mean'] + coef['blockiness']['std'])):
                coefficient *= 0.8
            elif not(coef['blockiness']['min'] <= shot['blockiness'] <= coef['blockiness']['max']):
                coefficient *= 0.9
            if not ((coef['letterbox']['mean'] - coef['letterbox']['std']) <= shot['letterbox'] <= (
            coef['letterbox']['mean'] + coef['letterbox']['std'])):
                coefficient *= 0.1
            if not ((coef['pillarbox']['mean'] - coef['pillarbox']['std']) <= shot['pillarbox'] <= (
            coef['pillarbox']['mean'] + coef['pillarbox']['std'])):
                coefficient *= 0.1
            if not ((coef['blockloss']['mean'] - coef['blockloss']['std']) <= shot['blockloss'] <= (
            coef['blockloss']['mean'] + coef['blockloss']['std'])):
                coefficient *= 0.9
            if not ((coef['blur']['mean'] - coef['blur']['std']) <= shot['blur'] <= (
            coef['blur']['mean'] + coef['blur']['std'])) and (shot['blur'] < 30):
                coefficient *= 0.9
            elif not ((coef['blur']['mean'] - coef['blur']['std']) <= shot['blur'] <= (
            coef['blur']['mean'] + coef['blur']['std'])) and (30 <= shot['blur'] <= 50):
                coefficient *= 0.7
            elif not ((coef['blur']['mean'] - coef['blur']['std']) <= shot['blur'] <= (
            coef['blur']['mean'] + coef['blur']['std'])) and (shot['blur'] > 50):
                coefficient *= 0.5

            if shot['blackout'] == 1:
                coefficient *= 0
            if shot['freezing'] > 0.1:
                coefficient *= 0.9
            if shot['exposure_bri'] > 200:
                coefficient *= 0.6

            if not ((coef['noise']['mean'] - coef['noise']['std']) <= shot['noise'] <= (
            coef['noise']['mean'] + coef['noise']['std'])):
                coefficient *= 0.9

            if not ((coef['slice']['mean'] - coef['slice']['std']) <= shot['slice'] <= (
            coef['slice']['mean'] + coef['slice']['std'])):
                coefficient *= 0.9

            if not ((coef['flickering']['mean'] - coef['flickering']['std']) <= shot['flickering'] <= (
            coef['flickering']['mean'] + coef['flickering']['std'])):
                coefficient *= 0.9

            x['coefficient'] = coefficient
            calculated_data.append(x)

        sorted_shots = list()
        sorted_shots.append(calculated_data[0])
        calculated_data = sorted(calculated_data[1:], key=itemgetter('coefficient'))[::-1]
        sorted_shots += calculated_data
        return sorted_shots

    def sort_shots_of_B_category_video(self, shots_data):
        pass

    def sort_shots_of_C_category_video(self, shots_data, coef):
        # calculated_data = [
        #     {
        #         'shot_number': shot['shot_number'],
        #         'frames_range': shot['frames_range'],
        #         'coefficient': shot['SA'] * shot['TA']
        #     }
        #     for shot in shots_data]
        sorted_shots = list()

        calculated_data = list()

        for shot in shots_data:
            x = dict()
            x['shot_number'] = shot['shot_number']
            x['frames_range'] = shot['frames_range']

            coefficient = shot['SA'] * shot['TA']

            if not (coef['blockiness']['min'] <= shot['blockiness'] <= coef['blockiness']['max']) and not (
                    (coef['blockiness']['mean'] - coef['blockiness']['std']) <= shot['blockiness'] <= (
                coef['blockiness']['mean'] + coef['blockiness']['std'])):
                coefficient *= 0.8
            elif not (coef['blockiness']['min'] <= shot['blockiness'] <= coef['blockiness']['max']):
                coefficient *= 0.9
            if not ((coef['letterbox']['mean'] - coef['letterbox']['std']) <= shot['letterbox'] <= (
                        coef['letterbox']['mean'] + coef['letterbox']['std'])):
                coefficient *= 0.1
            if not ((coef['pillarbox']['mean'] - coef['pillarbox']['std']) <= shot['pillarbox'] <= (
                        coef['pillarbox']['mean'] + coef['pillarbox']['std'])):
                coefficient *= 0.1
            if not ((coef['blockloss']['mean'] - coef['blockloss']['std']) <= shot['blockloss'] <= (
                        coef['blockloss']['mean'] + coef['blockloss']['std'])):
                coefficient *= 0.9
            if not ((coef['blur']['mean'] - coef['blur']['std']) <= shot['blur'] <= (
                        coef['blur']['mean'] + coef['blur']['std'])) and (shot['blur'] < 30):
                coefficient *= 0.9
            elif not ((coef['blur']['mean'] - coef['blur']['std']) <= shot['blur'] <= (
                        coef['blur']['mean'] + coef['blur']['std'])) and (30 <= shot['blur'] <= 50):
                coefficient *= 0.7
            elif not ((coef['blur']['mean'] - coef['blur']['std']) <= shot['blur'] <= (
                        coef['blur']['mean'] + coef['blur']['std'])) and (shot['blur'] > 50):
                coefficient *= 0.5

            if shot['blackout'] == 1:
                coefficient *= 0
            if shot['freezing'] > 0.1:
                coefficient *= 0.9
            if shot['exposure_bri'] > 200:
                coefficient *= 0.6

            if not ((coef['noise']['mean'] - coef['noise']['std']) <= shot['noise'] <= (
                        coef['noise']['mean'] + coef['noise']['std'])):
                coefficient *= 0.9

            if not ((coef['slice']['mean'] - coef['slice']['std']) <= shot['slice'] <= (
                        coef['slice']['mean'] + coef['slice']['std'])):
                coefficient *= 0.9

            if not ((coef['flickering']['mean'] - coef['flickering']['std']) <= shot['flickering'] <= (
                        coef['flickering']['mean'] + coef['flickering']['std'])):
                coefficient *= 0.9

            x['coefficient'] = coefficient
            print(coefficient)
            calculated_data.append(x)

        calculated_data = sorted(calculated_data, key=itemgetter('coefficient'))[::-1]
        sorted_shots += calculated_data
        return sorted_shots

if __name__ == "__main__":
    vs = CategorySummarization('09Ytjo1cmSE', 60)
    vs.summarize_A_category_video()
