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
            data = raw["location"][0]["weatherElement"]

            function_type = "Weather"
            description = functions
            list_results = []

            # short form: Wx, PoP, AT
            index = [1, 7, 2]
            # used when coverting list into dict
            dict_output = {
                "Type": function_type,
                "Description": description,
                "Location": location,
                "Prediction": []
            }
            keyname = ["Date", "Time", "Wx", "PoP6h", "AT"]

            # Long form: Wx, PoP, AT, T, RH, CI
            # index = [1, 7, 2, 3, 4, 5]
            # keyname = ["Date", "Time", "Wx", "PoP6h", "AT", "T", "RH", "CI"]

            i = 0
            # Categorize data into strings
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
                        value = fetch_time["elementValue"][0]["value"]
                        output = date + " " + duration + " " + value
                        # save results into list
                        list_results.append(output)

                elif(idx == 1):
                    for fetch_time in data[key]["time"]:
                        value = " " + fetch_time["elementValue"][0]["value"]
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

            # Prepar for the output dict
            # Steps: string > split into list > save into the list in dict
            load = dict_output["Prediction"]
            i = 0
            for order, content in enumerate(list_results):
                # determine how many data to be loaded
                if(i < 4):
                    # split the string into list
                    list_results[order] = content.split(" ")

                    for num in range(0, len(keyname)):
                        list_results[order].insert(num * 2, keyname[num])

                    load.append(List_Dict_Converter(list_results[order]))
                i = i + 1

            return dict_output

        else:
            print("Request fialed, status_code:", response.status_code)
    else:
        print("功能名稱錯誤")


output = Get_Predic_3Days("三天預報", "台北市")

if(output):
    # JSON format
    print(json.dumps(output, indent=4, ensure_ascii=False))

# Results_JSON_format
'''
{
    "Type": "Weather",
    "Description": "三天預報",
    "Location": "台北市",
    "Prediction": [
        {
            "Date": "07/14~14",
            "Time": "00:00~03:00",
            "Wx": "晴",
            "PoP6h": "0%",
            "AT": "32"
        },
        {
            "Date": "07/14~14",
            "Time": "03:00~06:00",
            "Wx": "多雲",
            "PoP6h": "0%",
            "AT": "31"
        },
        {
            "Date": "07/14~14",
            "Time": "06:00~09:00",
            "Wx": "晴",
            "PoP6h": "0%",
            "AT": "30"
        },
        {
            "Date": "07/14~14",
            "Time": "09:00~12:00",
            "Wx": "晴",
            "PoP6h": "0%",
            "AT": "37"
        }
    ]
}
'''
