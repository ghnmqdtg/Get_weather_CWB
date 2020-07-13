import requests
import urllib.parse
import configparser
import json

config = configparser.ConfigParser()
config.read("config.ini")


def List_Dict_Converter(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


def Get_Predic_3Days(functions, location):
    if(functions == "三天預報"):
        # URL for fetching prediction for 3 days.
        Request_URL = config["URL"]["prediction_3days"]\
            + config["settings"]["Authorization"] + "&format=JSON"\
            + "&locationName=" + urllib.parse.quote(location.replace("台", "臺"))

        response = requests.get(Request_URL)

        # requests.codes.ok == 200
        if(response.status_code == requests.codes.ok):
            # filter out which data we need
            raw = response.json()["records"]["locations"][0]
            function_type = "weather"
            data = raw["location"][0]["weatherElement"]
            list_results = []

            # short form: Wx, PoP, AT
            index = [1, 7, 2]
            # used when coverting list into dict
            keyname = ["Type", "Description", "Location", "Date", "Time", "Wx", "PoP6h", "AT"]

            # Long form: Wx, PoP, AT, T, RH, CI
            '''
            index = [1, 7, 2, 3, 4, 5]
            keyname = ["Type", "Description", "Location", "Date", "Time", "Wx", "PoP6h", "AT", "T", "RH", "CI"]
            '''

            i = 0

            for idx, key in enumerate(index):
                if(idx == 0):
                    for fetch_time in data[key]["time"]:
                        # fetch date
                        date_start = fetch_time["startTime"][5:10]
                        date_end = fetch_time["endTime"][8:10]
                        date = (date_start + "~" + date_end).replace("-", "/")

                        # fetch duration
                        duration_start = fetch_time["startTime"][11:16]
                        duration_end = fetch_time["endTime"][11:16]
                        duration = duration_start + "~" + duration_end

                        # fetch value
                        # value = "|{0:<7}|".format(fetch_time["elementValue"][0]["value"]).replace(" ", "　")
                        value = fetch_time["elementValue"][0]["value"]
                        output = date + " " + duration + " " + value
                        # save results into list
                        list_results.append(output)

                elif(idx == 1):
                    for fetch_time in data[key]["time"]:
                        # value = "{0:>2}".format(fetch_time["elementValue"][0]["value"])
                        value = " " + fetch_time["elementValue"][0]["value"]
                        # output = data[key]["description"][3:] + "：" + value + "%"
                        output = value + "%"
                        list_results[i] = list_results[i] + output
                        list_results[i + 1] = list_results[i + 1] + output
                        i = i + 2

                else:
                    i = 0
                    for fetch_time in data[key]["time"]:
                        value = fetch_time["elementValue"][0]["value"]
                        # output = " " + data[key]["description"] + "：" + value
                        output = " " + value
                        list_results[i] = list_results[i] + output
                        i = i + 1

            # Steps: string > list > dict with keys > final list for output
            for order, content in enumerate(list_results):
                # split the string into list
                list_results[order] = content.split(" ")

                # insert keys into the list which is to be converted into dict
                list_results[order].insert(0, function_type)
                list_results[order].insert(1, functions)
                list_results[order].insert(2, location)

                for num in range(0, len(keyname)):
                    list_results[order].insert(num * 2, keyname[num])
                # print(list_results[order])  # for testing

            # Convert a specified range of data of list into dict
            # Finally append dict into final list
            final_output = []
            for order in range(0, 3):
                final_output.append(List_Dict_Converter(list_results[order]))
            return final_output

        else:
            print("Request fialed, status_code:", response.status_code)
    else:
        print("功能名稱錯誤")


output = Get_Predic_3Days("三天預報", "台北市")

if(output):
    for i in range(0, 3):
        print(json.dumps(output[i], indent=4, ensure_ascii=False))


# Results
'''
{
    "Type": "weather",
    "Description": "三天預報",
    "Location": "台北市",
    "Date": "07/13~13",
    "Time": "18:00~21:00",
    "Wx": "晴",
    "PoP6h": "0%",
    "AT": "36"
}
{
    "Type": "weather",
    "Description": "三天預報",
    "Location": "台北市",
    "Date": "07/13~14",
    "Time": "21:00~00:00",
    "Wx": "晴",
    "PoP6h": "0%",
    "AT": "34"
}
{
    "Type": "weather",
    "Description": "三天預報",
    "Location": "台北市",
    "Date": "07/14~14",
    "Time": "00:00~03:00",
    "Wx": "晴",
    "PoP6h": "0%",
    "AT": "32"
}
'''
