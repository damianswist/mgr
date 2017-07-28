from DBHandler.DBHandler import DBHandler


class VideoSummarization(object):
    def __init__(self, video_id, summarization_time, fps=25):
        ''' Inits VideoSummarization with video_id (youtube identifier), summarization time in seconds and fps number
            (default value is equal to 25) '''
        self.video_id = video_id
        self.summarization_time = summarization_time
        self.fps = fps

    def prepare_summarization_recipe(self):
        ''' Prepares recipe of summarization (txt file witch contains selected frames numbers)'''
        data = self.get_data_from_database()
        data = self.prepare_shots_data(data)
        print(data)

    def get_data_from_database(self):
        ''' Downloads data for every frame of video from AMIS database
            RETURNS tuple of tuples
            eg. (18332870, 'YswnulN_q0w', 1, 0, '0.94962', '60.08957', '0.00000', '0.00000', '0.17857', '5.726',
             '21.77585', '0', '0', '136', '62.39975', '0.00537', '0.0000', '2.494', '-1.00000') '''
        db = DBHandler()
        db.connect()
        results = db.get_selected_video_data(self.video_id)
        db.close_connection()
        return results

    def get_last_frame_of_shots_numbers(self):
        ''' Downloads last frame of shots numbers for summarized video
            RETURNS list of frames '''
        db = DBHandler()
        db.connect()
        last_frames = db.get_video_last_frame_of_shots_numbers(self.video_id)
        db.close_connection()
        return last_frames

    def prepare_shots_data(self, frames_data):
        shots_data = list()
        last_frames = self.get_last_frame_of_shots_numbers()

        # ToDo - check how below coefficients should be calculated
        '''
            frame_data[0] = frame id
            frame_data[1] = video id (youtube identifier)
            frame_data[2] = frame number
            frame_data[3] = newshot (not fully filled)
            frame_data[4] = vq_Blockiness
            frame_data[5] = vq_SA
            frame_data[6] = vq_Letterbox
            frame_data[7] = vq_Pillarbox
            frame_data[8] = vq_Blockloss
            frame_data[9] = vq_Blur
            frame_data[10] = vq_TA
            frame_data[11] = vq_Blackout
            frame_data[12] = vq_Freezing
            frame_data[13] = vq_Exposure_bri
            frame_data[14] = vq_Contrast
            frame_data[15] = vq_Interlace
            frame_data[16] = vq_Noise
            frame_data[17] = vq_Slice
            frame_data[18] = vq_Flickering
        '''

        shot_number = 0

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

        last_frame_number = 0

        for shot_end in last_frames:
            first_frame_number = last_frame_number + 1
            last_frame_number = shot_end

            first_frame_of_shot = True
            for frame_number in range(first_frame_number, last_frame_number):
                if not first_frame_of_shot:
                    # TA depends on previous frame, so if it is from another shot it should be omitted
                    ta += float(frames_data[frame_number][10])

                blockiness += float(frames_data[frame_number][4])
                sa += float(frames_data[frame_number][5])
                letterbox += float(frames_data[frame_number][6])
                pillarbox += float(frames_data[frame_number][7])
                blockloss += float(frames_data[frame_number][8])
                blur += float(frames_data[frame_number][9])
                blackout += float(frames_data[frame_number][11])
                freezing += float(frames_data[frame_number][12])
                exposure_bri += float(frames_data[frame_number][13])
                contrast += float(frames_data[frame_number][14])
                interlace += float(frames_data[frame_number][15])
                noise += float(frames_data[frame_number][16])
                slice += float(frames_data[frame_number][17])
                flickering += float(frames_data[frame_number][18])

                first_frame_of_shot = False

            frames_number = last_frame_number - first_frame_number
            shot = {
                'shot_number': shot_number,
                'frames_range': "{0}, {1}".format(first_frame_number, last_frame_number),
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
            }
            shots_data.append(shot)

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

            shot_number += 1

        return shots_data


if __name__ == "__main__":
    vs1 = VideoSummarization('1H7Y_vcI_6c', 60)
    # vs2 = VideoSummarization('YswnulN_q0w', 60)

    vs1.prepare_summarization_recipe()
    # vs2.prepare_summarization_recipe()

