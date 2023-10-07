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

def Meal(name: str, foods: Optional[List[data_models.Food]] = None):
    return {
        "name": name,
        "foods":  foods or []
    }


def DailyEntry(date: str, meals: Optional[List[data_models.Meal]] = None):
    return {
        "date": date,
        "meals": meals or []
    }


