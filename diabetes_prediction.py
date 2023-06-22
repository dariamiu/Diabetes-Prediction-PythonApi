from flask import jsonify
from flask_restful import Resource, reqparse
from keras.models import load_model


class Predictor(Resource):
    def __init__(self):
        self.model = load_model("model.h5")
        self.req_parser = reqparse.RequestParser()
        self.req_parser.add_argument('age', type=int, location='json')
        self.req_parser.add_argument('gender', type=str, location='json')
        self.req_parser.add_argument('hypertension', type=int, location='json')
        self.req_parser.add_argument('heart_disease', type=int, location='json')
        self.req_parser.add_argument('smoking_history', type=str, location='json')
        self.req_parser.add_argument('bmi', type=float, location='json')
        self.req_parser.add_argument('HbA1c_level', type=float, location='json')
        self.req_parser.add_argument('blood_glucose_level', type=int, location='json')

    def post(self):
        args = self.req_parser.parse_args()
        age = args['age']
        return jsonify(x=age)
