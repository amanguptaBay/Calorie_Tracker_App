import unittest
from datetime import datetime, timedelta
import mock_app

"""
    Tests mock_app functionality by querying the database
"""

class TestDailyEntries(unittest.TestCase):
    #Be careful about modifying this, it will affect other test cases beyond creation of daily entries
    dates = ["2023-01-01", "2023-01-02", "2023-01-03"]
    def setUp(self):
        self.client = mock_app.client
        self.client._clean_db()

    def test_create_daily_entries(self):
        mock_app.createDailyEntry("2023-01-01")
        mock_app.createDailyEntry("2023-01-02")
        mock_app.createDailyEntry("2023-01-03")
        self.assertEqual(self.client.dates_with_entries(), ["2023-01-01", "2023-01-02", "2023-01-03"])
    

class TestSimpleMealEntries(unittest.TestCase):
    def setUp(self):
        self.client = mock_app.client
        self.client._clean_db()
        mock_app.createDailyEntry("2023-01-01")
        mock_app.createDailyEntry("2023-01-02")
        mock_app.createDailyEntry("2023-01-03")

    def test_create_simple_meal(self):
        mock_app.addMealEntry("2023-01-01 . Breakfast")
        mock_app.addMealEntry("2023-01-01 . Lunch")
        mock_app.addMealEntry("2023-01-01 . Dinner")
        self.assertEqual(len(self.client.get_daily_journal("2023-01-01").meals), 3)

    def test_create_simple_meal_invalid_path(self):
        with self.assertRaises(IndexError):
            mock_app.addMealEntry("2023-01-01 Breakfast/ Chicken_Salad")

    def test_add_simple_foods(self):
        mock_app.addMealEntry("2023-01-01 . Breakfast")
        mock_app.addMealEntry("2023-01-01 . Lunch")
        mock_app.addMealEntry("2023-01-01 . Dinner")
        mock_app.addFoodEntry("2023-01-01 Breakfast Eggs 2 eggs 100")
        mock_app.addFoodEntry("2023-01-01 Breakfast Bacon 3 slices 200")
        mock_app.addFoodEntry("2023-01-01 Lunch Salad 1 cup 50")
        mock_app.addFoodEntry("2023-01-01 Lunch Chicken 1 breast 200")
        mock_app.addFoodEntry("2023-01-01 Lunch Dressing 1 tbsp 100")
        mock_app.addFoodEntry("2023-01-01 Lunch Bread 1 slice 100")
        mock_app.addFoodEntry("2023-01-01 Dinner Steak 1 steak 300")
        mock_app.addFoodEntry("2023-01-01 Dinner Potatoes 1 cup 100")
        #Each meal has correct number of entries
        self.assertEqual(len(self.client.get_daily_journal("2023-01-01").getMealByName("Breakfast").entries), 2)
        self.assertEqual(len(self.client.get_daily_journal("2023-01-01").getMealByName("Lunch").entries), 4)
        self.assertEqual(len(self.client.get_daily_journal("2023-01-01").getMealByName("Dinner").entries), 2)

    def test_add_simple_foods_invalid_path(self):
        mock_app.addMealEntry("2023-01-01 . Breakfast")
        mock_app.addFoodEntry("2023-01-01 Lunch Eggs 2 eggs 100")
        self.assertEqual(len(self.client.get_daily_journal("2023-01-01").getMealByName("Breakfast").entries), 0)

class TestComplexMealEntries(unittest.TestCase):
        def setUp(self):
            self.client = mock_app.client
            self.client._clean_db()
            mock_app.createDailyEntry("2023-01-01")
            mock_app.addMealEntry("2023-01-01 . Breakfast")

        def test_create_nested_meal(self):
            mock_app.addMealEntry("2023-01-01 Breakfast Omlette")
            self.assertNotEqual(self.client.get_daily_journal("2023-01-01").processMealPath("Breakfast/0"), None)

        def test_full_nested_meal(self):
            mock_app.addMealEntry("2023-01-01 Breakfast Omlette")
            mock_app.addFoodEntry("2023-01-01 Breakfast/0 Eggs 2 eggs 100")
            mock_app.addFoodEntry("2023-01-01 Breakfast/0 Bacon 3 slices 200")
            self.assertEqual(len(self.client.get_daily_journal("2023-01-01").getMealByName("Breakfast").entries), 1)
            self.assertEqual(len(self.client.get_daily_journal("2023-01-01").processMealPath("Breakfast/0").entries), 2)


if __name__ == '__main__':
    unittest.main()