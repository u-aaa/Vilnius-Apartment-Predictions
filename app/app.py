import pickle
from typing import Union
import json
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

with open('models/linear_regression.pkl', 'rb') as f:
    model = pickle.load(f)

features = {'division', 'no_of_rooms', 'area', 'floor', 'no_of_floors',
                                  'build_year', 'building_type', 'nearest_kindergarten',
                                  'nearest_educational_institution', 'nearest_shop',
                                  'public_transport_stop'}


def process_input(posted_data: json) -> Union[pd.DataFrame, None]:
    '''
    processes the input data and makes it suitable for prediction
    :param posted_data: data sent in the post request
    :return: df
    '''
    data = json.loads(posted_data)
    for i in data:
        assert features.issubset(set(i.keys()))
    return pd.DataFrame(data, columns=list(features))


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
        prediction = model.predict(predict_params)
        predict_params['price_per_month'] = np.round(prediction, decimals=0)
        predict_params.to_sql('predictions', con=db.engine, if_exists='append', index=False)
        result = predict_params.to_dict('index')
        response = []
        for x in result:
            response.append(result[x])
        return json.dumps(response)
    except (AssertionError, json.decoder.JSONDecodeError):
        return json.dumps({'Please post data with these headers': ['division', 'no_of_rooms', 'area', 'floor',
                                                                       'no_of_floors',
                                                                       'build_year', 'building_type',
                                                                       'nearest_kindergarten',
                                                                       'nearest_educational_institution',
                                                                       'nearest_shop',
                                                                       'public_transport_stop']}), 400
    except Exception as ex:
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
