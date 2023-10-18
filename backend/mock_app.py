import inspect
import mock_data
import utilities
import data_models
import data_connector.mongodb as mongodb
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
uri = config.get("database", "uri")



#Using MongoDB Community as a mock database
print("Connecting to database... at", uri)
client = mongodb.MongoClient(uri)

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

@utilities.Debug_User_Input([mock_data.startingEntry1["date"],])
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

@utilities.Debug_User_Input([mock_data.startingEntry1["date"],"2021-01-01"])
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

@utilities.Debug_User_Input([f"{mock_data.startingEntry1['date']} . Midnight"])
def addMealEntry(user_input):
    """
    Adds a meal entry to the journal:
        Input format <date> <meal_path> <meal_name> 
    """
    cmds = user_input.split()
    if len(cmds) != 3:
        print("Error: Invalid command format")
        return
    date, meal_path, meal_name = cmds
    currentEntry = client.get_daily_journal(date)
    meal = currentEntry.processMealPath(meal_path)
    if meal is None:
        currentEntry.addMeal(data_models.Meal(name = meal_name))
    else:
        meal.addEntry(data_models.MealEntry(type = data_models.MealEntryType.MEAL, foodOrMeal = data_models.Meal(name = meal_name)))
    client.push_daily_journal(date, currentEntry)

@utilities.Debug_User_Input(f"{mock_data.startingEntry1['date']} Midnight Blueberries 1 cup 55")
def addFoodEntry(user_input):
    """
    Adds a food entry to the journal:
        Input format <date> <meal_path> <food> <quantity> <unit> <calories> 
    """
    cmds = user_input.split()
    if len(cmds) != 6:
        print("Error: Invalid command format")
        return
    date, meal_path, food, quantity, unit, calories = cmds
    quantity = int(quantity)
    calories = int(calories)
    
    entryForDate = client.get_daily_journal(date)

    try:
        mealObject = entryForDate.processMealPath(meal_path)
    except IndexError:
        print("Error: Meal path invalid")
        return
    
    foodObject = data_models.Food(name = food, quantity = quantity, unit = unit, calories = calories)
    mealObject.addEntry(data_models.MealEntry(type = data_models.MealEntryType.FOOD, foodOrMeal = foodObject))

    client.push_daily_journal(date, entryForDate)

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
    "add_to_meal": addMealEntry,
    "add_to_entry": addFoodEntry,
    "create_entry": createDailyEntry,
    "get_entry": getFullJournal,
}
if __name__ == "__main__":
    print("Running in production mode")
    app()
        