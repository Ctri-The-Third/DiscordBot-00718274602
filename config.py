import json

config = {}
with open("config.json",'r') as json_file:
    config = json.load(json_file)

authToken = config["token"]
guildID = config["guildID"]
ownerChannelID = config["ownerChannelID"]

golemMode = {"enabled" : False, "channelID" : 0, "sourceChannelID" : 0}