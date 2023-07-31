import os
import pprint
import pandas as pd
import json
from flask import Flask, request, jsonify
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient("mongodb+srv://daredevilteja:4kjktxQJ5qwD15Ag@cluster0.8bxb9sn.mongodb.net/?retryWrites=true&w=majority"
                     )
db = client["test-database"]
collection = db["test-collection"]


def import_csv_data():
    data_file_path = os.path.join('data', 'data.csv')
    data = pd.read_csv(data_file_path)
    data_list = data.to_dict(orient='records')
    collection.insert_many(data_list)


@app.route('/', methods=["GET"])
def index():
    if not collection.find_one():
        pprint.pprint("in")
        import_csv_data()
    return {"data": "DB loaded successfully",
            "message": "server started successfully"}


if __name__ == "__main__":
    app.run(debug=True)
