import {useState } from "react";
import { Food } from './Food';
import { FoodAdder } from "./Food";
import {getModificationHandler} from "./jsonDataModifier"

const emptyMealObject = { name: "", entries: [], type: "MEAL" };
export const maxIndentationDepth = (depth) => Math.min(3, depth);

export function Meal({ meal, indentation = 0 }) {
  const [additionMode, setAdditionMode] = useState(null);
  const [editing, setEditing] = useState(false);
  const mealData = meal.jsonData;

  let computedIndentation = maxIndentationDepth(indentation);
  let calorieCount = calculateCalories(mealData.entries);

  function handleFoodAddition(newFoodObject) {
    setAdditionMode(null);
    if (newFoodObject !== null) {
      const newMealObject = { ...mealData, entries: [...mealData.entries, newFoodObject] };
      meal.onUpdate("Update",newMealObject); 
    }
  }

  function handleMealAddition(mealObjectToCreate){
    setAdditionMode(null);
    if (mealObjectToCreate !== null) {
      const newMealObject = { ...mealData, entries: [...mealData.entries, mealObjectToCreate] };
      meal.onUpdate("Update",newMealObject);
    }
  }

  function handleModification(modifiedMealObject){
    setEditing(false);
    meal.onUpdate("Update", modifiedMealObject);
  }

  

  function buildAdditionBar(){
    switch(additionMode){
      case "FOOD":
        return <FoodAdder updatedValuesCallback={handleFoodAddition}></FoodAdder>;
      case "MEAL":
        return <MealAdder updatedValuesCallback={handleMealAddition}></MealAdder>;
      default:
        return <>
            <button id="new-food-item" onClick={() => {setAdditionMode("FOOD")}}>Add Food</button>
            <button id="new-meal-item" onClick={() => {setAdditionMode("MEAL")}}>Add Meal</button>
        </>;
    }
  }

  function modificationCallback(newJson){
    console.log("My JSON was updated!")
    const newObject = { ...mealData, entries: [...newJson] };
    console.log(newObject);
    meal.onUpdate("Update",newObject);
  }

  return (<div className={computedIndentation > 0?`journal-indentation-${computedIndentation}`:""}>
    <div className="meal-header">
      {
        editing ?
        <MealAdder mealObject = {{...mealData} } updatedValuesCallback={handleModification}></MealAdder>:
        <h4 className="inline">{mealData.name} - {calorieCount} calories</h4>
      }
      
      <button className="inline right-aligned" onClick={() => {setEditing(true)}}>:</button>
      <button className="inline right-aligned" onClick={() => meal.onUpdate("Delete", null)}>-</button>
    </div>

    {mealData.entries.map((entry, entryIndex) => <div key={entry.name}>
      {entry.type === "FOOD" ?
        <Food indentation={computedIndentation} food={{"jsonData": entry, "onUpdate": getModificationHandler(mealData.entries, entryIndex, modificationCallback)}}></Food> :
        <Meal indentation={computedIndentation + 1} meal={{"jsonData": entry, "onUpdate": getModificationHandler(mealData.entries, entryIndex, modificationCallback)}}></Meal>
        }
    </div>
    )}

    <div className="meal-footer">
      {buildAdditionBar()}
    </div>
  </div>
  );
}

function calculateCalories(topLevelMeal){
  let queue = [...topLevelMeal];
  let calories = 0;
  while(queue.length > 0){
    let entry = queue.shift();
    if(entry.type === "FOOD"){
      calories += Number(entry.calories);
    }
    else{
      queue.push(...entry.entries);
    }
  }
  return calories;
}

export function MealAdder({ updatedValuesCallback, mealObject = emptyMealObject}) {
  const [mealState, setMealState] = useState(mealObject);
  function addMeal() {
    updatedValuesCallback({ ...mealState });
  }
  function saveInput(save_key) {
    return (e) => {
      let newMealState = { ...mealState, [save_key]: e.target.value };
      setMealState(newMealState)
    };
  }

  return <div className="MealAdder">
    <input className="inline" type="text" onInput={saveInput("name")} defaultValue={mealObject.name}></input>
    <button className="inline" onClick={addMeal}>Add</button>
  </div>;
}


