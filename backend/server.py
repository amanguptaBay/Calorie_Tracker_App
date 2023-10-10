import flask
import os
import pathlib
import logging

import data_models
import data_connector.mongodb as mongodb
import configparser
import mock_data

config = configparser.ConfigParser()
config.read("config.ini")
uri = config.get("database", "uri")

logging.basicConfig(level=logging.INFO)
app = flask.Flask(__name__)

# Serve static files from the "static" directory
base_dir = pathlib.Path.cwd()

#Using MongoDB Community as a mock database
print("Connecting to database... at", uri)
client = mongodb.MongoClient(uri)
client._clean_db()
client._push_mock_data(mock_data=data_models.DailyEntry.from_object(mock_data.startingEntry1))
client._push_mock_data(mock_data=data_models.DailyEntry.from_object(mock_data.startingEntry2))

@app.route("/api/echo/<message>")
def echo(message):
    return flask.jsonify({"message": message})

#Get dates with entries
@app.route("/api/summaries/dates")
def dates():
    logging.info("Fetching dates with entries")
    logging.info(client.dates_with_entries())
    return flask.jsonify(client.dates_with_entries())

@app.route("/api")
def api():
    return flask.jsonify({"message": "Hello from the API!"})


@app.route("/api/daily/food/<date>/<path:meal_path>", methods=["PUT","POST"])
def add_food_meal_path(date, meal_path):
    journal = client.get_daily_journal(date)
    if journal is None:
        return flask.jsonify({"error": "Journal not found"})
    obj = journal.processMealPath(meal_path)
    logging.info(f"Object being replaced: {obj}")
    if obj is None:
        return flask.jsonify({"error": "Meal not found"})
    newObject = data_models.MealEntry.from_object(flask.request.get_json(force=True))
    logging.info(f"Recieved new object: {newObject}")
    parent_path = "/".join(meal_path.split("/")[:-1])
    parent_object = journal.processMealPath(parent_path)
    if flask.request.method == "PUT":
        rel_index_parent = int(meal_path.split("/")[-1])
        parent_object.entries[rel_index_parent] = newObject
    if flask.request.method == "POST":
        obj.entries.append(newObject)
    flag = client.push_daily_jounral(date, journal)
    return flask.jsonify({"message": "Success" if flag else "Failure"})

@app.route("/api/daily/meal/<date>/<path:meal_path>", methods=["POST"])
def add_meal_meal_path(date, meal_path):
    journal = client.get_daily_journal(date)
    if journal is None:
        return flask.jsonify({"error": "Journal not found"})
    obj = journal.processMealPath(meal_path)
    newObject = data_models.Meal.from_object(flask.request.get_json(force=True))
    logging.info(f"New Object: {newObject}")
    logging.info(f"Meal Path is {obj}")
    if obj is None:
        journal.addMeal(data_models.Meal.from_object(newObject))
    else:
        obj.addEntry(data_models.MealEntry(type = data_models.MealEntryType.MEAL, foodOrMeal = newObject))
    flag = client.push_daily_jounral(date, journal)
    return flask.jsonify({"message": "Success" if flag else "Failure"})

@app.route("/api/daily/<date>")
def fetch_days_entry(date):
    journal = client.get_daily_journal(date)
    if journal is None:
        return flask.jsonify({})
    return flask.jsonify(journal.toJson())

@app.route("/api/summaries/calories/<date>")
def fetch_daily_calories(date):
    calories = client.get_daily_calories(date)
    return flask.jsonify(calories)

if __name__ == "__main__":
    app.run(debug=True, port=5100)