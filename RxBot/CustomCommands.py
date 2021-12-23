from Initialize import *
import random
import urllib, urllib.request




commands_CustomCommands = {
    "!test": ('customcmds.example', 'cmdArguments', 'user'),
    "!uptime": ('customcmds.uptime', 'cmdArguments', 'user'),
    "!followage": ('customcmds.followage', 'cmdArguments', 'user'),
    "!coinflip": ('customcmds.coinflip', 'cmdArguments', 'user'),
    "!description": ('customcmds.description', 'cmdArguments', 'user'),
}

class resources:
    def __init__(self):
        self.questionActive = False
        self.affirmationResponses = [
            "I'm glad!",
            "Thank you!",
            "SeemsGood",
            "VirtualHug",
            "PogChamp"
        ]
        self.refutationResponses = [
            "How can I improve?",
            "I'm sorry to hear that.",
        ]
        self.timerActive = False
        self.timer = datetime.datetime.now()

    def affirmation(self, user):
        if self.questionActive:
            chatConnection.sendMessage(random.choice(self.affirmationResponses))

    def refutation(self, user):
        if self.questionActive:
            chatConnection.sendMessage(random.choice(self.refutationResponses))

    def setTimer(self, duration):
        self.timerActive = True
        curTime = datetime.datetime.now()
        targetTime = curTime + datetime.timedelta(seconds=duration)
        self.timer = targetTime

    def timerDone(self):
        self.timerActive = False
        self.questionActive = False
        print("Time's up")

    def askChatAQuestion(self, question):
        print("Asking chat the question: %s" % question)
        self.questionActive = True
        self.setTimer(15)
        return question

    def callApi(self, url):
        f = urllib.request.urlopen(url)
        return f.read().decode("utf-8")



class CustomCommands:
    def __init__(self):
        pass

    def example(self, args, user):
        chatConnection.sendMessage(resources.askChatAQuestion("Is everyone enjoying themselves?"))

    def followage(self, args, user):
        if args:
            user = args
        return resources.callApi("https://beta.decapi.me/twitch/followage/{channel}/{user}".format(channel=settings['CHANNEL'], user=user))

    def uptime(self, args, user):
        result = resources.callApi("https://beta.decapi.me/twitch/uptime/" + settings['CHANNEL'])
        if "offline" in result:
            return result + "."
        else:
            return "The stream has been live for: " + result

    def coinflip(self, args, user):
        result = random.choice(["Heads!", "Tails!"])
        return "The result is... " + result

    def description(self, args, user):
        game = resources.callApi("https://beta.decapi.me/twitch/game/" + settings['CHANNEL'])
        title = resources.callApi("https://beta.decapi.me/twitch/title/" + settings['CHANNEL'])
        print(commandsFromFile)
        return settings["CHANNEL"] + " - " + title + " - Playing " + game


resources = resources()