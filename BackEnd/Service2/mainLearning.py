import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import sklearn.externals
import joblib
from sklearn import tree

test_data: dict = {
    "music.csv": "{\"age\":{\"0\":20,\"1\":23,\"2\":25,\"3\":26,\"4\":29,\"5\":30,\"6\":31,\"7\":33,\"8\":37,\"9\":20,\"10\":21,\"11\":25,\"12\":26,\"13\":27,\"14\":30,\"15\":31,\"16\":34,\"17\":35},\"gender\":{\"0\":1,\"1\":1,\"2\":1,\"3\":1,\"4\":1,\"5\":1,\"6\":1,\"7\":1,\"8\":1,\"9\":0,\"10\":0,\"11\":0,\"12\":0,\"13\":0,\"14\":0,\"15\":0,\"16\":0,\"17\":0},\"genre\":{\"0\":\"HipHop\",\"1\":\"HipHop\",\"2\":\"HipHop\",\"3\":\"Jazz\",\"4\":\"Jazz\",\"5\":\"Jazz\",\"6\":\"Classical\",\"7\":\"Classical\",\"8\":\"Classical\",\"9\":\"Dance\",\"10\":\"Dance\",\"11\":\"Dance\",\"12\":\"Acoustic\",\"13\":\"Acoustic\",\"14\":\"Acoustic\",\"15\":\"Classical\",\"16\":\"Classical\",\"17\":\"Classical\"}}"
}

#main composer method, takes in everything and then distributes to other methods
def run_time(data_json: dict, output_field: str, model_type: int):
    df = data_intake(data_json)
    model = create_model(df= df, output_field=output_field, model_type=model_type)

#TODO swap this in flask to intake the csv file, send it to be cleaned and then get it back
def data_intake(data_json: dict) -> pd.DataFrame:
    file_name: str = list(data_json.keys())[0]
    df = pd.read_json(data_json[file_name])
    print(df.head(10))
    return df

#model type 0 = classifier, model type 1 = regressions
def create_model(df: pd.DataFrame, output_field: str, model_type: str):
    #TODO input and output, tree type, model creating
    pass
    

run_time(data_json=test_data, output_field='genre', model_type=0)
