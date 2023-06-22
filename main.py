from flask import Flask
from flask_restful import Api
from diabetes_prediction import Predictor

app = Flask(__name__)
api = Api(app)
api.add_resource(Predictor, '/diagnose')

if __name__ == '__main__':
    app.run(debug=True)

