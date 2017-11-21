from operator import itemgetter

from MachineLearning.MachineLearningHandler import MachineLearningHandler
from VideoSummarization.VIdeoSummarization import VideoSummarization

import numpy as np
import math


class MachineLearningSummarization(VideoSummarization):
    def summarize_video(self):
        data = self.get_data_from_database()
        data = self.prepare_shots_data(data)
        predictions = self.get_predictions(data)
        data = self.fill_shots_data_with_predictions(data, predictions)
        data = self.sort_shots_basing_on_predictions(data)
        data = self.select_number_of_shots_depending_on_expected_video_time(data)
        data = self.sort_shots_based_on_shot_number(data)
        self.prepare_summarization_recipe(data)
        for d in data:
            print(d)

    def get_predictions(self, data):
        results = list()
        for d in data:
            results.append(self.prepare_row_format(d))
        results = np.array(results)
        results = MachineLearningHandler().get_predictions(results)
        return results

    @staticmethod
    def prepare_row_format(row):
        ordered_columns = [
            "blockiness",
            "SA",
            "letterbox",
            "pillarbox",
            "blockloss",
            "blur",
            "TA",
            "blackout",
            "freezing",
            "exposure_bri",
            "contrast",
            "interlace",
            "noise",
            "slice",
            "flickering"
        ]
        results = [row[i] if math.isfinite(row[i]) or math.isnan(row[i]) else 0.0 for i in ordered_columns]
        results = np.array(results)
        return results

    @staticmethod
    def fill_shots_data_with_predictions( data, predictions):
        results = data
        for i in range(len(results)):
            results[i]['score'] = predictions[i]
        return results

    @staticmethod
    def sort_shots_basing_on_predictions(shots_data):
        # calculated_data = [
        #     {
        #         'shot_number': shot['shot_number'],
        #         'frames_range': shot['frames_range'],
        #         'coefficient': shot[score]
        #     }
        #     for shot in shots_data]

        calculated_data = list()
        for shot in shots_data:
            x = dict()
            x['shot_number'] = shot['shot_number']
            x['frames_range'] = shot['frames_range']
            x['score'] = shot['score']
            calculated_data.append(x)

        calculated_data = sorted(calculated_data, key=itemgetter('score'))[::-1]
        return calculated_data

if __name__ == "__main__":
    vs = MachineLearningSummarization('qYLhOGRdofg', 60)
    vs.summarize_video()
