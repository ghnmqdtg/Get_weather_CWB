import requests
import urllib.parse
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


def Get_Current(functions, location):
    # URL for fetching the current weather
    Request_URL = config["URL"]["observation_auto"]\
        + config["settings"]["Authorization"] + "&format=JSON"\
        + "&locationName=" + urllib.parse.quote(location)

    # data = requests.get(Request_URL).json()
    # print(data)

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

    msg = city + town + " " + functions + "\n"
    msg += "氣溫：" + temp + "℃\n"
    msg += "濕度：" + humidity + "% RH\n"
    # msg += "風向：" + wind_dir + "°\n"
    # msg += "風速：" + wind_speed + " m/s\n"
    print(msg)


Get_Current("目前天氣", "永和")

# Results
'''
新北市永和區 目前天氣
氣溫：33.9℃
濕度：62.0% RH
'''
