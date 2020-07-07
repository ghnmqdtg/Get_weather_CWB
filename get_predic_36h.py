import requests
import urllib.parse
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


def Get_36hours(functions, location):
    if(functions == "三天預報"):
        # URL for fetching the current weather
        Request_URL = config["URL"]["prediction_36hours"]\
            + config["settings"]["Authorization"] + "&format=JSON"\
            + "&locationName=" + urllib.parse.quote(location)

        # filter out which data we need
        raw = requests.get(Request_URL).json()["records"]
        function = raw["datasetDescription"]
        data = raw["location"][0]

        # examine if the location is valid
        if not data:
            predict_data = "target city not found"
            # print(target_station)
            return False

        # load message
        # ref: https://opendata.cwb.gov.tw/opendatadoc/DIV2/A0001-001.pdf
        predict_data = data["weatherElement"]
        city = data["locationName"]
        list_results = []

        # fetch three intervals of time
        for fetch_time in predict_data[0]["time"]:
            # fetch date
            date_start = fetch_time["startTime"][5:10].replace("-", "/")
            date_end = fetch_time["endTime"][8:10]
            date = date_start + "~" + date_end

            # fetch duration
            duration_start = fetch_time["startTime"][11:16]
            duration_end = fetch_time["endTime"][11:16]
            duration = duration_start + "~" + duration_end

            # save results into list
            list_results.append(date + " " + duration)

        i = 0
        j = 0

        for x in predict_data:
            for y in x["time"]:
                situation = y["parameter"]["parameterName"]
                if(i % 3 == 1):
                    situation = situation + "%"
                elif(i % 3 == 2 or i % 3 == 4):
                    situation = situation + "℃"

                # update the list with Wx, Pop, MinT, CI and MaxT
                list_results[j % 3] += " " + situation
                j = j + 1

            i = i + 1

        print(function + "：" + city)
        for content in list_results:
            print(content)

    else:
        print("功能名稱錯誤")


Get_36hours("目前天氣", "臺北市")

# Results
'''
三十六小時天氣預報：臺北市
07/07~07 12:00~18:00 多雲午後短暫雷陣雨 40% 32℃ 悶熱至易中暑 36%
07/07~08 18:00~06:00 多雲 0% 27℃ 舒適至悶熱 32%
07/08~08 06:00~18:00 晴午後短暫雷陣雨 30% 27℃ 舒適至悶熱 36%
'''
