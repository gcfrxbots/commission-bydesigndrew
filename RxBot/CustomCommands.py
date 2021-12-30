from Initialize import *
import random
import urllib, urllib.request
from gtts import gTTS
import playsound




commands_CustomCommands = {
    "!test": ('customcmds.example', 'cmdArguments', 'user'),
    "!uptime": ('customcmds.uptime', 'cmdArguments', 'user'),
    "!followage": ('customcmds.followage', 'cmdArguments', 'user'),
    "!coinflip": ('customcmds.coinflip', 'cmdArguments', 'user'),
    "!description": ('customcmds.description', 'cmdArguments', 'user'),
    "!bullshit": ('customcmds.bullshit', 'cmdArguments', 'user'),
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
        print("Time's up")

    def askChatAQuestion(self, question):
        print("Asking chat the question: %s" % question)
        self.questionActive = True
        self.setTimer(15)
        return question

    def callApi(self, url):
        f = urllib.request.urlopen(url)
        return f.read().decode("utf-8")

    def sayInTTS(self, message):
        os.remove("message.mp3")
        msgObj = gTTS(text=message, lang="en", slow=False)
        msgObj.save("message.mp3")
        playsound.playsound("message.mp3")



class CustomCommands:
    def __init__(self):
        pass

    def example(self, args, user):
        return  resources.askChatAQuestion("Is everyone enjoying themselves?")

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


resources = resources()