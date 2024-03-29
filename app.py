
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pickle
import numpy as np
from  sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

#from model import NLPModel

app = Flask(__name__)
api = Api(app)

#model = NLPModel()

clf_path = 'lib/models/Classifier.pkl'
with open(clf_path, 'rb') as f:
    clf = pickle.load(f)

vec_path = 'lib/models/Vectorizer.pkl'
with open(vec_path, 'rb') as f:
    vectorizer = pickle.load(f)

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('query')


class PredictSentiment(Resource):
    def get(self):
        # use parser and find the user's query
        args = parser.parse_args()
        user_query = args['query']

        # vectorize the user's query and make a prediction
        uq_vectorized = vectorizer.transform(np.array([user_query]))
        prediction = clf.predict(uq_vectorized)
        pred_proba = clf.predict_proba(uq_vectorized)

        # Output either 'Negative' or 'Positive' along with the score
        pred_text = prediction
		#if prediction == 0:
        #    pred_text = 'Negative'
        #else:
        #    pred_text = 'Positive'
            
        # round the predict proba value and set to new variable
        confidence = round(pred_proba[0], 3)

        # create JSON object
        output = {'prediction': pred_text, 'confidence': confidence}
        
        return output


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PredictSentiment, '/')


if __name__ == '__main__':
    app.run(debug=True)