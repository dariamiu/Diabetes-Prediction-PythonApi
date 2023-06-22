import numpy as np
from flask import jsonify
from flask_restful import Resource, reqparse
from keras.models import load_model
from sklearn.preprocessing import StandardScaler

class Predictor(Resource):
    def __init__(self):
        self.model = load_model("model.h5")
        self.req_parser = reqparse.RequestParser()
        self.x_scaled = np.array([])
        self.req_parser.add_argument('age', type=int, location='json')
        self.req_parser.add_argument('gender', type=str, location='json')
        self.req_parser.add_argument('hypertension', type=int, location='json')
        self.req_parser.add_argument('heart_disease', type=int, location='json')
        self.req_parser.add_argument('smoking_history', type=str, location='json')
        self.req_parser.add_argument('bmi', type=float, location='json')
        self.req_parser.add_argument('HbA1c_level', type=float, location='json')
        self.req_parser.add_argument('blood_glucose_level', type=int, location='json')

    def process_data(self):
        args = self.req_parser.parse_args()
        x = [args['age'], args['hypertension'], args['heart_disease'], args['bmi'], args['HbA1c_level'],
             args['blood_glucose_level']]

        if args['gender'] == 'Male':
            x.append(0)
            x.append(1)
        else:
            x.append(1)
            x.append(0)

        smoking_values = np.array([])
        if args['smoking_history'] == 'current':
            smoking_values = [1, 0, 0, 0, 0]
        elif args['smoking_history'] == 'ever':
            smoking_values = [0, 1, 0, 0, 0]
        elif args['smoking_history'] == 'former':
            smoking_values = [0, 0, 1, 0, 0]
        elif args['smoking_history'] == 'never':
            smoking_values = [0, 0, 0, 1, 0]
        elif args['smoking_history'] == 'not current':
            smoking_values = [0, 0, 0, 0, 1]
        print("smoking is ")
        print(smoking_values)
        x += smoking_values
        print("x is ")
        print(x)
        x_array = np.array(x)
        scaler = StandardScaler()
        self.x_scaled = scaler.fit_transform(x_array[:, np.newaxis])

    def post(self):
        self.process_data()
        print(self.x_scaled)
        print(self.x_scaled.reshape((1, -1)))
        y = self.model.predict(self.x_scaled.reshape((1, -1)))
        print(y)
        prediction = [
            {'prediction': y}
        ]
        return jsonify(prediction)
