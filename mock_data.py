import json

currentDate = "2023-10-06"
startingEntry = """{
  "date": "2023-10-06",
  "meals": [
    {
      "name": "Breakfast",
      "foods": [
        {
          "name": "Scrambled Eggs",
          "quantity": "2",
          "unit": "eggs",
          "calories": 140
        },
        {
          "name": "Whole Wheat Toast",
          "quantity": "2",
          "unit": "slices",
          "calories": 160
        },
        {
          "name": "Banana",
          "quantity": "1",
          "unit": "medium",
          "calories": 105
        },
        {
          "name": "Coffee",
          "quantity": "1",
          "unit": "cup",
          "calories": 2
        }
      ]
    },
    {
      "name": "Lunch",
      "foods": [
        {
          "name": "Grilled Chicken Salad",
          "quantity": "1",
          "unit": "bowl",
          "calories": 350
        },
        {
          "name": "Dressing (Vinaigrette)",
          "quantity": "2",
          "unit": "tablespoons",
          "calories": 70
        },
        {
          "name": "Brown Rice",
          "quantity": "1",
          "unit": "cup",
          "calories": 215
        },
        {
          "name": "Water",
          "quantity": "1",
          "unit": "glass",
          "calories": 0
        }
      ]
    },
    {
      "name": "Dinner",
      "foods": [
        {
          "name": "Salmon",
          "quantity": "1",
          "unit": "fillet",
          "calories": 367
        },
        {
          "name": "Steamed Broccoli",
          "quantity": "1",
          "unit": "cup",
          "calories": 55
        },
        {
          "name": "Quinoa",
          "quantity": "1",
          "unit": "cup",
          "calories": 220
        },
        {
          "name": "Lemonade",
          "quantity": "1",
          "unit": "glass",
          "calories": 120
        }
      ]
    },
    {
      "name": "Snacks",
      "foods": [
        {
          "name": "Apple",
          "quantity": "1",
          "unit": "medium",
          "calories": 95
        },
        {
          "name": "Almonds",
          "quantity": "1",
          "unit": "handful",
          "calories": 100
        },
        {
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