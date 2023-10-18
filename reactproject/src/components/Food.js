import { useContext, useState } from "react";
import { maxIndentationDepth } from "./Meal";
import { CurrentDateContext } from "./contexts/Date";
export function Food({ food, indentation = 0}) {
  const [editing, setEditing] = useState(false);
  const foodObject = (food.jsonData);
  const currentDate = useContext(CurrentDateContext);
  let computedIndentation = maxIndentationDepth(indentation);

  function onFoodChange(foodChanges) {
    setEditing(false);
    food.onUpdate("Update",{ ...foodObject, ...foodChanges });
  }

  return (<div className={`journal-indentation-${computedIndentation}`}>

    {editing ?
      <>
        <FoodAdder foodObject={foodObject} updatedValuesCallback={onFoodChange}></FoodAdder>
      </> :
      <>
        <p className="inline">{foodObject.name}: {foodObject.calories} calories</p>
        <button className="inline right-aligned" onClick={() => setEditing(true)}>:</button>
        <button className="inline right-aligned" onClick={() => food.onUpdate("Delete", null)}>-</button>
      </>}
  </div>);
}
export const emptyFoodObject = { name: "", calories: 0, quantity: 1, unit: "unit", type: "FOOD" };
export function FoodAdder({ updatedValuesCallback, foodObject = emptyFoodObject}) {
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

