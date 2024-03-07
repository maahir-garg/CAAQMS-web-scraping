# Python Script for Web Scraping Air Quality Data
This Python script scrapes air quality data from a website and saves it to an Excel sheet.

## Functionality
Reading Websites and IDs:
The script reads a list of sites and details such as State, City, Site_ID from an Excel sheet ("sites_all.xlsx").
This list can be modified to include different sites. 

### Creating Encoded Queries:
For each site, the script generates an encoded query based on the from_date, to_date, state, city, station_id 
using the function create_encoded_query.

### Web Scraping:
The script retrieves HTML content from the website using the encoded queries in the function get_info.

#### Updating CAPTCHA
This is perhaps the most important part of the code to ensure it it actually running. \
Click on [this link](https://airquality.cpcb.gov.in/ccr/#/caaqm-dashboard-all/caaqm-landing) to access the page. 
<img width="1015" alt="Screenshot 2024-03-07 at 10 13 57 PM" src="https://github.com/maahir-garg/CAAQMS-web-scraping/assets/117061563/1f533df6-cdef-46e4-b67e-cdfbe1b7fa02">

 \
Enter the correct captcha and then open the inspect panel by right clicking. \
Next select networks -> ccr and choose headers 

<img width="1015" alt="Screenshot 2024-03-07 at 10 14 08 PM" src="https://github.com/maahir-garg/CAAQMS-web-scraping/assets/117061563/b0cf5441-f384-489c-afb0-c8d2ed405f47">

Copy the Cookie element and paste in the headers
```python
headers["Cookie"] = '#paste copied element here and DONT remove the single quotations'
```

### Data Extraction:
The script extracts relevant air quality data from the HTML content. Function printing_lines

#### Data Saving:
The script saves the extracted data to a new Excel sheet ("Final_AQI.xlsx"). 

## Installation and Usage

### Install Requirements:
This script requires the following Python libraries:
pandas
requests
certifi
You can install them using 
```bash
pip install pandas 
pip install requests 
pip install certifi 
```
### Download Files:
Download the following files:
air_quality.py: The Python script that performs the web scraping. \
sites_all.xlsx: The Excel sheet containing the list all sites. \
Final_AQI.xlsx: The Excel sheet storing the final output. 

### Run the Script:
Open a terminal and navigate to the directory containing the downloaded files.
Run the following command:
```bash 
python air_quality.py
```

### Output:
The script will update the excel sheet ("Final_AQI.xlsx") in the same directory.
This sheet will contain the extracted air quality data for all specified sites.

