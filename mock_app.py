import inspect
import mock_data
import utilities
import data_models
import data_connector.mongodb as mongodb
import argparse
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
uri = config.get("database", "uri")

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test", help="run in test mode", action="store_true")
args = parser.parse_args()

#Using MongoDB Community as a mock database
print("Connecting to database... at", uri)
client = mongodb.MongoClient(uri)
client._push_mock_data(mock_data.startingEntry)

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
    meal_calories = client.get_daily_calories(mock_data.startingEntry["date"])
    for meal in meal_calories:
        print(f"{meal['name']}: {meal['calories']} calories")

def mealString(meal: data_models.Meal) -> [str, int]:
    entriesInMeal = []
    totalMealCalories = 0
    for mealEntry in meal.entries:
        if mealEntry.type != data_models.MealEntryType.FOOD:
            mealOutputString, mealCalories = mealString(mealEntry.object)
            entriesInMeal.append(utilities.tabbedString(mealOutputString, 1))
            totalMealCalories += mealCalories
        food = mealEntry.object
        entriesInMeal.append(f"\t{food.name}: {food.quantity} {food.unit} - {food.calories} calories")
        totalMealCalories += food.calories
    outputString = f"{meal.name} - {totalMealCalories} calories\n"
    outputString += ("\n".join(entriesInMeal))
    return outputString, totalMealCalories


def getFullJournal(user_input):
    """
    Prints the full journal for the day
    """
    data = client.get_daily_journal(mock_data.startingEntry["date"])
    dailyCalories = 0
    print(f"Journal for {data.date}")
    for meal in data.meals:
        output, calories = mealString(meal)
        print(output)
        dailyCalories += calories
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
    
    entryForDate = client.get_daily_journal(mock_data.startingEntry["date"])

    mealObject = entryForDate.getMealByName(meal)
    if mealObject is None:
        mealObject = data_models.Meal(meal)
    foodObject = data_models.Food(food, quantity, unit, calories)
    mealObject.addMealEntry(data_models.MealEntry(data_models.MealEntryType.FOOD, foodObject))

    client.push_daily_jounral(mock_data.startingEntry["date"], entryForDate)

@utilities.Debug_User_Input("2021-01-01")
def createDailyEntry(user_input):
    """
        Creates a new daily entry: <date>
    """
    if user_input == "":
        print("Error: No date provided")
        return
    date = user_input
    data = client.create_daily_journal(date)

def error(user_input):
    print("Error: Command not recognized")

commands = {
    "help": help,
    "summary": getDaySummary,
    "add_to_entry": addFoodEntry,
    # "create_entry": createDailyEntry,
    "get_entry": getFullJournal,
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