import sqlite3
import os.path as pt

class Database() :
    
    dbFilename = pt.abspath('database.db')

    def getUserById(self, id:int) :
        query = f"""SELECT * FROM users WHERE id='{str(id)}'"""
        #query = f"""DELETE FROM users WHERE id='{str(id)}'"""
        conn = sqlite3.connect(self.dbFilename)
        cursor = conn.cursor()
        cursor.execute(query)
        users = cursor.fetchall() 
        if len(users) != 0 :
            return users[0]
        else :
            return None

    def createNewUser(self, userInfo:dict):
        isExist = self.getUserById(userInfo['id']) 
        if isExist == None :
            query = f"""INSERT INTO users VALUES ('{userInfo['id']}',  '{userInfo['name']}')"""
            conn = sqlite3.connect(self.dbFilename)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        else:
            return 'false'

    def getAllUsers(self, key=None) -> list :
        query = """SELECT * from users"""
        conn = sqlite3.connect(self.dbFilename)
        cursor = conn.cursor()
        cursor.execute(query )
        users = cursor.fetchall()
        if key == 'id' :
            ids = []
            for item in users :
                ids.append(item[0])
            return ids
        elif key == 'count' :
            counter = len(users)
            return counter
        else :
            return users


qw = Database()
qw.getUserById(331392389)