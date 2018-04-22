# -*- coding: utf-8 -*-
import mysql.connector
from datetime import date
from mysql.connector import errorcode

class Database :

    config = {
        'host' : 'db-api-justify.mysql.database.azure.com',
        'user' : 'admin-ad-api@db-api-justify',
        'password' : 'eE77ae62465811e896f5548ca0d1cf18',
        'database' : 'api-justify'
    }

    def __init__(self) : 
        try :
            self.conn = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err :
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR :
                print("Something is wrong with the user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR :
                print("Database does not exist")
            else :
                print(err)
            quit()
        else :
            self.cursor = self.conn.cursor()
            # self.cursor.execute("delete from user;")

    def getUsers(self) :
        users = []
        self.cursor.execute("select email, pwd, creation_date from user;")
        rows = self.cursor.fetchall()
        for row in rows :
            users.append({
                'email' : row[0],
                'pwd' : row[1],
                'creat' : row[2]
            })

        return users

    def getUser(self, username) :
        for user in self.getUsers() :
            if user['email'] == username :
                return user

    def getNbWordsByUser(self, username) :
        nbWords = 0
        self.cursor.execute("select nb_words from text_justified where email = %s and date = %s;", (username, date.today()))
        rows = self.cursor.fetchall()
        for row in rows :
            nbWords += row[0]
        return nbWords

    def save_justification(self, username, nbWords) :
        self.cursor.execute("insert into text_justified values(%s, %s, %s)", (username, nbWords, date.today()))
        self.conn.commit()

    def saveUser(self, email, pwd) :
        self.cursor.execute("insert into user value(%s, %s, %s);", (email, pwd, date.today()))
        self.conn.commit()

    def userExists(self, username) :
        for user in self.getUsers() :
            if user['email'] == username :
                return True
        return False
