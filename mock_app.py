import inspect
import mock_data
from pymongo.mongo_client import MongoClient


#Using MongoDB Community as a mock database
uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.1"
client = MongoClient(uri)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.get_database("mock_tracker")
collection = db.get_collection("dailyEntries")

if collection.count_documents({}) == 0:
    collection.insert_one(mock_data.startingEntry)

def app():
    print("App initialized")
    print("Type 'help' for a list of commands")
    while True:
        user_input = input("Enter a command: ")
        user_command = user_input.split(" ")[0]
        if user_command == "quit":
            print("Quitting...")
            break
        if user_command == "help":
            print("Available commands:")
            for command in commands:
                print(f"{command}: {inspect.getdoc(commands[command])}")
            continue
        command = commands.get(user_command, error)
        command(user_input)



def getDaySummary(user_input):
    """
    Summarized the day's meals by calories
    """
    data = collection.find_one({"date": mock_data.startingEntry["date"]})
    meal_calories = (list(collection.aggregate([
        {"$match": {"date": mock_data.startingEntry["date"]}},
        {"$unwind": "$meals"},
        #Brings meals to the top level (we want meals: total calories)
        {"$replaceRoot": {"newRoot": "$meals"}},
        #For each meal, keeps only the name and then computes the sum of calories
        {"$project": {"_id": 0, "name": 1, "calories": {"$sum": "$foods.calories"}}}
    ])))
    for meal in meal_calories:
        print(f"{meal['name']}: {meal['calories']} calories")


def getFullJournal(user_input):
    """
    Prints the full journal for the day
    """
    data = collection.find_one({"date": mock_data.startingEntry["date"]})
    print(f"Journal for {data['date']}")
    for meal in data["meals"]:
        print(f"{meal['name']}:")
        for food in meal["foods"]:
            print(f"\t{food['name']}: {food['quantity']} {food['unit']}")

def command3(user_input):
    print("Command 3 executed")

def error(user_input):
    print("Error: Command not recognized")

commands = {
    "dailySummary": getDaySummary,
    "fullJournal": getFullJournal,
    "command3": command3,
}
if __name__ == "__main__":
    for command in commands:
        print(f"Running {command}")
        commands[command]('')
        print()
    #app()
