import inspect
import mock_data
import utilities
from pymongo.mongo_client import MongoClient
import argparse
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

uri = config.get("database", "uri")

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test", help="run in test mode", action="store_true")
args = parser.parse_args()

#Using MongoDB Community as a mock database
uri = config.get("database", "uri")
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
        if user_command in {"quit", "exit", "exit()"}:
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
    dailyCalories = 0
    print(f"Journal for {data['date']}")
    for meal in data["meals"]:
        entriesInMeal = []
        totalMealCalories = 0
        for food in meal["foods"]:
            entriesInMeal.append(f"\t{food['name']}: {food['quantity']} {food['unit']} - {food['calories']} calories")
            totalMealCalories += food["calories"]
        print(f"{meal['name']} - {totalMealCalories} calories")
        print("\n".join(entriesInMeal))
        dailyCalories += totalMealCalories
    print(f"Total Calories: {dailyCalories}")
@utilities.Debug_User_Input("Breakfast Blueberries 1 cup 55")
def addFoodEntry(user_input):
    """
    Adds a food entry to the journal:
        Input format <meal> <food> <quantity> <unit> <calories>
    """
    cmds = user_input.split()
    if len(cmds) != 5:
        print("Error: Invalid command format")
        print(utilities.tabbedString("Expected Parameters: <meal> <food> <quantity> <unit> <calories>", 1))
        return
    meal, food, quantity, unit, calories = cmds
    quantity = int(quantity)
    calories = int(calories)
    
    data = collection.find_one({"date": mock_data.startingEntry["date"]})

    for mealObject in data["meals"]:
        if mealObject["name"] == meal:
            #Insert food into meal
            mealObject["foods"].append({
                "name": food,
                "quantity": quantity,
                "unit": unit,
                "calories": calories
            })
            break
    else:
        #Create meal and insert food into meal
        data["meals"].append({
            "name": meal,
            "foods": []
        })
        data["meals"][-1]["foods"].append({
            "name": food,
            "quantity": quantity,
            "unit": unit,
            "calories": calories
        })

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