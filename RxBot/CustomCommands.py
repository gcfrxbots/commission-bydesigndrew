from Settings import *
from Initialize import *




commands_CustomCommands = {
    "!test": ('customcmds.example', 'cmdArguments', 'user'),
}

class resources:
    def __init__(self):
        pass

    def askChatAQuestion(self, question):
        print("Asking chat the question: %s" % question)
        return question



class CustomCommands:
    def __init__(self):
        pass

    def example(self, args, user):
        chatConnection.sendMessage(resources.askChatAQuestion("Is everyone enjoying themselves?"))


resources = resources()