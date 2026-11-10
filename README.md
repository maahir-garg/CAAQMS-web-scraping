# CAAQMS web scraping

A Python script that exports air-quality readings from the CAAQMS portal of India's Central Pollution Control Board (CPCB) to Excel. It was built to collect data for an air-quality study.

## Context and status

The script was written between September 2023 and January 2024 as research-support tooling. It is kept for reference and is not maintained. The portal's endpoint and request format may have changed since, so it may no longer work as written.

## What is in the repo

- `air_quality.py`: builds the request for each monitoring station, posts it to the portal, decodes the response, and appends the readings to a workbook.
- `sites_all.xlsx`: the station list the script iterates over, with columns `state`, `city`, `site`, `site_name` and `parsed`. Stations with `parsed` equal to 0 are fetched, and the flag is set to 1 afterwards so that an interrupted run can resume.
- `Final_AQI.xlsx`: the collected readings (about 19 MB), one row per station and 24-hour period as written by the script, with the columns `State`, `City`, `Station_id`, `Station_name`, `From_Date`, `To_Date` and one column for each of 24 parameters: PM2.5, PM10, NO, NO2, NOx, NH3, SO2, CO, Ozone, Benzene, Toluene, Eth-Benzene, MP-Xylene, Temp, RH, WS, WD, SR, BP, VWS, AT, TOT-RF, RF and Xylene. The data is public government data published on the CPCB portal.
- `requirements.txt`: the third-party libraries the script imports.
- `.env.example`: the environment variable the script reads, with no value.

## Requirements and setup

Python 3 and the packages in `requirements.txt` (`certifi`, `dataset`, `pandas`, `requests`). Reading and writing `.xlsx` files through pandas also needs an Excel engine such as `openpyxl`, which is not imported directly and so is not in `requirements.txt`. The `dataset` package is imported but not used by the code.

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt openpyxl
```

Configuration: the script sends a `Cookie` header taken from the `CAAQMS_COOKIE` environment variable and raises an error if it is not set. The value is never stored in the repository. To use the script, copy a current session value from your own browser into the environment variable (see `.env.example`). Do not commit it.

## Usage

The script takes no command-line arguments. The date range is set by the `from_date` and `to_date` variables at the top of `run_final()`, in `DD-MM-YYYY` format, and they are currently set to 10-12-2023 and 31-12-2023. Edit them before running.

```
python air_quality.py
```

- Input: `sites_all.xlsx` and an existing `Final_AQI.xlsx` in the current directory. `create_final()` writes an empty `Final_AQI.xlsx` with the right columns, but nothing calls it, so call it once from a Python session if you are starting from scratch.
- Request: one request per unfetched station, asking for 24-hour averages of the 24 parameters listed above over the date range.
- Output: the readings are appended to `Final_AQI.xlsx`, and `sites_all.xlsx` is rewritten with updated `parsed` flags. Both files are overwritten in place.
- Batching: the script stops after 88 stations in one run, saves both files, and can be run again to continue.

## Notes and limits

- The script calls an undocumented endpoint of the CPCB portal (`/caaqms/fetch_table_data`) and mimics a browser request. Check the portal's terms of use before running it, and keep request volumes low.
- Empty values in the response are stored as missing. Values are converted to floating point numbers without any unit check or validation, so validate the workbook before analysis.
- `sites_all.xlsx` is written back with its row index, so an extra index column is added on each save.
- The cookie must come from a session you have opened yourself on the portal. The script cannot work without it.
