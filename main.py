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
        if(self.functions == "目前天氣"):
            # URL for fetching the current weather
            Request_URL = config["URL"]["observation_auto"]\
                + config["settings"]["Authorization"] + "&format=JSON"\
                + "&locationName=" + urllib.parse.quote(self.location)

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
            town = self.location
            observed_data = data[0]["weatherElement"]

            temp = observed_data[3]["elementValue"]
            humidity = str(float(observed_data[4]["elementValue"]) * 100)
            # wind_dir = observed_data[1]["elementValue"]
            # wind_speed = observed_data[0]["elementValue"]

            msg = city + town + " " + self.functions + "\n"
            msg += "氣溫：" + temp + "℃\n"
            msg += "濕度：" + humidity + "% RH"
            # msg += "風向：" + wind_dir + "°\n"
            # msg += "風速：" + wind_speed + " m/s\n"
            print(msg)

        else:
            print("功能名稱錯誤")

    def Get_Predic_36hours(self):
        if(self.functions == "36小時預報"):
            # URL for fetching the current weather
            Request_URL = config["URL"]["prediction_36hours"]\
                + config["settings"]["Authorization"] + "&format=JSON"\
                + "&locationName=" + urllib.parse.quote(self.location)

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
            city = self.location
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

    def Get_Predic_3Days(self):
        if(self.functions == "三天預報"):
            # URL for fetching prediction for 3 days.
            Request_URL = config["URL"]["prediction_3days"]\
                + config["settings"]["Authorization"] + "&format=JSON"\
                + "&locationName=" + urllib.parse.quote(self.location.replace("台", "臺"))

            # filter out which data we need
            raw = requests.get(Request_URL).json()["records"]["locations"][0]
            function = raw["datasetDescription"][:11] + self.functions
            data = raw["location"][0]["weatherElement"]
            list_results = []
            index = [1, 7, 2, 3, 4, 5]

            i = 0

            for idx, key in enumerate(index):
                if(idx == 0):
                    for fetch_time in data[key]["time"]:
                        # fetch date
                        date_start = fetch_time["startTime"][5:10].replace("-", "/")
                        date_end = fetch_time["endTime"][8:10]
                        date = date_start + "~" + date_end

                        # fetch duration
                        duration_start = fetch_time["startTime"][11:16]
                        duration_end = fetch_time["endTime"][11:16]
                        duration = duration_start + "~" + duration_end

                        # fetch value
                        value = "|{0:<7}|".format(fetch_time["elementValue"][0]["value"]).replace(" ", "　")
                        output = date + " | " + duration + " " + value
                        # save results into list
                        list_results.append(output)

                elif(idx == 1):
                    for fetch_time in data[key]["time"]:
                        value = "{0:>2}".format(fetch_time["elementValue"][0]["value"])
                        output = data[key]["description"][3:] + "：" + value + "%"
                        list_results[i] = list_results[i] + output
                        list_results[i + 1] = list_results[i + 1] + output
                        i = i + 2

                else:
                    i = 0
                    for fetch_time in data[key]["time"]:
                        value = fetch_time["elementValue"][0]["value"]
                        output = " | " + data[key]["description"] + "：" + value
                        list_results[i] = list_results[i] + output
                        i = i + 1

            print(function + "：" + self.location)
            for content in list_results:
                print(content)

        else:
            print("功能名稱錯誤")


message = Get_Weather("目前天氣", "永和").Get_Current()
print("\n")
message = Get_Weather("36小時預報", "臺北市").Get_Predic_36hours()
print("\n")
message = Get_Weather("三天預報", "台北市").Get_Predic_3Days()
print("\n")

# Results
'''
# Get_Current()
新北市永和 目前天氣
氣溫：29.4℃
濕度：100.0% RH

# Get_Predic_36hours()
三十六小時天氣預報：臺北市
07/08~08 00:00~06:00 多雲 0% 27℃ 舒適至悶熱 29%
07/08~08 06:00~18:00 晴午後短暫雷陣雨 30% 27℃ 舒適至易中暑 36%
07/08~09 18:00~06:00 陰時多雲 20% 27℃ 舒適至悶熱 32%

# Get_Predic_3Days()
臺灣各縣市鄉鎮未來3天三天預報：台北市
07/08~08 | 00:00~03:00 |多雲　　　　　|降雨機率： 0% | 體感溫度：33 | 溫度：29 | 相對濕度：81 | 舒適度指數：27
07/08~08 | 03:00~06:00 |多雲　　　　　|降雨機率： 0% | 體感溫度：32 | 溫度：28 | 相對濕度：81 | 舒適度指數：26
07/08~08 | 06:00~09:00 |多雲　　　　　|降雨機率：10% | 體感溫度：30 | 溫度：27 | 相對濕度：76 | 舒適度指數：25
07/08~08 | 09:00~12:00 |晴　　　　　　|降雨機率：10% | 體感溫度：35 | 溫度：32 | 相對濕度：57 | 舒適度指數：28
07/08~08 | 12:00~15:00 |午後短暫雷陣雨|降雨機率：30% | 體感溫度：43 | 溫度：36 | 相對濕度：80 | 舒適度指數：34
07/08~08 | 15:00~18:00 |晴　　　　　　|降雨機率：30% | 體感溫度：39 | 溫度：35 | 相對濕度：55 | 舒適度指數：30
07/08~08 | 18:00~21:00 |陰　　　　　　|降雨機率：20% | 體感溫度：36 | 溫度：32 | 相對濕度：58 | 舒適度指數：28
07/08~09 | 21:00~00:00 |多雲　　　　　|降雨機率：20% | 體感溫度：34 | 溫度：30 | 相對濕度：62 | 舒適度指數：27
07/09~09 | 00:00~03:00 |陰　　　　　　|降雨機率：20% | 體感溫度：31 | 溫度：29 | 相對濕度：54 | 舒適度指數：25
07/09~09 | 03:00~06:00 |多雲　　　　　|降雨機率：20% | 體感溫度：30 | 溫度：28 | 相對濕度：59 | 舒適度指數：25
07/09~09 | 06:00~09:00 |多雲　　　　　|降雨機率：20% | 體感溫度：31 | 溫度：27 | 相對濕度：78 | 舒適度指數：26
07/09~09 | 09:00~12:00 |陰　　　　　　|降雨機率：20% | 體感溫度：34 | 溫度：31 | 相對濕度：57 | 舒適度指數：27
07/09~09 | 12:00~15:00 |午後短暫雷陣雨|降雨機率：30% | 體感溫度：41 | 溫度：34 | 相對濕度：80 | 舒適度指數：32
07/09~09 | 15:00~18:00 |多雲　　　　　|降雨機率：30% | 體感溫度：38 | 溫度：33 | 相對濕度：56 | 舒適度指數：29
07/09~09 | 18:00~21:00 |多雲　　　　　|降雨機率：10% | 體感溫度：35 | 溫度：31 | 相對濕度：64 | 舒適度指數：28
07/09~10 | 21:00~00:00 |多雲　　　　　|降雨機率：10% | 體感溫度：33 | 溫度：29 | 相對濕度：69 | 舒適度指數：27
07/10~10 | 00:00~03:00 |多雲　　　　　|降雨機率：10% | 體感溫度：32 | 溫度：28 | 相對濕度：79 | 舒適度指數：27
07/10~10 | 03:00~06:00 |多雲　　　　　|降雨機率：10% | 體感溫度：31 | 溫度：27 | 相對濕度：81 | 舒適度指數：26
07/10~10 | 06:00~09:00 |多雲　　　　　|降雨機率：10% | 體感溫度：30 | 溫度：27 | 相對濕度：77 | 舒適度指數：25
07/10~10 | 09:00~12:00 |晴　　　　　　|降雨機率：10% | 體感溫度：35 | 溫度：31 | 相對濕度：60 | 舒適度指數：28
07/10~10 | 12:00~15:00 |午後短暫雷陣雨|降雨機率：30% | 體感溫度：43 | 溫度：35 | 相對濕度：80 | 舒適度指數：33
07/10~10 | 15:00~18:00 |晴　　　　　　|降雨機率：30% | 體感溫度：38 | 溫度：34 | 相對濕度：55 | 舒適度指數：29
07/10~10 | 18:00~21:00 |晴　　　　　　|降雨機率： 0% | 體感溫度：36 | 溫度：32 | 相對濕度：69 | 舒適度指數：29
07/10~11 | 21:00~00:00 |晴　　　　　　|降雨機率： 0% | 體感溫度：34 | 溫度：30 | 相對濕度：75 | 舒適度指數：28
'''
