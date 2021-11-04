import json
import pandas as pd
from app.app import process_input

single_input = [{
    "division": "Baltupiai",
    "area": 35,
    "no_of_rooms": 1,
    "build_year": 2021,
    "floor": 2,
    "nearest_kindergarten": 80,
    "nearest_educational_institution": 170.0,
    "nearest_shop": 490.0,
    "public_transport_stop": 240.0,
    "building_type": "Brick",
    "no_of_floors": 5}]

double_input = [{
    "division": "Karoliniškės",
    "area": 68.3,
    "no_of_rooms": 3,
    "build_year": 1977,
    "floor": 5,
    "nearest_kindergarten": 320,
    "nearest_educational_institution": 260.0,
    "nearest_shop": 180.0,
    "public_transport_stop": 100.0,
    "building_type": "Block house",
    "no_of_floors": 9},
    {"division": "Pilaitė",
     "area": 50,
     "no_of_rooms": 2,
     "build_year": 1994,
     "floor": 9,
     "nearest_kindergarten": 100,
     "nearest_educational_institution": 170.0,
     "nearest_shop": 310.0,
     "public_transport_stop": 180.0,
     "building_type": "Block house",
     "no_of_floors": 9
     }]

incomplete_data = [{
    "division": "Šnipiškės",
    "area": 71.78,
    "no_of_rooms": 2,
    "build_year": 1940,
    "floor": 1,
    "nearest_educational_institution": 310.0,
    "nearest_shop": 170.0,
    "public_transport_stop": 80.0,
    "building_type": "Brick",
    "no_of_floors": 3}]


def test_home(app, client):
    response = client.get('/')
    assert response.status_code == 200
    expected = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Vilnius Apartment Price Prediction App</title>
</head>
<body>
<h1>Vilnius Apartments Price Prediction App</h1>
<p>To post predictions, send a post request to <a href="https://www.w3.org/">app/predict</a></p>
<p>To view the last 10 predictions, click this link <a href="https://www.w3.org/">app/predictions</a></p>
</body>
</html>"""
    assert expected == response.get_data(as_text=True)


def test_process_input_positive():
    result = process_input(json.dumps(single_input))
    assert pd.DataFrame(single_input).equals(result)


def test_predict_single_input(app, client):
    response = client.post('/predict', data=json.dumps(single_input))
    assert response.status_code == 200
    expected = [{"division": "Baltupiai", "area": 35, "no_of_rooms": 1, "build_year": 2021, "floor": 2,
                 "nearest_kindergarten": 80, "nearest_educational_institution": 170.0, "nearest_shop": 490.0,
                 "public_transport_stop": 240.0, "building_type": "Brick", "no_of_floors": 5, "price_per_month": 311.0}]
    assert expected == json.loads(response.get_data())


def test_multiple_input_positive(app, client):
    response = client.post('/predict', data=json.dumps(double_input))
    assert response.status_code == 200
    expected = [{"division": "Karoliniškės", "area": 68.3, "no_of_rooms": 3, "build_year": 1977, "floor": 5,
                 "nearest_kindergarten": 320, "nearest_educational_institution": 260.0, "nearest_shop": 180.0,
                 "public_transport_stop": 100.0, "building_type": "Block house", "no_of_floors": 9,
                 "price_per_month": 651.0},
                {"division": "Pilaitė", "area": 50.0, "no_of_rooms": 2, "build_year": 1994, "floor": 9,
                 "nearest_kindergarten": 100, "nearest_educational_institution": 170.0, "nearest_shop": 310.0,
                 "public_transport_stop": 180.0, "building_type": "Block house", "no_of_floors": 9,
                 "price_per_month": 438.0}]
    assert expected == json.loads(response.get_data())


def test_incomplete_input_negative(app, client):
    response = client.post('/predict', data=json.dumps(incomplete_data))
    assert response.status_code == 400
    expected = {"Please post data with these headers": ["division", "no_of_rooms", "area", "floor", "no_of_floors",
                                                        "build_year", "building_type", "nearest_kindergarten",
                                                        "nearest_educational_institution", "nearest_shop",
                                                        "public_transport_stop"]}
    assert expected == json.loads(response.get_data())

