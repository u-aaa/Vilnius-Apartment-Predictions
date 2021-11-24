import pickle
from typing import Union
import json
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

with open('models/linear_regression.pkl', 'rb') as f:
    model = pickle.load(f)

features = ['division', 'no_of_rooms', 'area', 'floor', 'no_of_floors', 'build_year', 'building_type', 'nearest_kindergarten',
            'nearest_educational_institution', 'nearest_shop', 'public_transport_stop']

def process_input(posted_data: json) -> Union[pd.DataFrame, None]:
    '''
    processes the input data and makes it suitable for prediction
    :param posted_data: data sent in the post request
    :return: df
    '''
    data = json.loads(posted_data)
    for i in data:
        assert set(features).issubset(set(i.keys()))
    return pd.DataFrame(data, columns=features)

def predict_price(df: pd.DataFrame):
    """
    predicts the house price and pushes to database
    :param df:
    :return:
    """
    prediction = model.predict(df)
    df['price_per_month'] = np.round(prediction, decimals=0)
    try:
        df.to_sql('predictions', con=db.engine, if_exists='append', index=False)
        return df.to_dict('records')
    except Exception as err:
        logging.exception(f'An error occured', err)
        return df.to_dict('records')


@app.route('/')
def index() -> str:
    '''
    returns landing page for the app
    :return:
    '''
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict() -> Union[str, int]:
    '''
    returns the predicted house price depending on the data passed in the post request
    :return: json
    '''
    posted_data = request.data
    try:
        predict_params = process_input(posted_data)
        response = predict_price(predict_params)
        return json.dumps(response)
    except (AssertionError, json.decoder.JSONDecodeError) as err:
        logging.exception(err)
        return json.dumps({'Please post data with these headers': features}), 400
    except Exception as ex:
        logging.exception(ex)
        return json.dumps({'Unable to predict': ex}), 500


@app.route('/predictions', methods=['GET'])
def predictions() -> (str):
    '''
    returns the last 10 predictions made on the app
    :return: json
    '''
    query = 'SELECT * FROM predictions ORDER BY predictions.id DESC LIMIT 10'
    result_df = pd.read_sql(query, con=db.engine)
    result = result_df.to_dict('index')
    response = []
    if len(result) > 0:
        for x in result:
            response.append(result[x])
        return json.dumps(response)
    return json.dumps({'Empty database table'})



if __name__ == '__main__':
    app.run()
