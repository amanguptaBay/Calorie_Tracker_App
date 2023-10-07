import data_models
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
    def _push_mock_data(self, mock_data: data_models.DailyEntry):
        """
            Push mock data to the database
        """
        day_entries = self.db.get_collection("dailyEntries")
        day_entries.delete_many({})
        if day_entries.count_documents({}) == 0:
            return day_entries.insert_one(mock_data)
    def get_daily_calories(self, date) -> {str: int}:
        """
        Returns the calories by meal for a date
        """
        day_entries = self.db.get_collection("dailyEntries")
        data = day_entries.find_one({"date": date})
        return list(day_entries.aggregate([
            {"$match": {"date": date}},
            {"$unwind": "$meals"},
            #Brings meals to the top level (we want meals: total calories)
            {"$replaceRoot": {"newRoot": "$meals"}},
            #For each meal, keeps only the name and then computes the sum of calories
            {"$project": {"_id": 0, "name": 1, "calories": {"$sum": "$foods.calories"}}}
        ]))
    def create_daily_journal(self, date):
        """
            Creates a new daily journal
        """
        day_entries = self.db.get_collection("dailyEntries")
        data = day_entries.find_one({"date": date})
        if data is not None:
            print("Error: Daily journal already exists")
            return
        day_entries.insert_one(data_models.DailyEntry(date))
    def get_daily_journal(self, date) -> data_models.DailyEntry:
        """
            Fetches and returns the daily journal
        """
        day_entries = self.db.get_collection("dailyEntries")
        data = day_entries.find_one({"date": date})
        return data
    def push_daily_jounral(self, date, data: data_models.DailyEntry):
        """
            Pushes the daily journal to the database
        """
        day_entries = self.db.get_collection("dailyEntries")
        pushEvent = day_entries.update_one({"date": date}, {"$set": data})
        if pushEvent.modified_count == 0:
            print("Error: Server error")
            print(pushEvent.raw_result)
            return
    