import re
from datetime import datetime
from datetime import timedelta
import base64
import requests
import dataset
import json
import hashlib
import time
import certifi
import pandas as pd
import datetime

ca_bundle_path = certifi.where()


def create_encoded_query(from_date, to_date, state, city, station_id):
    time_part = " T00:00:00Z"
    time_part_end = " T23:59:00Z"

    fromDate = from_date + time_part
    toDate = to_date + time_part_end

    prompt = (
            '{"draw": 1,"columns": [{"data": 0,"name": "","searchable": true,"orderable": false,"search": {"value": '
            '"","regex": false}}],"order": [],"start": 0,"length": 366,"search": {"value": "","regex": false},'
            '"filtersToApply": {"parameter_list": [{"id": 0,"itemName": "PM2.5","itemValue": "parameter_193"},'
            '{"id": 1,"itemName": "PM10","itemValue": "parameter_215"},{"id": 2,"itemName": "NO","itemValue": '
            '"parameter_226"},{"id": 3,"itemName": "NO2","itemValue": "parameter_194"},{"id": 4,"itemName": "NOx",'
            '"itemValue": "parameter_225"},{"id": 5,"itemName": "NH3","itemValue": "parameter_311"},{"id": 6,'
            '"itemName": "SO2","itemValue": "parameter_312"},{"id": 7,"itemName": "CO","itemValue": "parameter_203"},'
            '{"id": 8,"itemName": "Ozone","itemValue": "parameter_222"},{"id": 9,"itemName": "Benzene","itemValue": '
            '"parameter_202"},{"id": 10,"itemName": "Toluene","itemValue": "parameter_232"},{"id": 11,"itemName": '
            '"Eth-Benzene","itemValue": "parameter_216"},{"id": 12,"itemName": "MP-Xylene","itemValue": '
            '"parameter_240"}, {"id": 13,"itemName": "Temp","itemValue": "parameter_198"},{"id": 14,"itemName": "RH",'
            '"itemValue": "parameter_235"},{"id": 15,"itemName": "WS","itemValue": "parameter_233"},{"id": 16,'
            '"itemName": "WD","itemValue": "parameter_234"},{"id": 17,"itemName": "SR","itemValue": "parameter_237"},'
            '{"id": 18,"itemName": "BP","itemValue": "parameter_238"},{"id": 19,"itemName": "VWS","itemValue": '
            '"parameter_239"},{"id": 20,"itemName": "AT","itemValue": "parameter_204"},{"id": 21,"itemName": '
            '"TOT-RF","itemValue": "parameter_37"},{"id": 22,"itemName": "RF","itemValue": "parameter_236"}, '
            '{"id": 23,"itemName": "Xylene","itemValue": "parameter_223"}],"criteria": "24 Hours","reportFormat": '
            '"Tabular","fromDate":"'
            + fromDate
            + '","toDate":"'
            + toDate
            + '","state":"'
            + state
            + '","city":"'
            + city
            + '","station":"'
            + station_id
            + '","parameter":["parameter_193","parameter_215","parameter_226","parameter_194","parameter_225",'
              '"parameter_311","parameter_312","parameter_203","parameter_222","parameter_202","parameter_232",'
              '"parameter_216","parameter_240","parameter_198","parameter_235","parameter_233","parameter_234",'
              '"parameter_237","parameter_238","parameter_239","parameter_204","parameter_37","parameter_236",'
              '"parameter_223"],"parameterNames":["PM2.5","PM10","NO","NO2","NOx","NH3","SO2","CO","Ozone","Benzene",'
              '"Toluene","Eth-Benzene","MP-Xylene","Temp","RH","WS","WD","SR","BP","VWS","AT","TOT-RF","RF",'
              '"Xylene"]},"pagination":1}'
    )

    data_to_encode = prompt
    encoded_data = base64.b64encode(data_to_encode.encode("UTF8"))
    return encoded_data


def get_info(encoded_data):
    headers = {"Origin": "https://airquality.cpcb.gov.in"}
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Accept-Language"] = "en-US,en;q=0.9"
    headers[
        "User-Agent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/119.0.0.0 Safari/537.36")
    headers["Content-Type"] = "text/plain"
    headers["Accept"] = "q=0.8;application/json;q=0.9"
    headers["Referer"] = "https://airquality.cpcb.gov.in/ccr/"
    headers[
        "Cookie"] = 'ccr_captcha="qXZLyHHyg3+1W946WbGqOTZmtJ2hlw/KRAUMjpfhcKeMs3abkfk0OI8fD6axdm4+EAhBuouxf2Uu7bY9qlWtc8gWBaPPVNkOCZ1nZG0D47aIi/J0faTb+TUkKRjl+eiNi9+vV6A0pwC6PpGH3IhskUajmNxL5vsLweoCrndDzWVewvmD/oAnHG+ucNnMmgS9Yt6la5zlIaNsAO0+yl1ZJfpSsRsNr9+I2pitpE2JxUubZvFCvcLNT/fX3FyWq5owZyZw7e9fbgy/JPFN1lqECg=="; ccr_public="+QGlzUA5qj0oN4ur6qPz/8VEycd3MhdpZG/YcjLkRhwW9rS5iw2fYx9Q6WHVUQUa3ZzcddRsOFzDnMqyw7bEdQ+g+oXvrYfLdYNeH3J4rUYOGVHoybZ9zciFiGpL/CJgEEllwrMNH61cGUuwFcyrqH3QKi0VX0GjrN+YUmxzjm5n+YQiej8FsYfCCRc+d5m5JRpClxYVPXlmuxhq+oIiV1K8idVOVfHJj33QKWvXDqo4C+jrBqpZJDCS5f7lLJKTD0hRohYLTbRg9eum3G3K1oioCuqNTrZXEGreF15AOG4/u2i2Hkt+riFqemua0y9YZ1YEXP8s+MNXfRb5mmcSw3byERE29YM6OjmyXe9WyX0="'
    r = requests.post(
        "https://airquality.cpcb.gov.in/caaqms/fetch_table_data",
        headers=headers,
        data=encoded_data,
        verify=ca_bundle_path,
    )

    if r.status_code == 200:
        print("Awesome response code 200")
        encoded = r.content
        header_part, _, _ = encoded.partition(b".")
        decoded_header_bytes = base64.urlsafe_b64decode(header_part + b'=' * (4 - len(header_part) % 4))
        json_data = decoded_header_bytes.decode('utf-8')
        json_data = json.loads(json_data)
        data = json_data["data"]
        tabularData = data["tabularData"]
        bodyContent = tabularData["bodyContent"]
        return bodyContent


def to_int(str):
    if str:
        return float(str)


def printing_lines(body_content):
    ret_final = []
    for line in body_content:
        from_date = line["from date"]
        to_date = line["to date"]
        pm25 = to_int(line["PM2.5"])
        pm10 = to_int(line["PM10"])
        no = to_int(line["NO"])
        no2 = to_int(line["NO2"])
        nox = to_int(line["NOx"])
        nh3 = to_int(line["NH3"])
        so2 = to_int(line["SO2"])
        co = to_int(line["CO"])
        ozone = to_int(line["Ozone"])
        benzene = to_int(line["Benzene"])
        toluene = to_int(line["Toluene"])
        eth = to_int(line["Eth-Benzene"])
        mp_xy = to_int(line["MP-Xylene"])
        temp = to_int(line["Temp"])
        rh = to_int(line["RH"])
        ws = to_int(line["WS"])
        wd = to_int(line["WD"])
        sr = to_int(line["SR"])
        bp = to_int(line["BP"])
        vws = to_int(line["VWS"])
        at = to_int(line["AT"])
        tot_rf = to_int(line["TOT-RF"])
        rf = to_int(line["RF"])
        xylene = to_int(line["Xylene"])
        ret = [from_date, to_date, pm25, pm10, no, no2, nox, nh3, so2, co, ozone, benzene, toluene, eth, mp_xy, temp,
               rh, ws, wd, sr, bp, vws, at, tot_rf, rf, xylene]
        ret_final.append(ret)
    return ret_final


def testing():
    test = printing_lines(get_info(create_encoded_query("10-12-2023", "31-12-2023", "Chhattisgarh", "Bhilai", "site_5659")))
    for lines in test:
        print(lines)


def create_final():
    final = pd.DataFrame(
        columns=["State", "City", "Station_id", "Station_name", "From_Date", "To_Date", "PM2.5", "PM10", "NO", "NO2",
                 "NOx", "NH3", "SO2", "CO", "Ozone", "Benzene", "Toluene", "Eth-Benzene", "MP-Xylene", "Temp", "RH",
                 "WS", "WD", "SR", "BP", "VWS", "AT", "TOT-RF", "RF", "Xylene"])
    print(final)
    final.to_excel("Final_AQI.xlsx", index=False)


def run_final():
    sites = pd.read_excel("sites_all.xlsx")
    final = pd.read_excel("Final_AQI.xlsx")
    from_date = "10-12-2023"  # TODO modify this DD-MM-YYY
    to_date = "31-12-2023"  # TODO modify this DD-MM-YYY

    k = 1
    for i in range(len(sites["state"])):
        state = sites["state"][i]
        city = sites["city"][i]
        site_id = sites["site"][i]
        site_name = sites["site_name"][i]
        parsed = sites["parsed"][i]

        if parsed == 0:
            print(f"+{i}+{k}"*30)
            info = [state, city, site_id, site_name]
            print(info)
            ret = printing_lines(get_info(create_encoded_query(from_date, to_date, state, city, site_id)))
            for a_line in ret:
                to_return = info + a_line
                print(to_return[4:])
                final.loc[len(final.index)] = to_return
                pass
            sites["parsed"][i] = 1
            k += 1
        else:
            pass
        if k == 89:
            sites[["state", "city", "site", "site_name", "parsed"]].to_excel("sites_all.xlsx")
            final[["State", "City", "Station_id", "Station_name", "From_Date", "To_Date", "PM2.5", "PM10", "NO", "NO2",
                   "NOx", "NH3", "SO2", "CO", "Ozone", "Benzene", "Toluene", "Eth-Benzene", "MP-Xylene", "Temp", "RH",
                   "WS", "WD", "SR", "BP", "VWS", "AT", "TOT-RF", "RF", "Xylene"]].to_excel("Final_AQI.xlsx", index=False)
            break

    sites[["state", "city", "site", "site_name", "parsed"]].to_excel("sites_all.xlsx")
    final[["State", "City", "Station_id", "Station_name", "From_Date", "To_Date", "PM2.5", "PM10", "NO", "NO2",
           "NOx", "NH3", "SO2", "CO", "Ozone", "Benzene", "Toluene", "Eth-Benzene", "MP-Xylene", "Temp", "RH",
           "WS", "WD", "SR", "BP", "VWS", "AT", "TOT-RF", "RF", "Xylene"]].to_excel("Final_AQI.xlsx", index=False)


print(datetime.datetime.now()) # Start time for code
run_final()
print(datetime.datetime.now()) # End time for code
