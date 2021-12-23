from Settings import *
from subprocess import call
import urllib, urllib.request
import json
import socket
import os
import sqlite3
from sqlite3 import Error
import datetime
try:
    import xlsxwriter
    import xlrd
except ImportError as e:
    print(e)
    raise ImportError(">>> One or more required packages are not properly installed! Run INSTALL_REQUIREMENTS.bat to fix!")
global settings, commandsFromFile

class socketConnection:
    def __init__(self):
        self.socketConn = socket.socket()

    def openSocket(self):
        self.socketConn.connect(("irc.chat.twitch.tv", int(settings['PORT'])))
        self.socketConn.send(("PASS " + settings['BOT OAUTH'] + "\r\n").encode("utf-8"))
        self.socketConn.send(("NICK " + settings['BOT NAME'] + "\r\n").encode("utf-8"))
        self.socketConn.send(("JOIN #" + settings['CHANNEL'] + "\r\n").encode("utf-8"))
        return self.socketConn

    def sendMessage(self, message):
        messageTemp = "PRIVMSG #" + settings['CHANNEL'] + " : " + message
        self.socketConn.send((messageTemp + "\r\n").encode("utf-8"))
        print("Sent: " + message)
        db.write('''INSERT INTO chatlog(time, username, message) VALUES("{time}", "{username}", "{message}");'''.format(
            time=datetime.datetime.now(), username="BOT", message=message))

    def joinRoom(self, s):
        readbuffer = ""
        Loading = True

        while Loading:
            readbuffer = readbuffer + s.recv(1024).decode("utf-8")
            temp = readbuffer.split("\n")
            readbuffer = temp.pop()

            for line in temp:
                Loading = self.loadingComplete(line)

    def loadingComplete(self, line):
        if ("End of /NAMES list" in line):
            print(">> Bot Startup complete!")
            self.sendMessage("Bot is online!")
            return False
        else:
            return True

class coreFunctions:
    def __init__(self):
        pass


    def getmoderators(self):
        moderators = []
        json_url = urllib.request.urlopen('http://tmi.twitch.tv/group/user/' + settings['CHANNEL'].lower() + '/chatters')
        data = json.loads(json_url.read())['chatters']
        mods = data['moderators'] + data['broadcaster']

        for item in mods:
            moderators.append(item)

        return moderators


class dbControl:
    def __init__(self):
        self.db = None

    def createDb(self):
        try:
            self.db = sqlite3.connect('botData.db', check_same_thread=False)
            sql_creation_commands = (
                # Create chat log
                """ CREATE TABLE IF NOT EXISTS chatlog (
                                id integer PRIMARY KEY,
                                time text,
                                username text,
                                message text
                            ); """,
                # Create Backup counts
                """ CREATE TABLE IF NOT EXISTS counts (
                                id integer PRIMARY KEY,
                                counter text NOT NULL,
                                count text
                            ); """,

            )
            c = self.db.cursor()
            for item in sql_creation_commands:
                c.execute(item)
            self.db.commit()
        except Error as e:
            print(e)

    def sqlError(self, src, command, e):
        print("DATABASE ERROR INSIDE %s FUNCTION:" % src.upper())
        print(e)
        print(command)
        return False

    def read(self, command):
        self.db = sqlite3.connect('botData.db', check_same_thread=False)
        try:
            cursor = self.db.cursor()
            cursor.execute(command)
            data = cursor.fetchone()
            self.db.close()
            return data
        except Error as e:
            self.db.rollback()
            self.sqlError("READ", command, e)

    def fetchAll(self, command):
        self.db = sqlite3.connect('botData.db', check_same_thread=False)
        try:
            cursor = self.db.cursor()
            cursor.execute(command)
            data = cursor.fetchall()
            self.db.close()
            return data
        except Error as e:
            self.db.rollback()
            self.sqlError("FETCHALL", command, e)

    def write(self, command):
        self.db = sqlite3.connect('botData.db', check_same_thread=False)
        try:
            cursor = self.db.cursor()
            cursor.execute(command)
            self.db.commit()
            self.db.close()
            return True
        except Error as e:
            self.db.rollback()
            self.sqlError("WRITE", command, e)


chatConnection = socketConnection()
core = coreFunctions()
db = dbControl()

def initSetup():
    global settings, commandsFromFile

    db.createDb()

    # Create Folders
    if not os.path.exists('../Config'):
        buildConfig()
    if not os.path.exists('../Config/Commands.xlsx'):
        buildConfig()
    if not os.path.exists('Resources'):
        os.makedirs('Resources')
        print("Creating necessary folders...")

    # Create Settings.xlsx
    settings = settingsConfig.settingsSetup(settingsConfig())
    commandsFromFile = settingsConfig.readCommands(settingsConfig())

    return

