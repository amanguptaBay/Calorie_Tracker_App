import { useState } from "react";
import { maxIndentationDepth, currentDate } from '../App';

export function Food({ food, meal_path, refreshParentCallback, indentation = 0 }) {
  const [editing, setEditing] = useState(false);
  const [foodObject, setFoodObject] = useState(food);
  let computedIndentation = maxIndentationDepth(indentation);

  function getFoodChanges(foodChanges) {
    setEditing(false);
    const oldFoodObject = { ...foodObject };
    const newFoodObject = { ...foodObject, ...foodChanges };
    if (oldFoodObject !== newFoodObject) {
      setFoodObject(newFoodObject);
      fetch(`/api/daily/food/${currentDate}/${meal_path}`, {
        method: "PUT",
        body: JSON.stringify(newFoodObject),
      }).catch((err) => {
        //Rollback
        console.log(err);
        setFoodObject(oldFoodObject);
      });
    }
  }

  return (<div className={`journal-indentation-${computedIndentation}`} key={meal_path}>

    {editing ?
      <div>
        <FoodAdder foodObject={foodObject} updatedValuesCallback={getFoodChanges}></FoodAdder>
      </div> :
      <div>
        <p className="inline">{foodObject.name}: {foodObject.calories} calories</p>
        <button className="inline right-aligned" onClick={() => setEditing(true)}>:</button>
      </div>}
  </div>);
}export const emptyFoodObject = { name: "", calories: 0, quantity: 1, unit: "unit", type: "FOOD" };
export function FoodAdder({ updatedValuesCallback, foodObject = { emptyFoodObject } }) {
  const [foodState, setFoodState] = useState(foodObject);

  function addFood() {
    updatedValuesCallback({ ...foodState });
  }

  function saveInput(save_key) {
    return (e) => setFoodState({ ...foodState, [save_key]: e.target.value });
  }

  function cancel() {
    updatedValuesCallback(null);
  }
  return (<div>
    <input className="inline" type="text" onInput={saveInput("name")} defaultValue={foodObject.name}></input>:
    <input className="inline" type="number" onInput={saveInput("calories")} defaultValue={foodObject.calories}></input> calories
    <input className="inline" type="number" onInput={saveInput("quantity")} defaultValue={foodObject.quantity}></input>
    <input className="inline" type="text" onInput={saveInput("unit")} defaultValue={foodObject.unit}></input>
    <button className="inline" onClick={addFood}>Add</button>
    <button className="inline" onClick={cancel}>Cancel</button>
  </div>);
}

