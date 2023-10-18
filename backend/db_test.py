import unittest
import data_models.journal
from data_connector.mongodb import MongoClient as Database
import data_models
import configparser

"""
Designed to test our data-connector along with our data models to ensure that they are working as expected.
Also outlines usage of the data-connector and data models.
"""

config = configparser.ConfigParser()
config.read("config.ini")
uri = config.get("database", "uri")

class TestDailyEntries(unittest.TestCase):
    def setUp(self):
        self.db = Database(uri)
        self.db._clean_db()

    def test_create_daily_entries(self):
        db = self.db
        db.create_daily_journal("2023-01-01")
        db.create_daily_journal("2023-01-02")
        db.create_daily_journal("2023-01-03")
        self.assertEqual(db.dates_with_entries(), ["2023-01-01", "2023-01-02", "2023-01-03"])

class TestSimpleMealEntries(unittest.TestCase):
    def setUp(self):
        self.db = Database(uri)
        self.db._clean_db()
        self.db.create_daily_journal("2023-01-01")
        self.db.create_daily_journal("2023-01-02")
        self.db.create_daily_journal("2023-01-03")
    def test_create_simple_meals(self):
        db = self.db
        journal = db.get_daily_journal("2023-01-01")
        journal.addMeal(data_models.journal.Meal(name = "Breakfast"))
        journal.addMeal(data_models.journal.Meal(name = "Lunch"))
        journal.addMeal(data_models.journal.Meal(name = "Snack"))
        journal.addMeal(data_models.journal.Meal(name = "Dinner"))
        db.push_daily_journal(journal)
        self.assertEqual(len(db.get_daily_journal("2023-01-01").meals), 4)

    def test_add_simple_foods(self):
        db = self.db
        journal = db.get_daily_journal("2023-01-01")
        journal.addMeal(data_models.journal.Meal(name = "Breakfast"))
        journal.getMealByName("Breakfast").addEntry(data_models.journal.MealEntry(type = data_models.journal.MealEntryType.FOOD, foodOrMeal = data_models.journal.Food(name = "Extra-Large Eggs", quantity = 2, unit = "eggs", calories = 140)))
        journal.getMealByName("Breakfast").addEntry(data_models.journal.MealEntry(type = data_models.journal.MealEntryType.FOOD, foodOrMeal = data_models.journal.Food(name = "Spinach", quantity = 32, unit = "grams", calories = 10)))
        journal.getMealByName("Breakfast").addEntry(data_models.journal.MealEntry(type = data_models.journal.MealEntryType.FOOD, foodOrMeal = data_models.journal.Food(name = "Tomato", quantity = 1.5, unit = "tomatos", calories = 20)))
        db.push_daily_journal(journal)
        self.assertEqual(db.get_daily_calories("2023-01-01")["Breakfast"], 170)
if __name__ == '__main__':
    unittest.main()