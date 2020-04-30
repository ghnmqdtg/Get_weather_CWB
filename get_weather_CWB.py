import requests
import urllib.parse
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

def CurrentWeather(functions, location):
    # URL for fetching the current weather
        Request_URL = config["URL"]["observation_auto"]\
            + config["settings"]["Authorization"] + "&format=JSON"\
            + "&locationName=" + urllib.parse.quote(location)

        # filter out which data we need
        data = requests.get(Request_URL).json()["records"]["location"]

        # examine if the location is valid
        if not data:
            WeatherData = "target station not found"
            # print(target_station)
            return False

        # load message
        # ref: https://opendata.cwb.gov.tw/opendatadoc/DIV2/A0001-001.pdf
        CITY = data[0]["parameter"][0]["parameterValue"]
        TOWN = data[0]["parameter"][2]["parameterValue"]
        WeatherData = data[0]["weatherElement"]

        msg = CITY + TOWN + " " + functions + "\n\n"
        msg += "氣溫：" + WeatherData[3]["elementValue"] + "℃\n"
        msg += "濕度：" + \
            str(float(WeatherData[4]["elementValue"]) * 100) + "% RH\n"
        msg += "風向：" + WeatherData[1]["elementValue"] + "°\n"
        msg += "風速：" + WeatherData[0]["elementValue"] + " m/s\n"
        city = msg
        print(city)


CurrentWeather("目前天氣", "永和")
