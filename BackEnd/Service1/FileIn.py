from flask import Flask, redirect, url_for, request
import pandas as pd

app = Flask(__name__)

#clean up any null values in the csv (replace or delete them) (deleting them for now, will come back to replace with means/medians)
#should return a valid and clean json version of the dataframe
def remove_nulls(file) -> dict:
    df: pd.DataFrame = pd.read_csv(file)
    df = df.fillna(df.mean(numeric_only=True)) #numbers are a lot easier to fill in with the mean
    df = df.dropna() #clear out any fields that still have nulls in them
    # print(df.head(20))
    return df.to_json()


#TODO flask endpoint here, make sure to use pd.to_csv to return the csv file
@app.route('/cleanCSV', methods=['POST'])
def clean_data():
    file_name: str = request.files["dirty_csv"].filename
    dirty_csv = request.files["dirty_csv"]
    clean_dict = {file_name : remove_nulls(dirty_csv)}
    print(type(clean_dict[file_name]))
    return clean_dict


app.run(host='0.0.0.0', port=8080)