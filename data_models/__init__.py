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
    def from_object(self, *args, **kwargs):
        return self(*args, **kwargs)

class Food (JsonSerializable): 
    def __init__(self,*args, name: str, quantity: int, unit: str, calories: int, **kwargs):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.calories = calories
    @classmethod
    def from_object(self, food: dict):
        if isinstance(food, Food):
            return food
        return Food(**food)

class MealEntryType(Enum):
    FOOD = 0
    MEAL = 1

class MealEntry (JsonSerializable):
    def __init__(self, type: [""], foodOrMeal: Union[Food, "Meal"]):
        self.type = MealEntryType[type] if isinstance(type, str) else type
        if self.type == MealEntryType.FOOD or self.type == MealEntryType.FOOD.name:
            self.object = Food.from_object(foodOrMeal)
        else:
            self.object = Meal.from_object(foodOrMeal)
    @classmethod
    def from_object(self, mealEntryDict: dict):
        if isinstance(mealEntryDict, MealEntry):
            return MealEntry(mealEntryDict["type"], mealEntryDict["object"])
        return MealEntry(mealEntryDict["type"], mealEntryDict)
    def toJson(self):
        output = {
            "type": self.type.name,
        }
        output.update(self.object.toJson())
        return output

class Meal(JsonSerializable):
    def __init__(self, name: str, entries: List[MealEntry] = []):
        self.name = name
        self.entries = [MealEntry.from_object(entry) if not isinstance(entry, MealEntry) else entry for entry in entries]
    @classmethod
    def from_object(self, meal: dict):
        if isinstance(meal, Meal):
            return meal
        return Meal(meal["name"], meal["entries"])
    def addMealEntry(self, entry: MealEntry):
        self.entries.append(entry)

class DailyEntry(JsonSerializable):
    def __init__(self, date: str, meals: List[Meal] = []):
        self.date = date
        self.meals = [Meal.from_object(meal) if not isinstance(meal, Meal) else meal for meal in meals]
    @classmethod
    def from_object(self, dailyEntry: dict):
        if isinstance(dailyEntry, DailyEntry):
            return dailyEntry
        return DailyEntry(dailyEntry["date"], dailyEntry["meals"])
    def getMealByName(self, name: str) -> Optional[Meal]:
        for meal in self.meals:
            if meal.name == name:
                return meal
        return None
    def addMeal(self, meal: Meal):
        self.meals.append(meal)

