from Initialize import *
import random
import urllib, urllib.request
from gtts import gTTS
import playsound

commands_CustomCommands = {
    #"!test": ('customcmds.example', 'cmdArguments', 'user'),
    "!uptime": ('customcmds.uptime', 'cmdArguments', 'user'),
    "!followage": ('customcmds.followage', 'cmdArguments', 'user'),
    "!coinflip": ('customcmds.coinflip', 'cmdArguments', 'user'),
    "!description": ('customcmds.description', 'cmdArguments', 'user'),
    "!bullshit": ('customcmds.bullshit', 'cmdArguments', 'user'),
    "!tts": ("STREAMER", 'customcmds.tts', 'cmdArguments', 'user'),
    "!commands": ('customcmds.commands', 'cmdArguments', 'user'),
    "!timestamp": ('customcmds.timestamp', 'cmdArguments', 'user'),
    "!addcounter": ("STREAMER", 'customcmds.addCounter', 'cmdArguments', 'user'),
    "!count": ('customcmds.count', 'cmdArguments', 'user'),
}


class resources:
    def __init__(self):
        self.questionActive = False
        self.reallyBadWords = [
            "Nigger",
            "Nig",
            "Faggot",
            "Fag",
            "Cracker",
            "Cunt",
            "Tranny",
            "Shemale",
            "Kike",
            "Nicker",
            "Tard",
            "Negro",
            "Chink"
        ]

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
        self.questions = [
            "Is everyone enjoying themselves?",
            "Is everyone understanding everything?",
            "Does everything make sense so far?",
        ]
        self.timerActive = False
        self.timer = datetime.datetime.now()

    def affirmation(self, user):
        if self.questionActive:
            return random.choice(self.affirmationResponses)

    def refutation(self, user):
        if self.questionActive:
            return random.choice(self.refutationResponses)

    def setTimer(self, duration):
        self.timerActive = True
        curTime = datetime.datetime.now()
        targetTime = curTime + datetime.timedelta(seconds=duration)
        self.timer = targetTime

    def timerDone(self):
        self.timerActive = False
        self.questionActive = False

    def askChatAQuestion(self):
        question = random.choice(self.questions)
        print("Asking chat the question: %s" % question)
        self.questionActive = True
        self.setTimer(15)
        return question

    def callApi(self, url):
        f = urllib.request.urlopen(url)
        return f.read().decode("utf-8")

    def sayInTTS(self, message):
        for badword in self.reallyBadWords:
            if badword.lower() in message.lower():
                return "You can't say that! That has a bad word in it!"
        os.remove("message.mp3")
        msgObj = gTTS(text=message, lang="en", slow=False)
        msgObj.save("message.mp3")
        playsound.playsound("message.mp3")



class CustomCommands:
    def __init__(self):
        pass

    def example(self, args, user):
        return

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

    def bullshit(self, args, user):
        firstWordList = ["implement", "utilize", "enhance", "reclaim", "ratify", "hybirdize", "inundate", "re-tool", "mesh", "montage", "threshold", "anticipate", "design", "embrace", "integrate", "capture", "biodiversify", "bundle", "streamline", "regenerate", "perforate", "optimize", "evolve", "transform", "amplify", "embrace", "enable", "orchestrate", "leverage", "reinvent", "aggregate", "architect", "stratify", "mediate", "diversify", "enhance", "assign", "incentivize", "differentiate", "de-differentiate", "morph", "empower", "monetize", "bifurcate", "allocate", "deterritorialize", "contaminate", "initialize", "harness", "facilitate", "seize", "disintermediate", "synergize", "strategize", "deploy", "map", "reconceptualize", "brand", "urbanize", "survey", "curate", "diagram", "grow", "target", "synthesize", "infiltrate", "mesh", "sediment", "rectify", "seed", "incubate", "engage", "maximize", "negotiate", "expedite", "reintermediate", "exurbanize", "enhance", "innovate", "scale", "unleash", "extend","remidiate", "engineer", "broadcast", "generate", "represent", "intensify", "reveal", "inculcate", "propagate", "transition", "iterate", "cultivate", "matrix", "score", "redefine", "inhabit", "recontextualize"]
        secondWordList = ["performative", "aleatoric", "productive", "rogue", "ruderal", "experiential", "industrial", "elastic", "systematic", "exurban", "pliant", "open-ended", "synthetic", "steady-state", "successional", "boolean", "post-fordist", "eidetic", "bionomic", "emergent", "unassigned", "dendritic", "self-organizing", "post-urban", "abandoned", "post-industrial", "suburban", "adaptive", "hyperbolic", "vertical", "scalar", "site-specific", "imbricate", "heterogeneous", "robust", "revolutionary", "scalable", "geographic", "green", "algorithmic", "generative", "invasive", "fluctuating", "porous", "interstitial", "hydrological", "fluid", "innovative", "latent", "intermodal", "intuitive", "strategic", "urbanistic", "fallow", "malleable", "hybrid", "temporal", "undefined", "ephemeral", "urban", "end-to-end", "global", "sectional", "granular", "scaled", "landscape", "interconnected", "frictionless", "sustainable", "virtual", "viral", "dynamic", "mutable", "magnetic", "revelatory", "bleeding-edge", "interactive", "back-end", "real-time", "efficient", "front-end", "distributed", "seamless", "extensible", "open-source", "hyper", "cross-platform", "integrated", "regional", "transparent", "indexical", "permeable", "rhizomatic", "topographical", "probabilistic", "infrastructural", "visionary", "customized", "vegetal", "ubiquitous", "plug-and-play", "collaborative", "compelling", "holistic"]
        thirdWordList = ["synergies", "scenarios", "basins", "paradigms", "agents", "vocabularies", "surfaces", "morphologies", "phase-states", "dynamic equilibria", "conditions", "territories", "regimes", "markets", "programs", "partnerships", "infrastructures", "planes", "recipes", "armatures", "platforms", "maps", "furrows", "mappings", "grids", "initiatives", "channels", "fields", "communities", "solutions", "palimpsests", "ecologies", "pluralities", "flows", "clusters", "sites", "edges", "membranes", "sinks", "peripheries", "ecosystems", "nodes", "operations", "corridors", "rhizomes", "methodologies", "ecologies", "portals", "niches", "technologies", "contexts", "laminar flows", "convergence", "relationships", "processes", "urbanisms", "architectures", "interfaces", "taxonomies", "systems", "commons", "meshworks", "hybrids", "gradients", "frameworks", "events", "microclimates", "models", "interventions", "deliverables", "users", "schemas", "networks", "applications", "ecotomes", "drosscapes", "peripheries", "metrics", "functionalities", "nests", "equilibria", "strata", "circuits", "constituencies", "dynamics", "terrains", "thresholds", "dichotomies", "matrices", "mosaics", "experiences", "methodologies"]
        return "Here's some bullshit: " + random.choice(firstWordList) + " " + random.choice(secondWordList) + " " + random.choice(thirdWordList)

    def tts(self, args, user):
        return resources.sayInTTS(args)

    def commands(self, args, user):  # Does not return streamer only commands
        cmds = []
        for key in commands_CustomCommands.keys():
            if not commands_CustomCommands[key][0] == "STREAMER":
                cmds.append(key)

        return "You can use the following commands: " + ", ".join(cmds)

    def timestamp(self, args, user):
        if args == "reset":
            with open("../timestamps.txt", "w") as f:
                f.truncate()
                return "Reset the timestamps!"
        result = resources.callApi("https://beta.decapi.me/twitch/uptime/" + settings['CHANNEL'])
        with open("../timestamps.txt", "a") as f:
            f.write(str(datetime.datetime.now()) + " >> " + result + " - Label: " + args + "\n")
        if args:
            return "Saved a timestamp titled " + args
        else:
            return "Saved a timestamp!"

    def addCounter(self, args, user):
        if not args:
            return "You need to give a name for the counter!"

        result = db.read('''SELECT * FROM counts WHERE counter="%s"''' % args)

        if result:
            return "The counter for %s already exists." % args

        db.write(
            '''INSERT INTO counts(counter, count) VALUES("{counter}", "0");'''.format(counter=args))

        return "Added the counter {0}. Use it by typing !count {0}.".format(args)

    def count(self, args, user):
        if not args:
            return "You need to specify which counter to increase."

        result = db.read('''SELECT count FROM counts WHERE counter="%s"''' % args)
        if not result:
            return "That counter doesn't exist. Ask the streamer to add it!"

        count = int(result[0]) + 1
        db.write(
            '''UPDATE counts SET count = "{count}" WHERE counter = "{counter}";'''.format(counter=args, count=str(count)))
        return "The count for %s is now %s" % (args, str(count))


resources = resources()