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


def DailyEntry(date: str, meals: List[data_models.Meal] = []):
    return {
        "date": date,
        "meals": meals
    }


