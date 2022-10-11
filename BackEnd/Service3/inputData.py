from flask import Flask, request
import pymongo
from bson.objectid import ObjectId
import joblib
import os


DB_USER = os.environ.get('DB_USERNAME')
DB_PASS = os.environ.get('DB_PASSWORD')

DB_USER = DB_USER if DB_USER is not None else 'ShokoCapstone' #take these out before prod
DB_PASS = DB_PASS if DB_PASS is not None else 'U5bjze5RVZsHiLn5'

client = pymongo.MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASS}@capstone.qawfukq.mongodb.net/?retryWrites=true&w=majority")
db = client['Capstone']
col = db['ModelFiles']

app = Flask(__name__)

#use the id to find the model, load it with pandas/sklearn, shoot back a result (stretch goal is letting user input multiple entries at once)
def model_input(id: str, entered_data: list) -> list:
    model = col.find_one({'_id':ObjectId(id)})
    trained = model['training']
    with open('trained.joblib', 'wb') as f:
        f.write(trained)
    model = joblib.load('trained.joblib') #load in previous training data
    predictions = list(model.predict([entered_data]))[0]
    os.remove('trained.joblib')
    return predictions


@app.route('/useModel', methods=['GET'])
def use_model():
    id: str = request.form.get('id')
    entered_data: list = str(request.form.get('entered_data')).split(',')
    return model_input(id=id, entered_data=entered_data)
    

app.run(host='0.0.0.0', port=8082)