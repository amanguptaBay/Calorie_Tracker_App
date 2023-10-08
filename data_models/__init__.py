from typing import Optional
from typing import List
from typing import Union
from enum import Enum

class JsonSerializable:
    def toJson(self):
        output = {}
        for k, v in self.__dict__.items():
            if not k.startswith("_") and not callable(v):
                if isinstance(v, JsonSerializable):
                    output[k] = v.toJson()
                elif isinstance(v, list):
                    output[k] = []
                    if len(v) > 0:
                        for entry in v:
                            output[k].append(entry.toJson() if isinstance(entry, JsonSerializable) else entry)
                else:
                    output[k] = v
        return output
    @classmethod
    def from_object(self, arg: Union[dict, "JsonSerializable"]):
        return self(**arg) if isinstance(arg, dict) else arg

class Food (JsonSerializable): 
    def __init__(self,*args, name: str, quantity: int, unit: str, calories: int, **kwargs):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.calories = calories

class MealEntryType(Enum, JsonSerializable):
    FOOD = 0
    MEAL = 1
    def toJson(self):
        return self.name

class MealEntry (JsonSerializable):
    def __init__(self, *args, type: [""], foodOrMeal: Union[Food, "Meal"], **kwargs):
        self.type = MealEntryType[type] if isinstance(type, str) else type
        if self.type == MealEntryType.FOOD or self.type == MealEntryType.FOOD.name:
            self.object = Food.from_object(foodOrMeal)
        else:
            self.object = Meal.from_object(foodOrMeal)

class Meal(JsonSerializable):
    def __init__(self, *args, name: str, entries: List[MealEntry] = [], **kwargs):
        self.name = name
        self.entries = [MealEntry.from_object(entry) if not isinstance(entry, MealEntry) else entry for entry in entries]
    def addEntry(self, entry: MealEntry):
        self.entries.append(entry)

class DailyEntry(JsonSerializable):
    def __init__(self,*args, date: str, meals: List[Meal] = [], **kwargs):
        self.date = date
        self.meals = [Meal.from_object(meal) if not isinstance(meal, Meal) else meal for meal in meals]
    def getMealByName(self, name: str) -> Optional[Meal]:
        for meal in self.meals:
            if meal.name == name:
                return meal
        return None
    def processMealPath (self, meal_path:str) -> Union[Meal, Food, None]:
        """
            Given a meal path, returns the meal or food object it refers to in the daily entry
            Meal path format: <meal name>/<index>/.../<index>, meal entries can be further indexed, food items are atomics
        """

        meal_path = meal_path.split("/")
        mealName = meal_path.pop(0)
        meal = self.getMealByName(mealName)
        for ind, meal_path_index in enumerate(meal_path):
            if meal is None:
                return None
            if meal.type != MealEntryType.MEAL:
                return meal if ind == len(meal_path) - 1 else None
            meal_path_index = int(meal_path_index)
            meal = meal.entries[meal_path_index].object
        return meal

    def addMeal(self, meal: Meal):
        self.meals.append(meal)

