import json

currentDate = "2023-10-06"
startingEntry = """{
  "date": "2023-10-06",
  "meals": [
    {
      "name": "Breakfast",
      "entries": [
        {
         "type": "FOOD",
          "name": "Scrambled Eggs",
          "quantity": "2",
          "unit": "eggs",
          "calories": 140
        },
        {
         "type": "FOOD",
          "name": "Whole Wheat Toast",
          "quantity": "2",
          "unit": "slices",
          "calories": 160
        },
        {
         "type": "FOOD",
          "name": "Banana",
          "quantity": "1",
          "unit": "medium",
          "calories": 105
        },
        {
          "type": "FOOD",
          "name": "Coffee",
          "quantity": "1",
          "unit": "cup",
          "calories": 2
        }
      ]
    },
    {
      "name": "Lunch",
      "entries": [
        {
          "type": "FOOD",
          "name": "Grilled Chicken Salad",
          "quantity": "1",
          "unit": "bowl",
          "calories": 350
        },
        {
          "type": "FOOD",
          "name": "Dressing (Vinaigrette)",
          "quantity": "2",
          "unit": "tablespoons",
          "calories": 70
        },
        {
          "type": "FOOD",
          "name": "Brown Rice",
          "quantity": "1",
          "unit": "cup",
          "calories": 215
        },
        {
          "type": "FOOD",
          "name": "Water",
          "quantity": "1",
          "unit": "glass",
          "calories": 0
        }
      ]
    },
    {
      "name": "Dinner",
      "entries": [
        {
          "type": "FOOD",
          "name": "Salmon",
          "quantity": "1",
          "unit": "fillet",
          "calories": 367
        },
        {
          "type": "FOOD",
          "name": "Steamed Broccoli",
          "quantity": "1",
          "unit": "cup",
          "calories": 55
        },
        {
          "type": "FOOD",
          "name": "Quinoa",
          "quantity": "1",
          "unit": "cup",
          "calories": 220
        },
        {
          "type": "FOOD",
          "name": "Lemonade",
          "quantity": "1",
          "unit": "glass",
          "calories": 120
        }
      ]
    },
    {
      "name": "Snacks",
      "entries": [
        {
          "type": "FOOD",
          "name": "Apple",
          "quantity": "1",
          "unit": "medium",
          "calories": 95
        },
        {
          "type": "FOOD",
          "name": "Almonds",
          "quantity": "1",
          "unit": "handful",
          "calories": 100
        },
        {
          "type": "FOOD",
          "name": "Yogurt",
          "quantity": "1",
          "unit": "container",
          "calories": 150
        }
      ]
    }
  ]
}
"""
startingEntry = json.loads(startingEntry)