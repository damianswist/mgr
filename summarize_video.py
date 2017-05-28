import sys

from DatabaseHandler import DatabaseHandler

from operator import itemgetter


class Summarization(object):
    def __init__(self, video_id, summarization_time):
        self.video_id = video_id
        self.summarization_time = summarization_time

    def prepare_recipe(self):
        data = self.get_data_from_database()
        data = self.prep_shots_data(data)
        data = self.sort_shots_depends_on_sa_and_ta_coefficients(data)
        data = self.choose_most_important_shots(data)
        data = self.sort_shots_based_on_shot_number(data)
        self.prepare_txt_file_with_recipe(data)

        return data

    def get_data_from_database(self):
        db = DatabaseHandler()
        query = "SELECT * FROM kozbial.frames WHERE video_id='{0}'".format(self.video_id)
        results = db.print(query)
        return results

    def get_last_shot_frames_numbers(self):
        db = DatabaseHandler()
        query = "SELECT * FROM kozbial.frames_sbd WHERE video_id ='{0}'".format(self.video_id)
        results = db.print(query)
        last_frames = [frame[1] for frame in results]
        return last_frames

    def prep_shots_data(self, frames_data):
        shots_data = []
        last_frames = self.get_last_shot_frames_numbers()

        shot_number = 0
        sa = 0.0
        ta = 0.0

        first_frame_number = 0
        last_frame_number = 0

        for shot_end in last_frames:
            first_frame_number = last_frame_number + 1
            last_frame_number = shot_end

            first_frame_of_shot = True
            for frame_number in range(first_frame_number, last_frame_number):
                if not first_frame_of_shot:
                    ta += float(frames_data[frame_number][10])
                sa += float(frames_data[frame_number][5])
                first_frame_of_shot = False

            frames_number = last_frame_number - first_frame_number
            shot = {
                'shot_number': shot_number,
                'frames_range': "{0}, {1}".format(first_frame_number, last_frame_number),
                'TA': float(ta / (frames_number - 1)),
                'SA': float(sa / frames_number)
            }
            shots_data.append(shot)

            ta = 0.0
            sa = 0.0
            shot_number += 1

        return shots_data

    def sort_shots_depends_on_sa_and_ta_coefficients(self, shots_data):
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

    def choose_most_important_shots(self, sorted_data):
        max_number_of_frames = self.summarization_time * 25  # 25 frames per second

        first_shot = sorted_data[0]['frames_range'].replace(" ", "").split(',')
        number_of_selected_frames = int(first_shot[1]) - int(first_shot[0]) + 1

        selected_shots = list()
        selected_shots.append(sorted_data[0])

        for shot in sorted_data[1:]:
            tmp = shot['frames_range'].replace(" ", "").split(',')
            number_of_frames = int(tmp[1]) - int(tmp[0]) + 1
            if (number_of_selected_frames + number_of_frames) <= max_number_of_frames:
                selected_shots.append(shot)
                number_of_selected_frames += number_of_frames
        return selected_shots

    def sort_shots_based_on_shot_number(self, shots):
        return sorted(shots, key=itemgetter('shot_number'))

    def prepare_txt_file_with_recipe(self, data):
        file = open('{0}.txt'.format(self.video_id), 'w')
        [file.write(shot['frames_range'] + "\n") for shot in data]
        file.close()


if __name__ == "__main__":
    video = Summarization('YswnulN_q0w', 60)
    video.prepare_recipe()

    if len(sys.argv) < 3:
        print("Incorrect arguments")
    else:

        ############################################
        # arg1 = time in [s]
        # arg2 = localisation of CSV file
        ############################################

        video = Summarization(sys.argv[3], int(sys.argv[2]))
        video.prepare_recipe()
