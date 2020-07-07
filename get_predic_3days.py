import requests
import urllib.parse
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


def Get_Predic_3Days(functions, location):
    if(functions == "三天預報"):
        # URL for fetching prediction for 3 days.
        Request_URL = config["URL"]["prediction_3days"]\
            + config["settings"]["Authorization"] + "&format=JSON"\
            + "&locationName=" + urllib.parse.quote(location.replace("台", "臺"))

        # filter out which data we need
        raw = requests.get(Request_URL).json()["records"]["locations"][0]
        function = raw["datasetDescription"][:11] + "天氣預報"
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

        print(function + "：" + location)
        for content in list_results:
            print(content)

    else:
        print("功能名稱錯誤")


Get_Predic_3Days("三天預報", "台北市")

# Results
'''
臺灣各縣市鄉鎮未來3天天氣預報：台北市
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

'''
(X) data[0]: PoP12h 12小時降雨機率(間隔太久)
(O) data[1]: Wx 天氣現象
(O) data[2]: AT 體感溫度
(O) data[3]: T  溫度
(O) data[4]: RH 相對溼度
(O) data[5]: CI 舒適度指數
(X) data[6]: 天氣預報綜合描述(要的資料通通都有，但是難以分類)
(O) data[7]: PoP6h 6小時降雨機率
(X) data[8]: WS 風速
(X) data[9]: WD 風向
(X) data[10]: Td 露點溫度
'''
