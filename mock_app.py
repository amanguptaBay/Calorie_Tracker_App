import inspect
import mock_data
import utilities
from pymongo.mongo_client import MongoClient
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test", help="run in test mode", action="store_true")
args = parser.parse_args()

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
        command_arguments = user_input.split(" ")[1:]
        if user_command == "quit":
            print("Quitting...")
            break
        else:
            command = commands.get(user_command, error)
            command(command_arguments)

def help(user_input):
    print("Available commands:")
    for command in commands:
        print(f"{command}:")
        print(utilities.tabbedString(inspect.getdoc(commands[command]), 1))

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

@utilities.Debug_User_Input("Breakfast blueberries 1 cup")
def addFoodEntry(user_input):
    """
    Adds a food entry to the journal:
        Input format <meal> <food> <quantity> <unit>
    """
    cmds = user_input.split()
    if len(cmds) != 4:
        print("Error: Invalid command format")
        print(utilities.tabbedString("Expected Parameters: <meal> <food> <quantity> <unit>", 1))
        return
    meal, food, quantity, unit = cmds
    
    data = collection.find_one({"date": mock_data.startingEntry["date"]})
    
    if meal not in data.keys():
        data[meal] = []

    data[meal].append({"name": food, "quantity": quantity, "unit": unit})

    pushEvent = collection.update_one({"date": mock_data.startingEntry["date"]}, {"$set": data})
    if pushEvent.modified_count == 0:
        print("Error: Server error")
        print(pushEvent.raw_result)
        return

def command3(user_input):
    print("Command 3 executed")

def error(user_input):
    print("Error: Command not recognized")

commands = {
    "dailySummary": getDaySummary,
    "fullJournal": getFullJournal,
    "addFoodEntry": addFoodEntry,
    "help": help,
}
if __name__ == "__main__":
    if args.test:
        print("Running in test mode")
        for command in commands:
            mock_input = ""
            try:
                mock_input = commands[command].debug_user_input
            except AttributeError:
                pass
            print("Executing command:", command)
            print("Mock input:", mock_input)
            commands[command](mock_input)
    else:
        print("Running in production mode")
        app()