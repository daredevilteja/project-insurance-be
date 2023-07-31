import os
import pandas as pd
from flask import Flask, request, jsonify
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient("mongodb+srv://<MONGO_USER_NAME>:<MONGO_PASSWORD>@cluster0.8bxb9sn.mongodb.net/?retryWrites=true&w=majority"
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
        import_csv_data()
    return {"data": "DB loaded successfully",
            "message": "server started successfully"}


@app.route('/get-premium', methods=["POST"])
def get_premium():
    data = request.json
    adult_ages = []
    child_ages = []
    adult_count = data.get("adult_count")
    if adult_count != 0:
        adult_ages = data.get("adult_ages")
        adult_ages.sort(reverse=True)
    child_count = data.get("child_count")
    if child_count != 0:
        child_ages = data.get("child_ages")
    sum_insured = data.get("sum_insured")
    city_tier = data.get("city_tier")
    tenure_of_insurance = data.get("tenure_of_insurance")

    rate = 0

    for i in range(len(adult_ages)):
        query = {
            '$and': [
                {'SumInsured': sum_insured},
                {'TierID': city_tier},
                {'Tenure': tenure_of_insurance},
                {"Age": adult_ages[i]}
            ]
        }

        curr_rate = collection.find_one(query).get("Rate")
        if i == 0:
            rate += curr_rate
            continue
        rate += curr_rate / 2

    if len(child_ages) != 0:
        for i in range(len(child_ages)):
            query = {
                '$and': [
                    {'SumInsured': sum_insured},
                    {'TierID': city_tier},
                    {'Tenure': tenure_of_insurance},
                    {"Age": child_ages[i]}
                ]
            }

            curr_rate = collection.find_one(query).get("Rate")
            rate += curr_rate / 2

    return jsonify(rate)


if __name__ == "__main__":
    app.run()
