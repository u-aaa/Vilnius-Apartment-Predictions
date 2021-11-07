# Vilnius Apartment Prediction App
## Description
This project was carried out to help users estimate the prices for apartments in Vilnius, Lithuania.
Looking for a new apartment can be daunting and this app aims to help user estimate how much they should be budgeting for their dream home.
The project is divided into two parts.
* The Aruodas web-scraper
* The Apartment prediction app

## The Aruodas Web-scraper
This web_scraper is designed to collect the following information for apartments listed on the [Aruodas website](https://en.aruodas.lt/).
* City
* Sub-district
* Description
* Link
* Building number
* Flat number
* Area
* Price per month
* Build year
* Building type
* Heating system
* Energy class
* Nearest kindergarten
* Nearest educational institution
* Nearest stop
* Nearest public transport stop

The scraper has 3 methods:
* scrape - Loops through webpages and scrapes data off the [aruodas.lt](https://en.aruodas.lt/) website.
* to_csv - Used to save the dataframe to csv
* scrape_to_csv - Used to scrape and save the data to csv

### Usage
To use the scaper, pip install the package.
```python
pip install vilnius-aruodas-scraper

from aruodas_scraper import AruodasScraper

one_four_rooms = AruodasScraper()

# to scrape and data
df = one_four_rooms.scrape(num_houses=1000, room_min=1, room_max=4)

# to save scraped data to csv
one_four_rooms.to_csv(df)

# to scrape and save data to csv
one_four_rooms.scrape_to_csv(num_houses=1000, room_min=1, room_max=4)

```


## The Apartment Prediction App
The apartment prediction can be found here - [Vilnius Apartment Prediction API](https://vilnius-apartment-price.herokuapp.com/).
To predict apartment prices using the app, send a post request to the `/predict` endpoint [here]( https://vilnius-apartment-price.herokuapp.com/predict).
The `/predict` endpoint takes only POST requests. The see the results from the last 10 predictions, use the `/predictions` endpoint [here]( https://vilnius-apartment-price.herokuapp.com/predictions).

### Usage
Post request should be made with the following features - ['division', 'no_of_rooms', 'area', 'floor', 'no_of_floors',
'build_year', 'building_type', 'nearest_kindergarten', 'nearest_educational_institution', 'nearest_shop', 'public_transport_stop']

```python
import json

url = "https://b-house-predic.herokuapp.com/predict"
data = data = [{
    "division": "Šnipiškės",
    "area":  71.78,
    "no_of_rooms":  2,
    "build_year":  1940,
    "floor":  1,
    "nearest_kindergarten": 120,
    "nearest_educational_institution": 310.0,
    "nearest_shop": 170.0,
    "public_transport_stop": 80.0,
    "building_type": "Brick",
    "no_of_floors": 3}]

post_data = json.dumps(data)
resp = requests.post(url, data=post_data)
print(resp.status_code, resp.content)
```
For multiple listings, data can be passed as shown.
```python
import json

url = "https://b-house-predic.herokuapp.com/predict"
data = data1 = [{
    "division": "Lazdynai",
    "area":  48,
    "no_of_rooms":  2,
    "build_year":  1971,
    "floor":  5,
    "nearest_kindergarten": 190,
    "nearest_educational_institution": 160.0,
    "nearest_shop": 480.0,
    "public_transport_stop": 310.0,
    "building_type": "Brick",
    "no_of_floors": 5},
    {"division": "Naujininkai",
    "area": 41,
    "no_of_rooms": 2,
    "build_year": 1960,
    "floor": 3,
    "nearest_kindergarten": 120,
    "nearest_educational_institution": 160.0,
    "nearest_shop": 270.0,
    "public_transport_stop": 120.0,
    "building_type": "Brick",
    "no_of_floors":4
     }]

post_data = json.dumps(data)
resp = requests.post(url, data=post_data)
print(resp.status_code, resp.content)
```
## License
The MIT License - Copyright (c) 2021 - Blessing Ehizojie-Philips
