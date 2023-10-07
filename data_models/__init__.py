from typing import Optional
from typing import List
from typing import Union
from enum import Enum

class JsonSerializable:
    def toJson(self):
        return {k : v.toJson() if isinstance(v, JsonSerializable) else v
                 for k, v in self.__dict__.items() 
                 if not k.startswith("_") and not callable(v)}

class Food (JsonSerializable): 
    def __init__(self, name: str, quantity: int, unit: str, calories: int):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.calories = calories
    @classmethod
    def from_object(self, food: dict):
        return Food(food["name"], food["quantity"], food["unit"], food["calories"])

class MealEntryType(Enum):
    FOOD = 0
    MEAL = 1

class MealEntry (JsonSerializable):
    def __init__(self, type: [""], foodOrMeal: Union[Food, "Meal"]):
        self.type = type
        if self.type == MealEntryType.FOOD or self.type == MealEntryType.FOOD.name:
            self.food = Food.from_object(foodOrMeal)
        else:
            pass
    @classmethod
    def from_object(self, mealEntryDict: dict):
        return MealEntry(mealEntryDict["type"], mealEntryDict)

class Meal(JsonSerializable):
    def __init__(self, name: str, mealEntries: List[MealEntry] = []):
        self.name = name
        self.mealEntries = [MealEntry.from_object(entry) if not isinstance(entry, MealEntry) else entry for entry in mealEntries]
    @classmethod
    def from_object(self, meal: dict):
        return Meal(meal["name"], meal["entries"])
    def addMealEntry(self, mealEntry: MealEntry):
        self.mealEntries.append(mealEntry)

class DailyEntry(JsonSerializable):
    def __init__(self, date: str, meals: List[Meal] = []):
        self.date = date
        self.meals = [Meal.from_object(meal) if not isinstance(meal, Meal) else meal for meal in meals]
    @classmethod
    def from_object(self, dailyEntry: dict):
        return DailyEntry(dailyEntry["date"], dailyEntry["meals"])
    def getMealByName(self, name: str) -> Optional[Meal]:
        for meal in self.meals:
            if meal.name == name:
                return meal
        return None
    def addMeal(self, meal: Meal):
        self.meals.append(meal)

