import flask
import os
import pathlib
import logging

import data_models.journal
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
client._push_mock_journal(mock_data=data_models.journal.JournalEntry.from_object(mock_data.startingEntry1))
client._push_mock_journal(mock_data=data_models.journal.JournalEntry.from_object(mock_data.startingEntry2))
client._push_mock_library(mock_data=data_models.library.Library.from_object(mock_data.mock_library_1))
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

@app.route("/api/daily/<date>", methods=["GET"])
def get_daily_journal(date):
    journal = client.get_daily_journal(date)
    if journal is None:
        return flask.jsonify({})
    return flask.jsonify(journal.toJson())

@app.route("/api/daily/<date>", methods=["POST"])
def create_daily_journal(date):
    journal = data_models.journal.JournalEntry.from_object(flask.request.get_json(force=True))
    flag = client.push_daily_journal(journal)
    return flask.jsonify({"message": "Success" if flag else "Failure"})

@app.route("/api/daily/<date>", methods=["PUT"])
def update_daily_journal(date):
    journal = data_models.journal.JournalEntry.from_object(flask.request.get_json(force=True))
    logging.info(f"Pushing journal: {journal}")
    flag = client.push_daily_journal(journal)
    return flask.jsonify({"message": "Success" if flag else "Failure"})


@app.route("/api/summaries/calories/<date>")
def fetch_daily_calories(date):
    calories = client.get_daily_calories(date)
    return flask.jsonify(calories)

if __name__ == "__main__":
    app.run(debug=True, port=5100)