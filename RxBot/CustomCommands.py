from Settings import *
from Initialize import *
import random




commands_CustomCommands = {
    "!test": ('customcmds.example', 'cmdArguments', 'user'),
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



class CustomCommands:
    def __init__(self):
        pass

    def example(self, args, user):
        chatConnection.sendMessage(resources.askChatAQuestion("Is everyone enjoying themselves?"))


resources = resources()