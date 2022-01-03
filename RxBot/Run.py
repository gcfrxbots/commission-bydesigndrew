from threading import Thread
from Initialize import *
initSetup()
from CustomCommands import *
from websocket import create_connection


customcmds = CustomCommands()




class runMiscControls:

    def __init__(self):
        pass

    def getUser(self, line):
        seperate = line.split(":", 2)
        user = seperate[1].split("!", 1)[0]
        return user

    def getMessage(self, line):
        seperate = line.split(":", 2)
        message = seperate[2]
        return message

    def formatTime(self):
        return datetime.datetime.today().now().strftime("%I:%M")


def runcommand(command, cmdArguments, user, mute):
    commands = {**commands_CustomCommands}
    cmd = None
    arg1 = None
    arg2 = None

    for item in commands:
        if item == command:
            if commands[item][0] == "MOD":  # MOD ONLY COMMANDS:
                if (user in core.getmoderators()):
                    cmd = commands[item][1]
                    arg1 = commands[item][2]
                    arg2 = commands[item][3]
                else:
                    chatConnection.sendToChat("You don't have permission to do this.")
                    return
            elif commands[item][0] == "STREAMER":  # STREAMER ONLY COMMANDS:
                if (user == settings['CHANNEL']):
                    cmd = commands[item][1]
                    arg1 = commands[item][2]
                    arg2 = commands[item][3]
                else:
                    chatConnection.sendToChat("You don't have permission to do this.")
                    return
            else:
                cmd = commands[item][0]
                arg1 = commands[item][1]
                arg2 = commands[item][2]
            break
    if not cmd:
        return

    #try:  # Run all commands as a try/except, so the bot doesn't crash if one bot errors out.
    output = eval(cmd + '(%s, %s)' % (arg1, arg2))
    #except Error as e:
        # print("Error running the command %s with the args %s" % (command, cmdArguments))
        # print(e)
    #else:
    if not output:
        return

    chatConnection.sendToChat(user + " >> " + output)


class chat:
    def __init__(self):
        self.ws = None
        self.url = "wss://api.casterlabs.co/v2/koi?client_id=LmHG2ux992BxqQ7w9RJrfhkW"
        self.puppet = False
        self.active = False

        # Set the normal token
        if os.path.exists("../Config/token.txt"):
            with open("../Config/token.txt", "r") as f:
                self.token = f.read()
                f.close()

        # Set the puppet token, if it exists
        if os.path.exists("../Config/puppet.txt"):
            self.puppet = True
            with open("../Config/puppet.txt", "r") as f:
                self.puppetToken = f.read()
                f.close()

    def login(self):
        loginRequest = {
                "type": "LOGIN",
                "token": self.token
            }
        self.ws.send(json.dumps(loginRequest))

    def puppetlogin(self):
        time.sleep(1.5)
        loginRequest = {
            "type": "PUPPET_LOGIN",
            "token": self.puppetToken
        }
        self.ws.send(json.dumps(loginRequest))

    def sendRequest(self, request):
        self.ws.send(json.dumps(request))

    def sendToChat(self, message):
        if message:
            if not self.puppet:
                    request = {
                      "type": "CHAT",
                      "message": message,
                      "chatter": "CLIENT"}
            else:
                request = {
                    "type": "CHAT",
                    "message": message,
                    "chatter": "PUPPET"}
            self.sendRequest(request)


    def main(self):
        self.ws = create_connection(self.url)
        self.login()
        while True:
            result = self.ws.recv()
            resultDict = json.loads(result)
            #print(resultDict)
            if "event" in resultDict.keys() and not self.active:
                if "is_live" in resultDict["event"]:
                    print(">> Connection to chat successful!")
                    channel = resultDict["event"]["streamer"]["username"]
                    settings["CHANNEL"] = channel
                    self.active = True
                    if self.puppet:
                        self.puppetlogin()

            if "event" in resultDict.keys():  # Any actual event is under this
                eventKeys = resultDict["event"].keys()
                if "message" in eventKeys:  # Got chat message, display it then process commands
                    try:

                        message = resultDict["event"]["message"]
                        user = resultDict["event"]["sender"]["displayname"]
                        db.write(
                            '''INSERT INTO chatlog(time, username, message) VALUES("{time}", "{username}", "{message}");'''.format(
                                time=datetime.datetime.now(), username=user, message=message))
                        command = ((message.split(' ', 1)[0]).lower()).replace("\r", "")
                        cmdarguments = message.replace(command or "\r" or "\n", "")[1:]
                        print("(" + misc.formatTime() + ")>> " + user + ": " + message)

                        if command[0] == "!":  # Only run normal commands if COMMAND PHRASE is blank
                            runcommand(command, cmdarguments, user, False)

                        affirmations = ["yes", "yeah", "yep", "indeed"]
                        refutations = ["no", "nope", "not"]

                        for item in affirmations:
                            if item in message:
                                chatConnection.sendToChat(resources.affirmation(user))
                                break
                        for item in refutations:
                            if item in message:
                                chatConnection.sendToChat(resources.refutation(user))
                                break

                        if resultDict["event"]["is_highlighted"]:
                            if settings["TTS HIGHLIGHTED CHAT"]:
                                print("Saying highlighted text in TTS")
                                chatConnection.sendToChat(resources.sayInTTS(message))
                    except:
                        pass

                if "reward" in eventKeys:
                    try:
                        rewardTitle = resultDict["event"]["reward"]["title"]
                        rewardPrompt = resultDict["event"]["reward"]["prompt"]
                        rewardCost = resultDict["event"]["reward"]["cost"]
                        user = resultDict["event"]["sender"]["displayname"]
                        print("(" + misc.formatTime() + ")>> " + user + " redeemed reward title %s, prompt %s, for %s points." % (rewardTitle, rewardPrompt, rewardCost))
                    except:
                        pass

                if "subscriber" in eventKeys:
                    try:
                        subUsername = resultDict["event"]["subscriber"]["username"]
                        subMonths = resultDict["event"]["months"]
                        subLevel = resultDict["event"]["sub_level"]
                        print("(" + misc.formatTime() + ")>> " + subUsername + " subscribed with level %s for %s months." % (subLevel, subMonths))
                        resources.sayInTTS("Thank you %s for subscribing for %s months" % (subUsername, subMonths))
                    except:
                        pass

                if "donations" in eventKeys:
                        bitsAmount = round(resultDict["event"]["donations"][0]["amount"])
                        user = resultDict["event"]["sender"]["displayname"]
                        message = resultDict["event"]["message"]
                        print("(" + misc.formatTime() + ")>> " + user + " cheered %s bits with the message %s" % (bitsAmount, message))

            if "disclaimer" in resultDict.keys():  # Should just be keepalives?
                if resultDict["type"] == "KEEP_ALIVE":
                    response = {"type": "KEEP_ALIVE"}
                    self.sendRequest(response)


chatConnection = chat()


def console():  # Thread to handle console input
    while True:
        consoleIn = input("")

        command = ((consoleIn.split(' ', 1)[0]).lower()).replace("\r", "")
        cmdArguments = consoleIn.replace(command or "\r" or "\n", "").strip()
        # Run the commands function
        if command:
            if command[0] == "!":
                runcommand(command, cmdArguments, "CONSOLE", True)

            if command.lower() in ["quit", "exit", "leave", "stop", "close"]:
                print("Shutting down")
                chatConnection.sendToChat("Bot shutting down")
                os._exit(1)


def tick():
    prevTime = datetime.datetime.now()
    while True:
        time.sleep(0.5)

        if resources.timerActive:
            if datetime.datetime.now() > resources.timer:
                resources.timerDone()

        if datetime.datetime.now() > prevTime + datetime.timedelta(minutes=settings["QUESTION TIMER DELAY"]):
            if settings["ENABLE TIMERS"]:
                chatConnection.sendToChat(resources.askChatAQuestion())
                prevTime = datetime.datetime.now()





if __name__ == "__main__":
    misc = runMiscControls()

    t1 = Thread(target=chatConnection.main)
    t2 = Thread(target=console)
    t3 = Thread(target=tick)

    t1.start()
    t2.start()
    t3.start()
