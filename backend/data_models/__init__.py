from typing import Optional
from typing import List
from typing import Union
from enum import Enum

class JsonSerializable:
    """
        A class that can be serialized to json
    """

    def _toJson(self, obj):
        """
            Converts a object to Json.
        """
        if isinstance(obj, JsonSerializable):
            return obj.toJson()
        elif isinstance(obj, list):
            return [self._toJson(entry) for entry in obj]
        elif isinstance(obj, dict):
            return {k: self._toJson(v) for k, v in obj.items()}
        else:
            return obj

    def toJson(self):
        output = {}
        for k, v in self.__dict__.items():
            if not k.startswith("_") and not callable(v):
                output[k] = self._toJson(v)
        return output
    
    def __repr__(self):
        return str(self.toJson())
class JsonInitializable (JsonSerializable):
    """
        A class that can be initialized from a json object by passing it the object's dictionary representation.
        The class constructor must allow for no arguments to be passed, along with *args and **kwargs, this is to allow for dictionary splatting to intialize the object.
    """
    @classmethod
    def from_object(self, arg: Union[dict, "JsonSerializable"]):
        return self(**arg) if isinstance(arg, dict) else arg

class Food (JsonInitializable): 
    def __init__(self,*args, name: str, quantity: int, unit: str, calories: int, **kwargs):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.calories = calories

class MealEntryType(JsonSerializable, Enum):
    FOOD = 0
    MEAL = 1
    def toJson(self):
        return self.name

class MealEntry (JsonInitializable):
    def __init__(self, *args, type: [""], foodOrMeal: Union[Food, "Meal"] = None, **kwargs):
        self.type = MealEntryType[type] if isinstance(type, str) else type
        if self.type == MealEntryType.FOOD or self.type == MealEntryType.FOOD.name:
            self.object = Food.from_object(foodOrMeal) if foodOrMeal is not None else Food(**kwargs)
        else:
            self.object = Meal.from_object(foodOrMeal) if foodOrMeal is not None else Meal(**kwargs)
    def toJson(self):
        #Object is a convenience property, actually a named sub-element of the entry object
        output = {
            "type": self._toJson(self.type),
        }
        output.update(self._toJson(self.object))
        return output

class Meal(JsonInitializable):
    def __init__(self, *args, name: str, entries: List[MealEntry] = [], **kwargs):
        self.name = name
        self.entries = [MealEntry.from_object(entry) if not isinstance(entry, MealEntry) else entry for entry in entries]
    def addEntry(self, entry: MealEntry):
        self.entries.append(entry)

class DailyEntry(JsonInitializable):
    def __init__(self,*args, date: str, meals: List[Meal] = [], **kwargs):
        self.date = date
        self.meals = [Meal.from_object(meal) if not isinstance(meal, Meal) else meal for meal in meals]
    def getMealByName(self, name: str) -> Optional[Meal]:
        for meal in self.meals:
            if meal.name == name:
                return meal
        return None
    def processMealPath (self, meal_path:str) -> Optional[Union[Meal, Food]]:
        """
            Given a meal path, returns the meal or food object it refers to in the daily entry
            Meal path format: <meal name>/<index>/.../<index>, meal entries can be further indexed, food items are atomics
            Raises IndexError if the path is out of bounds, None if path is within bounds but no object there.
        """

        meal_path = meal_path.split("/")
        mealName = meal_path.pop(0)
        if mealName == "" or mealName == ".":
            return None
        meal = self.getMealByName(mealName)
        if meal is None:
            raise IndexError("Parent meal not found")
        for ind, meal_path_index in enumerate(meal_path):
            meal_path_index = meal_path_index.strip()
            if meal_path_index == ".":
                continue
            if meal_path_index == "":
                continue
            meal_path_index = int(meal_path_index)
            err = None
            try:
                meal = meal.entries[meal_path_index].object
            except AttributeError:
                #Trying to index a food, renames error to be easier to understand whats going on
                err = IndexError("Meal path index out of bounds, trying to index a non-indexable object")
            if err is not None:
                raise err
        return meal

    def addMeal(self, meal: Meal):
        self.meals.append(meal)

