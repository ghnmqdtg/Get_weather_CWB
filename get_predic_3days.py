import requests
import urllib.parse
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


def Get_Predic_3Days(functions, location):
        # URL for fetching prediction for 2 days.
        Request_URL = config["URL"]["prediction_3days"]\
            + config["settings"]["Authorization"] + "&format=JSON"\
            + "&locationName=" + urllib.parse.quote(location.replace("台", "臺"))

        # filter out which data we need
        data = requests.get(Request_URL).json()["records"]["locations"][0]["location"][0]["weatherElement"]
        # print(type(data))
        print(data[6]["time"][1])

        message = []
        for x in data[6]["time"]:
            message.append(x["startTime"][5:16] + " " + x["elementValue"][0]["value"])

        for i in message:
            print(i)

message = Get_Predic_3Days("三天預報", "台北市")