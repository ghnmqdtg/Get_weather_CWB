# Get_weather_CWB
## Intro
This python program is to get the weather from the [CWB opendata API](https://opendata.cwb.gov.tw/dist/opendata-swagger.html#/%E9%A0%90%E5%A0%B1/get_v1_rest_datastore_F_D0047_091).

CWB(中央氣象局) stands for Central Weather Bureau, which is a government agency of Taiwan.


## Declaration
The codes are the initial version which can only fetch current weather data. My expectation is not only to fetch current weather but three-days and one-week weather prediction.

## Basic knowledge
You should understand basic **HTTP methods** and **JSON format**. Also, read API instructions and knowing how to get the data you want. The tool in API's website or postman may help to figure out the way you parse the response JSON format data.

## Preparation
Before running the codes, you will need the following packages:
1. configparser: Parse configuration from config.ini.
2. requests: Send requests to API for fetching the data.
3. urllib.parse: Convert Chinese into UTF-8 code.