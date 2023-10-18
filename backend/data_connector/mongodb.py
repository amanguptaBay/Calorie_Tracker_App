import data_models.library
import data_models.journal
import pymongo

class MongoClient():
    def __init__(self, uri):
        self.uri = uri        
        client = pymongo.mongo_client.MongoClient(uri)
        try:
            client.admin.command('ping')
        except Exception as e:
            print(e)
        self.client = client
        self.db = client.get_database("mock_tracker")

    def dates_with_entries(self) -> [str]:
        """
            Returns a list of dates with entries
        """
        day_entries = self.db.get_collection("dailyEntries")
        return [entry["date"] for entry in day_entries.find({})]
    def _clean_db(self):
        """
            Cleans the database
        """
        self.db.get_collection("dailyEntries").delete_many({})
        self.db.get_collection("library").delete_many({})
    def _push_mock_journal(self, mock_data: data_models.journal.JournalEntry):
        """
            Push mock data to the database
        """
        day_entries = self.db.get_collection("dailyEntries")
        return day_entries.insert_one(mock_data.toJson())
    def _push_mock_library(self, mock_data: data_models.library.Library):
        """
            Push mock data to the database
        """
        library = self.db.get_collection("library")
        return library.insert_one(mock_data.toJson())
    def get_daily_calories(self, date) -> {str: int}:
        """
        Returns the calories by meal for a date
        """
        day_entries = self.db.get_collection("dailyEntries")
        data = day_entries.find_one({"date": date})
        if data is None:
            print("Error: Daily journal not found")
            return
        data = data_models.journal.JournalEntry.from_object(data)
        workQueue = []
        for meal in data.meals:
            workQueue += [{"action":"process", "object": entry.object} for entry in meal.entries]
            workQueue += [{"action":"store", "mealName" : meal.name}]

        caloriesByMeal = {}
        currentMealCalories = 0
        while len(workQueue) > 0:
            task = workQueue.pop(0)
            action = task["action"]
            if action == "store":
                caloriesByMeal[task["mealName"]] = currentMealCalories
                currentMealCalories = 0
            elif action == "process":
                object = task["object"]
                if isinstance(object, data_models.journal.Food):
                    currentMealCalories += object.calories
                elif isinstance(object, data_models.journal.Meal):
                    workQueue += [{"action":"process", "object": entry.object} for entry in object.entries]
        return caloriesByMeal
        
    def create_daily_journal(self, date):
        """
            Creates a new daily journal
        """
        day_entries = self.db.get_collection("dailyEntries")
        data = day_entries.find_one({"date": date})
        if data is not None:
            print("Error: Daily journal already exists")
            return
        newEntry = data_models.journal.JournalEntry(date = date)
        day_entries.insert_one(newEntry.toJson())
    def get_daily_journal(self, date) -> data_models.journal.JournalEntry:
        """
            Fetches and returns the daily journal
        """
        day_entries = self.db.get_collection("dailyEntries")
        data = day_entries.find_one({"date": date})
        return data_models.journal.JournalEntry.from_object(data)
    def push_daily_journal(self, data: data_models.journal.JournalEntry):
        """
            Pushes the daily journal to the database
        """
        day_entries = self.db.get_collection("dailyEntries")
        date = data.date
        pushEvent = day_entries.update_one({"date": date}, {"$set": data.toJson()})
        if pushEvent.modified_count == 0:
            print("Error: Server error")
            print(pushEvent.raw_result)
            return False
        return True
    