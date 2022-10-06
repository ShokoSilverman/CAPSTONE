import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from sklearn import tree
import pymongo
from bson.binary import Binary
import os
from flask import Flask, request, Response
import requests

#delete this soon
test_data: dict = {
    "music.csv": "{\"age\":{\"0\":20,\"1\":23,\"2\":25,\"3\":26,\"4\":29,\"5\":30,\"6\":31,\"7\":33,\"8\":37,\"9\":20,\"10\":21,\"11\":25,\"12\":26,\"13\":27,\"14\":30,\"15\":31,\"16\":34,\"17\":35},\"gender\":{\"0\":1,\"1\":1,\"2\":1,\"3\":1,\"4\":1,\"5\":1,\"6\":1,\"7\":1,\"8\":1,\"9\":0,\"10\":0,\"11\":0,\"12\":0,\"13\":0,\"14\":0,\"15\":0,\"16\":0,\"17\":0},\"genre\":{\"0\":\"HipHop\",\"1\":\"HipHop\",\"2\":\"HipHop\",\"3\":\"Jazz\",\"4\":\"Jazz\",\"5\":\"Jazz\",\"6\":\"Classical\",\"7\":\"Classical\",\"8\":\"Classical\",\"9\":\"Dance\",\"10\":\"Dance\",\"11\":\"Dance\",\"12\":\"Acoustic\",\"13\":\"Acoustic\",\"14\":\"Acoustic\",\"15\":\"Classical\",\"16\":\"Classical\",\"17\":\"Classical\"}}"
}

app = Flask(__name__)

#TODO CHANGE THIS TO USE ENVIRON VARIABLES
client = pymongo.MongoClient("mongodb+srv://ShokoCapstone:U5bjze5RVZsHiLn5@capstone.qawfukq.mongodb.net/?retryWrites=true&w=majority")
db = client['Capstone']
col = db['ModelFiles']

#main composer method, takes in everything and then distributes to other methods
def run_time(data_json: dict, output_field: str, model_type: int, training_percent: int, min_acc: int): #returns the inserted ID
    df, data_set = data_intake(data_json)
    df:pd.DataFrame = df
    #check regression for nums
    if model_type == 1:
        for column in df.columns:
            if not df[column].dtype in ['float', 'int64']:
                raise ValueError('All values must be numeric!')
    model = create_new_model(df=df, output_field=output_field, model_type=model_type, t_percent=training_percent, min_acc=min_acc)
    #save the joblib and dot file file to the db
    #https://stackoverflow.com/questions/40015103/upload-file-size-16mb-to-mongodb
    joblib.dump(model, 'model.joblib')
    with open('model.joblib', "rb") as f:
        model_info = Binary(f.read())
    with open('graph.dot', "rb") as f:
        graph_info = Binary(f.read())
    inserted = col.insert_one({'data_set': data_set, 'training': model_info, 'graph':graph_info})
    os.remove('graph.dot')
    os.remove('model.joblib')
    return inserted.inserted_id



#TODO swap this in flask to intake the csv file, send it to be cleaned and then get it back
def data_intake(data_json: dict) -> pd.DataFrame:
    clean_data: dict = data_json #swap this to call service 1 and clean
    # file_name: str = list(data_json.keys())[0]
    # df = pd.read_json(clean_data[file_name])
    df = pd.read_json(clean_data)
    print(df.head(10))
    return df, clean_data

#model type 0 = classifier, model type 1 = regressions
def create_new_model(df: pd.DataFrame, output_field: str, model_type: str, t_percent: int, min_acc: int):
    X = df.drop(columns=[output_field]) #input set #can not change the variable name on these, library wont work without it
    y = df[output_field] #output set
    if model_type == 0: #classifier
        model = DecisionTreeClassifier()
    elif model_type == 1: #regression
        model = DecisionTreeRegressor()
    #no else statement, stretch goal is adding more types
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(t_percent/100))
    min_acc_percent: float = (min_acc//100)
    #optimize this loop, its bad
    for i in range(0,5): #loop until desired accuracy is achieved, or until tested 10 times
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        score = accuracy_score(y_test, predictions)
        if score >= min_acc_percent:
            tree.export_graphviz(model, out_file='graph.dot', feature_names=list(X.columns), class_names=sorted(y.unique()),
                    label='all', rounded=True, filled=True)
            return model
    tree.export_graphviz(model, out_file='graph.dot', feature_names=list(X.columns), class_names=sorted(y.unique()),
                    label='all', rounded=True, filled=True)
    return model



@app.route('/createModel', methods=['POST'])
def create_model():
    dirty_csv = request.files["dirty_csv"]
    clean_data = (requests.get('http://localhost:8080/cleanCSV', files={'dirty_csv':dirty_csv}).json())['clean_csv']
    output_field: str = request.form.get('output_field')
    model_type: int = int(request.form.get('model_type'))
    #TODO add a check here, if model type 1 (regression) all data needs to be numbers!!!
    training_percent: int = int(request.form.get('training_percent'))
    min_acc: int = int(request.form.get('min_acc'))
    try:
        id = run_time(data_json=clean_data, output_field=output_field, model_type=model_type, training_percent=training_percent, min_acc=min_acc)
    except ValueError:
        return Response("{'Value Error' : 'all regression values must be numeric'}", status=400, mimetype='application/json')
    return str(id)
    

app.run(host='0.0.0.0', port=8081)
