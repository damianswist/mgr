import pandas

from DBHandler.DBHandler import DBHandler
import csv
import fileinput

from Settings import Settings


class LearningDataHandler(object):
    def __init__(self, video_id, recipe):
        self.video_id = video_id
        self.recipe = recipe

    def set_summarization(self, video_id, recipe):
        self.video_id = video_id
        self.recipe = recipe

    def fill_a_learning_data(self, grade):
        recipe = self.prepare_recipe_data()
        data = self.download_summarization_data(recipe)
        data = self.calculate_data(data, recipe)
        self.fill_file_with_data(data, grade)
        return data

    # def fill_b_learning_data(self):
    #     self.load_recipe()
    #
    # def fill_c_learning_data(self):
    #     self.load_recipe()

    def load_recipe(self):
        with open(self.recipe, 'r') as file:
            content = [line.strip() for line in file]
        return content

    def prepare_recipe_data(self):
        data = self.load_recipe()
        data = self.convert_recipe_format(data)
        return data

    def convert_recipe_format(self, data):
        results = list()
        for e in data:
            x = e.split(", ")
            results.append({'start': int(x[0]), 'end': int(x[1])})
        return results

    def download_summarization_data(self, recipe):
        db = DBHandler()
        db.connect()
        results = db.get_selected_video_data(self.video_id)
        db.close_connection()
        results = self.filter_frames(results, recipe)
        return results

    def filter_frames(self, data, recipe):
        results = list()
        for shot in recipe:
            for x in range(shot['start'], shot['end']+1):
                results.append(data[x])
        return results

    def calculate_data(self, data, recipe):
        shots_data = list()
        cnt = 0
        for shot_period in recipe:
            frames_number = 1 + shot_period['end'] - shot_period['start']
            blockiness = 0.0
            sa = 0.0
            letterbox = 0.0
            pillarbox = 0.0
            blockloss = 0.0
            blur = 0.0
            ta = 0.0
            blackout = 0.0
            freezing = 0.0
            exposure_bri = 0.0
            contrast = 0.0
            interlace = 0.0
            noise = 0.0
            slice = 0.0
            flickering = 0.0
            first_frame_of_shot = True
            for x in range(cnt, cnt+frames_number):
                if not first_frame_of_shot:
                    # TA depends on previous frame, so if it is from another shot it should be omitted
                    ta += float(data[x][10])
                blockiness += float(data[x][4])
                sa += float(data[x][5])
                letterbox += float(data[x][6])
                pillarbox += float(data[x][7])
                blockloss += float(data[x][8])
                blur += float(data[x][9])
                blackout += float(data[x][11])
                freezing += float(data[x][12])
                exposure_bri += float(data[x][13])
                contrast += float(data[x][14])
                interlace += float(data[x][15])
                noise += float(data[x][16])
                slice += float(data[x][17])
                flickering += float(data[x][18])

                first_frame_of_shot = False
                cnt += 1
            shot = {
                # 'frames_range': "{0}, {1}".format(shot_period['start'], shot_period['end']),
                'blockiness': float(blockiness / frames_number),
                'SA': float(sa / frames_number),
                'letterbox': float(letterbox / frames_number),
                'pillarbox': float(pillarbox / frames_number),
                'blockloss': float(blockloss / frames_number),
                'blur': float(blur / frames_number),
                'TA': float(ta / (frames_number - 1)),
                'blackout': float(blackout / frames_number),
                'freezing': float(freezing / frames_number),
                'exposure_bri': float(exposure_bri / frames_number),
                'contrast': float(contrast / frames_number),
                'interlace': float(interlace / frames_number),
                'noise': float(noise / frames_number),
                'slice': float(slice / frames_number),
                'flickering': float(flickering / frames_number),
                'grade': 0
            }
            shots_data.append(shot)
        return shots_data


    def get_number_of_last_frame_of_shots(self, recipe):
        results = [x['end'] for x in recipe]
        return results

    def fill_file_with_data(self, data, grade):
        rows = list()
        for row in data:
            x = list()
            x.append(row['blockiness'])
            x.append(row['SA'])
            x.append(row['letterbox'])
            x.append(row['pillarbox'])
            x.append(row['blockloss'])
            x.append(row['blur'])
            x.append(row['TA'])
            x.append(row['blackout'])
            x.append(row['freezing'])
            x.append(row['exposure_bri'])
            x.append(row['contrast'])
            x.append(row['interlace'])
            x.append(row['noise'])
            x.append(row['slice'])
            x.append(row['flickering'])
            x.append(grade)
            rows.append(x)
        with open(r"E:\video_summarization\MachineLearning\learning_data\learning_data_A.csv", 'a') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(rows)

    def add_columns_to_file(self, vid_cat):
        columns = [
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
            "flickering",
            "score"
        ]
        with open(r"E:\video_summarization\MachineLearning\learning_data\learning_data_A.csv", 'a') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(columns)

    @classmethod
    def get_learning_data(cls, vid_cat):
        path = ''
        settings = Settings()
        if vid_cat == "A":
            path = settings.get_a_learning_path()
        elif vid_cat == "B":
            path = settings.get_b_learning_path()
        elif vid_cat == "C":
            path = settings.get_c_learning_path()
        dataset = pandas.read_csv(path, sep="\t")
        return dataset

    def delete_empty_lines(self, file):
        with open('path/to/file') as infile, open('output.txt', 'w') as outfile:
            for line in infile:
                if not line.strip(): continue  # skip the empty line
                outfile.write(line)  # non-empty line. Write it to output

if __name__ == "__main__":
    recipe = r"E:\mgr_ml\Przepisy\qZjjSg4N-GI_random.txt"
    vid_id = "qZjjSg4N-GI"
    handler = LearningDataHandler(vid_id, recipe)
    # handler.add_columns_to_file("a")
    data = handler.fill_a_learning_data(4)

