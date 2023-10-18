import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from "react";
import { Meal, MealAdder } from './components/Meal';
import { useContext } from 'react';
import { CurrentDateContext } from './components/contexts/Date';
import {getModificationHandler} from "./components/jsonDataModifier"


function Entry({refreshCall}){
  const date = useContext(CurrentDateContext);
  const [entry, setEntry] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getEntry();
  },[date]);

  async function getEntry() {
    if(date != null){
      const result = await fetch(`/api/daily/${date}`);
      const json = await result.json();
      console.log("JSON from Server")
      console.log(json);
      setEntry(json);
      setLoading(false);
  }
  }

  function handleNewMealsObjectFromChild(newMeals){
    let newEntry = {...entry};
    let oldEntry = {...entry};
    newEntry.meals = [...newMeals];
    console.log(`Updating entry to`)
    console.log(newEntry)
    setEntry(newEntry);
    fetch(`/api/daily/${date}`, {
      method: "PUT",
      body: JSON.stringify(newEntry),
    }).then((res) => {
      console.log("Updated entry succesfully");
      console.log(res);
      refreshCall();
    }).catch((err) => {
      //Rollback
      console.log(err);
      setEntry(oldEntry);
      });
  }

  if(loading){
    return <div>Loading...</div>
  }
  else{
    return (<div>
      {
        entry.meals.length > 0?
        entry.meals.map((meal,index) => 
          <Meal className = "meal-details" key = {meal.name}  meal = {{"jsonData": meal, "onUpdate": getModificationHandler(entry.meals, index, handleNewMealsObjectFromChild)}}></Meal>
        ):
        <p> No meals</p>
      }

      <p>Add Meal:</p>
      <MealAdder updatedValuesCallback = {
        (newMeal) => getModificationHandler(entry.meals, entry.meals.length, handleNewMealsObjectFromChild)("Insert", newMeal)
      }></MealAdder>
    </div>);
  }


}

function Dates(){
  const [dates, setDates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeDate, setActiveDate_] = useState(null);

  function setActiveDate(date){
    setActiveDate_(date);
  }

  useEffect(() => {
    getDates();
  },[]);

  async function getDates() {
    const result = await fetch("/api/summaries/dates");
    const json = await result.json();
    console.log(json);
    setDates(json);
    if(activeDate === null)
    {
      setActiveDate(json[0]);
    }
    setLoading(false);
  }

  function changeActiveDateTo(date){
    return () => setActiveDate(date);
  }

  function refreshEntry(){
    let oldDate = activeDate;
    setActiveDate(null);
    setTimeout(() => setActiveDate(oldDate), 0);
  }

  if(loading){
    return <div>Loading...</div>
  }
  else{
    return <div>
      <section>
        <h2>Dates with Entries</h2>
        <ul>
          {dates.map((date) => <li className = "inline" key={date}>
            <button className = "inline" onClick = {changeActiveDateTo(date)}>{date}</button>
          </li>)}
        </ul>
      </section>
      <CurrentDateContext.Provider value={activeDate}>
        <section name = "journal">
            {activeDate !== null?
            <div>
                <div className = "journal-header">
                <h2 className = "inline">Journal for {activeDate}</h2>
                <button className = "inline right-aligned" onClick = {refreshEntry}>Refresh</button>
                </div>
                <Entry refreshCall = {refreshEntry}></Entry>
            </div>:
            <div>
            <h2>Journal</h2>
            <p>No date selected</p>
            </div>}
        </section>
    </CurrentDateContext.Provider>
      
    </div>
  }
  
  
}

function App() {
  return (
    <div className="App">
      <Dates />
    </div>
  );
}

export default App;
