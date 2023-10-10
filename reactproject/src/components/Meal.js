import { useState } from "react";
import { Food, emptyFoodObject } from './Food';
import { currentDate, maxIndentationDepth} from '../App';
import { FoodAdder } from "./Food";

const emptyMealObject = { name: "", entries: [], type: "MEAL" };

export function Meal({ meal, meal_path, refreshParentCallback, indentation = 1 }) {

  const [addingEntries, setAddingEntries] = useState(false);

  const [addingFood, setAddingFood] = useState(false);
  const [addingMeal, setAddingMeal] = useState(false);
  const [mealObject, setMealObject] = useState(meal);

  function handleFoodAddition(newFoodObject) {
    setAddingFood(false);
    setAddingEntries(false);
    if (newFoodObject !== null) {
      const oldMealObject = { ...mealObject };
      const newMealObject = { ...mealObject, entries: [...mealObject.entries, newFoodObject] };
      setMealObject(newMealObject);
      fetch(`/api/daily/food/${currentDate}/${meal_path}`, {
        method: "POST",
        body: JSON.stringify(newFoodObject),
      }).catch((err) => {
        //Rollback
        console.log(err);
        setMealObject(oldMealObject);
      });
    }
  }

  function handleMealAddition(mealObjectToCreate){
    setAddingMeal(false);
    setAddingEntries(false);
    if (mealObjectToCreate !== null) {
      console.log("Adding meal: "+JSON.stringify(mealObjectToCreate));
      //Endpoint: /api/daily/meal/<date>/<path:meal_path>
      const oldMealObject = { ...mealObject };
      const newMealObject = { ...mealObject, entries: [...mealObject.entries, mealObjectToCreate] };
      setMealObject(newMealObject);
      fetch(`/api/daily/meal/${currentDate}/${meal_path}`, {
        method: "POST",
        body: JSON.stringify(mealObjectToCreate),
      }).catch((err) => {
        //Rollback
        console.log(err);
        setMealObject(oldMealObject);
      });
    }
  }

  let computedIndentation = maxIndentationDepth(indentation);

  return (<div className={`journal-indentation-${computedIndentation}`} key={mealObject.name}>
    <div className="meal-header">
      <h4 className="inline">{mealObject.name}</h4>
      <button className="inline right-aligned">:</button>
      <button className="inline right-aligned">-</button>
    </div>

    {mealObject.entries.map((entry, entryIndex) => <div key={entry.name}>
      {entry.type === "FOOD" ?
        <Food refreshParentCallback={refreshParentCallback} meal_path={`${meal_path}/${entryIndex}`} indentation={computedIndentation} food={entry}></Food> :
        <Meal refreshParentCallback={refreshParentCallback} meal_path={`${meal_path}/${entryIndex}`} indentation={computedIndentation + 1} meal={entry}></Meal>}
    </div>
    )}

    <div className="meal-footer">
      {addingEntries ?
        <div className="inline" id="EntryAddition">

          {addingFood ?
            <FoodAdder foodObject={{ ...emptyFoodObject }} updatedValuesCallback={handleFoodAddition}></FoodAdder> :
            <button id="new-food-item" onClick={() => { setAddingFood(true); }}>Add Food</button>}

          {addingMeal ?
            <MealAdder mealObject={{ ...emptyMealObject }} updatedValuesCallback={handleMealAddition}></MealAdder> :
            <button id="new-meal-item" onClick={() => { setAddingMeal(true); }}>Add Meal</button>}  
          
          <button className="inline" onClick={() => setAddingEntries(false)}>... Hide Entries</button>
        </div> :
        <button onClick={() => setAddingEntries(true)}>... Add Entries</button>}
    </div>
  </div>
  );
}

function MealAdder({ updatedValuesCallback, mealObject = { emptyMealObject } }) {
  const [mealState, setMealState] = useState(mealObject);

  function addMeal() {
    updatedValuesCallback({ ...mealState });
  }
  function saveInput(save_key) {
    return (e) => setMealState({ ...mealState, [save_key]: e.target.value });
  }

  return <div class="MealAdder">
    <input className="inline" type="text" onInput={saveInput("name")} defaultValue={mealObject.name}></input>
    <button className="inline" onClick={addMeal}>Add</button>
  </div>;
}

