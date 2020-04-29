import requests
import urllib.parse

def GetWeather(station):
    Request_URL = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=CWB-FC8F10B8-9C7B-4CE1-A95C-D367619E3E1C"\
         + "&format=JSON" + "&locationName=" + urllib.parse.quote(station)

    # print(Request_URL)
    data = requests.get(Request_URL).json()

    data = data["records"]["location"]
    # print("\n\n", data)

    if not data:
        target_station = "target station not found"
        # print(target_station)
    else:
        target_station = data[0]

    return target_station


def MakeWeather(station):
    WeatherData = GetWeather(station)
    # print(WeatherData)
    if WeatherData == "target station not found":
        return False

    WeatherData = WeatherData["weatherElement"]
    msg = station + "天氣"
    msg += "\n\n氣溫 = " + WeatherData[3]["elementValue"] + "℃\n"
    msg += "濕度 = " + \
        str(float(WeatherData[4]["elementValue"]) * 100) + "% RH\n"

    print(msg)


MakeWeather("永和")
