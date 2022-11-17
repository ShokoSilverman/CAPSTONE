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
from subprocess import call
import py_eureka_client.eureka_client as eureka_client
from datetime import date
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

your_rest_server_port = 8081
eureka_client.init(eureka_server="http://eureka:8761/eureka",
                                app_name="mainlearningapi",
                                instance_port=your_rest_server_port)

DB_USER = os.environ.get('DB_USERNAME')
DB_PASS = os.environ.get('DB_PASSWORD')

DB_USER = DB_USER if DB_USER is not None else 'ShokoCapstone' #take these out before prod
DB_PASS = DB_PASS if DB_PASS is not None else 'U5bjze5RVZsHiLn5'

client = pymongo.MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASS}@capstone.qawfukq.mongodb.net/?retryWrites=true&w=majority")
db = client['Capstone']
col = db['ModelFiles']

#main composer method, takes in everything and then distributes to other methods
def run_time(data_json: dict, output_field: str, model_type: int, training_percent: int, min_acc: int, name: str, is_private: bool, user: str, user_email: str, description: str): #returns the inserted ID
    df = data_intake(data_json)
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
    call(['dot', '-Tpng', 'graph.dot', '-o', 'tree.png'])
    with open('tree.png', "rb") as f:
        graph_info = Binary(f.read())
    inserted = col.insert_one({'name':name, 'training': model_info, 'graph':graph_info, 'dateCreated': str(date.today()), 'is_private': is_private, 'user': user , 'user_mail':user_email, 'description':description, 'input_columns':input_cols})
    os.remove('graph.dot')
    os.remove('tree.png')
    os.remove('model.joblib')
    return inserted.inserted_id



#TODO swap this in flask to intake the csv file, send it to be cleaned and then get it back
def data_intake(data_json: dict) -> pd.DataFrame:
    clean_data: dict = data_json #swap this to call service 1 and clean
    df = pd.read_json(clean_data)
    print(df.head(10))
    return df

#model type 0 = classifier, model type 1 = regressions
def create_new_model(df: pd.DataFrame, output_field: str, model_type: str, t_percent: int, min_acc: int):
    X = df.drop(columns=[output_field]) #input set #can not change the variable name on these, library wont work without it
    # input_cols: list = X.columns
    # print('---------------------------', input_cols, '--------------------------------', sep='\n')
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
@cross_origin()
def create_model():
    dirty_csv = request.files["dirty_csv"]
    # clean_data = (requests.get('http://localhost:8080/cleanCSV', files={'dirty_csv':dirty_csv}).json())['clean_csv']
    clean_data = (requests.get('http://gateway:8888/cleanerapi/cleanCSV', files={'dirty_csv':dirty_csv}).json())['clean_csv']
    # data: dict = request.json()
    output_field: str = request.form.get('output_field')
    model_type: int = int(request.form.get('model_type'))
    training_percent: int = int(request.form.get('training_percent'))
    min_acc: int = int(request.form.get('min_acc'))
    name: str = request.form.get('name')
    #add ins from front end
    is_private: bool = bool(int(request.form.get('is_private')))
    user: str = request.form.get('user')
    user_email: str = request.form.get('user_email')
    description: str = request.form.get('description')
    try:
        id = run_time(data_json=clean_data, output_field=output_field, model_type=model_type, training_percent=training_percent, min_acc=min_acc, name=name, is_private=is_private, user=user, user_email=user_email, description=description)
    except ValueError:
        return Response("{'Value Error' : 'all regression values must be numeric'}", status=400, mimetype='application/json')
    return str(id)
    

app.run(host='0.0.0.0', port=8081)
