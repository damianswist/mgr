import csv
import sys

from operator import itemgetter

from DatabaseHandler import DatabaseHandler


class Video(object):
    def __init__(self):
        self.video_id = None

    def import_csv_to_list(self, csv_file):
        csv_list = []
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    csv_list.append(row)
        return csv_list

    def prepare_shots_data(self, frames_data):
        shots_data = []

        first_frame_number = "0"
        last_frame_number = None

        shot_number = 0
        sa = 0.0
        ta = 0.0

        frames_number = 0
        new_shot = False
        for frame in frames_data[1:]:
            if int(frame[2]) == 1:
                new_shot = True
            if new_shot:
                shot = {
                    'shot_number': shot_number,
                    'frames_range': "{0}, {1}".format(first_frame_number, last_frame_number),
                    'TA': float(ta/(frames_number-1)),
                    'SA': float(sa/frames_number)
                }

                shots_data.append(shot)

                first_frame_number = frame[1] if (frame[1] == "0") else int(frame[1]) + 1

                ta = 0.0
                sa = float(frame[4])
                frames_number = 1
                shot_number += 1
                new_shot = False
            else:
                frames_number += 1
                last_frame_number = frame[1]
                ta += float(frame[3])
                sa += float(frame[4])

        return shots_data

    def sort_shots_depends_on_sa_and_ta_coefficients(self, shots_data):
        calculated_data = [
            {
                'shot_number': shot['shot_number'],
                'frames_range': shot['frames_range'],
                'coefficient': shot['SA'] * shot['TA']
                           }
            for shot in shots_data]
        calculated_data = sorted(calculated_data, key=itemgetter('coefficient'))[::-1]
        return calculated_data

    def sort_shots_depends_on_sa_coefficient(self, shots_data):
        calculated_data = [
            {
                'shot_number': shot['shot_number'],
                'frames_range': shot['frames_range'],
                'coefficient': shot['SA']
                           }
            for shot in shots_data]
        calculated_data = sorted(calculated_data, key=itemgetter('coefficient'))[::-1]
        return calculated_data

    def sort_shots_depends_on_ta_coefficient(self, shots_data):
        calculated_data = [
            {
                'shot_number': shot['shot_number'],
                'frames_range': shot['frames_range'],
                'coefficient': shot['TA']
                           }
            for shot in shots_data]
        calculated_data = sorted(calculated_data, key=itemgetter('coefficient'))[::-1]
        return calculated_data

    def choose_most_important_shots(self, sorted_data, time):
        max_number_of_frames = time * 25  # 25 frames per second
        number_of_selected_frames = 0

        selected_shots = []
        for shot in sorted_data:
            tmp = shot['frames_range'].replace(" ", "").split(',')
            number_of_frames = int(tmp[1]) - int(tmp[0]) + 1
            if(number_of_selected_frames + number_of_frames) <= max_number_of_frames:
                selected_shots.append(shot)
                number_of_selected_frames += number_of_frames
        return selected_shots

    def sort_shots_based_on_shot_number(self, shots):
        return sorted(shots, key=itemgetter('shot_number'))

    def prepare_txt_file_with_recipe(self, data):
        file = open('formula.txt', 'w')
        [file.write(shot['frames_range'] + "\n") for shot in data]
        file.close()

    def prepare_recipe(self, type, time, csv_file):
        csv_list = self.import_csv_to_list(csv_file)
        shots_data = self.prepare_shots_data(csv_list)

        if type == "1":
            calculated_data = self.sort_shots_depends_on_sa_and_ta_coefficients(shots_data)
        elif type == "2":
            calculated_data =self.sort_shots_depends_on_sa_coefficient(shots_data)
        elif type == "3":
            calculated_data = self.sort_shots_depends_on_ta_coefficient(shots_data)

        selected_shots = self.choose_most_important_shots(calculated_data, time)
        sorted_shots = self.sort_shots_based_on_shot_number(selected_shots)
        self.prepare_txt_file_with_recipe(sorted_shots)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Incorrect arguments")

        print("Connecting")
        db = DatabaseHandler()
        print("Connected")

        print("creating query")
        query = "SELECT * FROM kozbial.frames WHERE video_id='YswnulN_q0w'"
        # db.insertItems(query)
        results = db.print(query)
        print("printing results")
        print(results)


    else:

        ############################################
        # arg1 = type of summarization
        #   1) depends on TA and SA
        #   2) depends only on SA
        #   3) depends only on TA
        # arg2 = time in [s]
        # arg3 = localisation of CSV file
        ############################################

        video = Video()
        video.prepare_recipe(sys.argv[1], int(sys.argv[2]), sys.argv[3])


