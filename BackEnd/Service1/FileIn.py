from flask import Flask, request
import pandas as pd
import py_eureka_client.eureka_client as eureka_client
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

your_rest_server_port = 8080
eureka_client.init(eureka_server="http://eureka:8761/eureka",
                                app_name="cleanerapi",
                                instance_port=your_rest_server_port)

#clean up any null values in the csv (replace or delete them) (deleting them for now, will come back to replace with means/medians)
#should return a valid and clean json version of the dataframe
def remove_nulls(file) -> dict:
    df: pd.DataFrame = pd.read_csv(file)
    df = df.fillna(df.mean(numeric_only=True)) #numbers are a lot easier to fill in with the mean
    df = df.dropna() #clear out any fields that still have nulls in them
    # print(df.head(20))
    return df.to_json()


#keeps the file name and data together
@app.route('/cleanCSV', methods=['GET'])
@cross_origin()
def clean_data():
    file_name: str = request.files["dirty_csv"].filename
    dirty_csv = request.files["dirty_csv"]
    clean_dict = {'clean_csv' : remove_nulls(dirty_csv)}
    print(file_name)
    return clean_dict


app.run(host='0.0.0.0', port=8080)