import requests
import urllib.parse
import configparser


config = configparser.ConfigParser()
config.read("config.ini")


class Get_Weather:
    def __init__(self, functions, location):
        self.functions = functions
        self.location = location

    def Get_Current(self):
        # URL for fetching the current weather
        Request_URL = config["URL"]["observation_auto"]\
            + config["settings"]["Authorization"] + "&format=JSON"\
            + "&locationName=" + urllib.parse.quote(self.location)

        # filter out which data we need
        data = requests.get(Request_URL).json()["records"]["location"]

        # examine if the location is valid
        if not data:
            observed_data = "target station not found"
            # print(target_station)
            return False

        # load message
        # ref: https://opendata.cwb.gov.tw/opendatadoc/DIV2/A0001-001.pdf
        city = data[0]["parameter"][0]["parameterValue"]
        town = data[0]["parameter"][2]["parameterValue"]
        observed_data = data[0]["weatherElement"]

        temp = observed_data[3]["elementValue"]
        humidity = str(float(observed_data[4]["elementValue"]) * 100)
        # wind_dir = observed_data[1]["elementValue"]
        # wind_speed = observed_data[0]["elementValue"]

        msg = city + town + " " + self.functions + "\n\n"
        msg += "氣溫：" + temp + "℃\n"
        msg += "濕度：" + humidity + "% RH\n"
        # msg += "風向：" + wind_dir + "°\n"
        # msg += "風速：" + wind_speed + " m/s\n"
        city = msg
        print(city)

    def GetPredic(self):
        pass

    def GetPredic_Week(self):
        pass

    def Get_Predic_3Days(self):
        # URL for fetching prediction for 3 days.
        Request_URL = config["URL"]["prediction_3days"]\
            + config["settings"]["Authorization"] + "&format=JSON"\
            + "&locationName=" + urllib.parse.quote(self.location.replace("台", "臺"))

        # filter out which data we need
        data = requests.get(Request_URL).json()["records"]["locations"][0]["location"][0]["weatherElement"]
        # print(type(data))

        message = []
        for x in data[6]["time"]:
            message.append(x["startTime"][5:16] + " " + x["elementValue"][0]["value"])

        for i in message:
            print(i)


message = Get_Weather("目前天氣", "永和").Get_Current()
message = Get_Weather("三天預報", "台北市")
'''
print(message.functions)
print(message.location)
'''
# message.Get_Current()
message.Get_Predic_3Days()
