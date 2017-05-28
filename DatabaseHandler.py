import pymysql as MySQLdb
# pymysql.install_as_MySQLdb()
# import MySQLdb


class DatabaseHandler:

    def __init__(self):
        self.hostname = "pbz.kt.agh.edu.pl"
        self.username = "amis"
        self.psd = "OtiBFLkdXjDWatHL"
        self.dbname = "kozbial"

        self.db = MySQLdb.connect(self.hostname, self.username, self.psd, self.dbname)

    def connect(self):
        self.db = MySQLdb.connect(self.hostname, self.username, self.psd, self.dbname)

    def closeConnection(self):
        self.db.close()

    def print(self, sql):
        cursor = self.db.cursor()
        results = []
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
        except Exception as e:
            print(e)
            print("Error: unable to fecth data")

        return results

    def getPathForSingleVideo(self, videoId):
        cursor = self.db.cursor()
        results = []
        try:
            cursor.execute("SELECT path, vidmp4 FROM amis_video_info WHERE video_id = '" + videoId +"'")
            results = cursor.fetchall()
        except Exception as e:
            print(e)
            print("Error: unable to fecth data")

        return results

    def getPathForMultipleVideos(self, videoIds):
        for item in videoIds:
            self.getPathForSingleVideo(item)



    def checkIfIdExist(self, vidid):
        for r in self.res:
            if(vidid == r[1]):
                print ("Film znajduje sie w bazie")
        return 0

    def getFilePath(self, videoid):
        #row[14] - path
        #row[16] - vidtitle
        #c857a84e5d
        return 0

    def insertItems(self, sqlQuery):
        cursor = self.db.cursor()

        try:
            cursor.execute(sqlQuery)
            print ("Succesfully: "+sqlQuery)

        except Exception as e:
            print(e)
            print("Error: unable to fetch data")

        self.db.commit()