"""
Libraries contain a collection of food entries.
Currently, will be stored as a document. In the future this should be some kind of model where each library is a collection and each entry is a document.
"""
from data_models.json_logic import JsonInitializable
from data_models.journal import Food
class Library(JsonInitializable):
    def __init__(self, *args, name: str, contents: [Food], **kwargs):
        self.name = name
        self.contents = [Food.from_object(food) for food in contents]

class Tag(JsonInitializable):
    def __init__(self, *args, name: str, value: str, **kwargs):
        self.name = name
        self.value = value

class FoodDescription(JsonInitializable):
    def __init__(self, *args, tags = [Tag], **kwargs):
        self.foodObject = Food.from_object(kwargs)
    def toJson(self):
        output = {}
        output.update(self._toJson(self.foodObject))

