from typing import Optional
from typing import List
import data_models

def Food(name: str, quantity: int, unit: str, calories: int):
    return {
        "name": name,
        "quantity": quantity,
        "unit": unit,
        "calories": calories
    }

def Meal(name: str, foods: List[data_models.Food] = []):
    return {
        "name": name,
        "foods":  foods
    }

def addFoodToMeal(meal: data_models.Meal, food: data_models.Food):
    meal["foods"].append(food)

def DailyEntry(date: str, meals: List[data_models.Meal] = []):
    return {
        "date": date,
        "meals": meals
    }

def getMealByName(dailyEntry: data_models.DailyEntry, name: str) -> Optional[data_models.Meal]:
    for meal in dailyEntry["meals"]:
        if meal["name"] == name:
            return meal
    return None

def addMealToDailyEntry(dailyEntry: data_models.DailyEntry, meal: data_models.Meal):
    dailyEntry["meals"].append(meal)

