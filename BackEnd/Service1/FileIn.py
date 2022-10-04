from flask import Flask, redirect, url_for, request
import pandas as pd
# import numpy


# app = Flask(__name__)

#clean up any null values in the csv (replace or delete them) (deleting them for now, will come back to replace with means/medians)
def remove_nulls(file) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(file)
    df = df.fillna(df.mean()) #numbers are a lot easier to fill in with the mean
    df = df.dropna() #clear out any fields that still have nulls in them
    print(df.head(20))


remove_nulls(r'testData\Data_With_Nulls_Age.csv')

# app.run(host='0.0.0.0', port=8080)