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
        command_arguments = user_input[len(user_command):].strip()
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

@utilities.Debug_User_Input([mock_data.startingEntry["date"],])
def getDaySummary(user_input):
    """
    Summarized the day's meals by calories
    """
    date = user_input
    meal_calories = client.get_daily_calories(date)
    for meal in meal_calories:
        print(f"{meal}: {meal_calories[meal]} calories")

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

@utilities.Debug_User_Input([mock_data.startingEntry["date"],"2021-01-01"])
def getFullJournal(user_input):
    date = user_input
    """
    Prints the full journal for the day
    """
    data = client.get_daily_journal(date)
    dailyCalories = 0
    print(f"Journal for {data.date}")
    for meal in data.meals:
        output, calories = mealString(meal)
        print(output)
        dailyCalories += calories
    print(f"Total Calories: {dailyCalories}")

@utilities.Debug_User_Input(f"Breakfast Blueberries 1 cup 55 {mock_data.startingEntry['date']}")
def addFoodEntry(user_input):
    """
    Adds a food entry to the journal:
        Input format <meal> <food> <quantity> <unit> <calories> <date>
    """
    cmds = user_input.split()
    if len(cmds) != 6:
        print("Error: Invalid command format")
        return
    meal, food, quantity, unit, calories, date = cmds
    quantity = int(quantity)
    calories = int(calories)
    
    entryForDate = client.get_daily_journal(date)

    mealObject = entryForDate.getMealByName(meal)
    if mealObject is None:
        mealObject = data_models.Meal(meal)
    foodObject = data_models.Food(name = food, quantity = quantity, unit = unit, calories = calories)
    mealObject.addMealEntry(data_models.MealEntry(data_models.MealEntryType.FOOD, foodObject))

    client.push_daily_jounral(date, entryForDate)

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
    "create_entry": createDailyEntry,
    "get_entry": getFullJournal,
}
if __name__ == "__main__":
    if args.test:
        print("Running in test mode")
        for command in commands:
            print("Executing command:", command)
            mock_inputs = [""]
            try:
                mock_inputs = commands[command].debug_user_input
            except AttributeError:
                pass
            if isinstance(mock_inputs, str):
                mock_inputs = [mock_inputs]
            for input in mock_inputs:
                print("\t Mock input:", input)
                commands[command](input)
    else:
        print("Running in production mode")
        app()