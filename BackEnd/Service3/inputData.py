from flask import Flask, request, Response
import pymongo
from bson.objectid import ObjectId
import joblib
import os
import py_eureka_client.eureka_client as eureka_client
from flask_cors import CORS, cross_origin


DB_USER = os.environ.get('DB_USERNAME')
DB_PASS = os.environ.get('DB_PASSWORD')

DB_USER = DB_USER if DB_USER is not None else 'ShokoCapstone' #take these out before prod
DB_PASS = DB_PASS if DB_PASS is not None else 'U5bjze5RVZsHiLn5'

client = pymongo.MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASS}@capstone.qawfukq.mongodb.net/?retryWrites=true&w=majority")
db = client['Capstone']
col = db['ModelFiles']

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

your_rest_server_port = 8082
eureka_client.init(eureka_server="http://eureka:8761/eureka",
                                app_name="usemodelapi",
                                instance_port=your_rest_server_port)

def debug_out(item: str):
    print('---------------------------------------------------',item,'---------------------------------------------------', sep='\n')

#use the id to find the model, load it with pandas/sklearn, shoot back a result (stretch goal is letting user input multiple entries at once)
def model_input(id: str, entered_data: list) -> list:
    # debug_out(str(str(ObjectId(id)) + ' here1'))
    # debug_out(id)
    model = col.find_one({'_id':ObjectId(id)})
    if(model is None): return Response("{'NullPointerError':'Object Can Not Be Found with id: " + str(ObjectId(id)) +  "'}", status=404, mimetype='application/json')
    print(model)
    trained = model['training']
    with open('trained.joblib', 'wb') as f:
        f.write(trained)
    model = joblib.load('trained.joblib') #load in previous training data
    predictions = list(model.predict([entered_data]))[0]
    os.remove('trained.joblib')
    return predictions
    # return id


@app.route('/useModel', methods=['POST'])
@cross_origin()
def use_model():
    data: dict = request.args.to_dict()
    id: str = data.get('id')
    entered_data: list = str(data.get('entered_data')).split(',')
    return model_input(id=id, entered_data=entered_data)
    

app.run(host='0.0.0.0', port=8082)