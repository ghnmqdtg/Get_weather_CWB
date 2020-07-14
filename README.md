# Get_weather_CWB
## Intro
This python program is to get the weather from the [CWB opendata API](https://opendata.cwb.gov.tw/dist/opendata-swagger.html#/%E9%A0%90%E5%A0%B1/get_v1_rest_datastore_F_D0047_091).

CWB(中央氣象局) stands for Central Weather Bureau, which is a government agency of Taiwan.

## Functions
The main.py includes the following three functions:
1. Get current weather
2. Get 36 hours prediction
3. Get 3 days prediction

All of these functions send the request to different APIs and get different responses. I filter them out and get different outputs.

In the latest version(2020/07/13), the output of the first two functions has no JSON format. 

## Basic knowledge
You should understand basic **HTTP methods** and **JSON format**. Also, read API instructions and knowing how to get the data you want. The tool in API's website or postman may help to figure out the way you parse the response JSON format data.

## Requirements
The program can run normally in **python 3.6.8(64 bits) and 3.8.4(64 bits)**.

While other versions, I don't know.

Before running the codes, you will need the following packages:
1. configparser: Parse configuration from config.ini.
2. requests: Send requests to API for fetching the data.
3. urllib.parse: Convert Chinese into UTF-8 code.

You can run the following instruction in the CMD or PowerShell to install them:
```
pip install -r requirements.txt
```