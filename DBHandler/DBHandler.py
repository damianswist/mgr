import pymysql


class DBHandler(object):

    def __init__(self):
        self.host = "pbz.kt.agh.edu.pl"
        self.user = "amis"
        self.passwd = "OtiBFLkdXjDWatHL"
        self.db = "kozbial"
        self.port = 3306
        self.conn = None
        self.cursor = None

    def connect(self):
        print("Connecting")
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                        passwd=self.passwd, db=self.db)
        except Exception as e:
            print(e)
            print("Error: can't connect to database")

    def close_connection(self):
        print("Closing connection")
        self.cursor.close()
        self.conn.close()

    def execute_query(self, query):
        print("executing query")
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(query)
        except Exception as e:
            print(e)
            print("Error: can't execute query")

    def get_data(self):
        print("Fetching data")
        results = None
        try:
            results = self.cursor.fetchall()
        except Exception as e:
            print(e)
            print("Error: can't fetch data")
        return results

    def get_selected_video_data(self, video_id):
        query = "SELECT * FROM kozbial.frames WHERE video_id='{0}'".format(video_id)
        self.execute_query(query)
        results = self.get_data()
        return results

    def get_video_last_shot_frames_numbers(self, video_id):
        query = "SELECT * FROM kozbial.frames_sbd WHERE video_id ='{0}'".format(video_id)
        self.execute_query(query)
        results = self.get_data()
        last_frames = [frame[1] for frame in results]
        return last_frames

if __name__ == "__main__":
    print("program start")
    db = DBHandler()
    db.connect()
    query = "SELECT * FROM kozbial.frames WHERE video_id='{0}'".format("YswnulN_q0w")
    db.execute_query(query)
    data = db.get_data()
    print(data)
    db.close_connection()
    print("program end")