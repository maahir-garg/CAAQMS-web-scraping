# CAAQMS air-quality data export

This Python script reads station metadata from `sites_all.xlsx`, requests tabular air-quality data from the CPCB CAAQMS service, and appends the results to `Final_AQI.xlsx`.

## Security

The script reads the request cookie from the `CAAQMS_COOKIE` environment variable. Treat this value as a secret.

- Never paste cookies, session values, or credentials into source code.
- Never commit a populated `.env` file.
- Revoke or invalidate exposed session material before using the repository.
- Run a full-history secret scan before treating the repository as clean.

## Requirements

- Python 3
- pandas
- requests
- certifi
- dataset
- openpyxl

Install the dependencies in a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas requests certifi dataset openpyxl
```

## Configuration

Copy the example configuration and provide the current session value only in your local environment:

```bash
cp .env.example .env
export CAAQMS_COOKIE="replace-with-a-current-local-value"
```

The `.env` file is ignored by Git. The script fails with a clear error when `CAAQMS_COOKIE` is missing.

## Inputs and outputs

- `sites_all.xlsx`: station metadata and parse status
- `Final_AQI.xlsx`: generated workbook containing the collected readings
- `air_quality.py`: request, parsing, and workbook-update logic

Review the station list and date range in `air_quality.py` before running:

```bash
python air_quality.py
```

## Limitations

The upstream endpoint, CAPTCHA flow, request headers, and response format can change without notice. Use conservative request rates, comply with the service's terms, and validate generated workbooks before analysis.
