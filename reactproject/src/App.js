import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from "react";
import { Meal } from './components/Meal';


export const maxIndentationDepth = (depth) => Math.min(3,depth);
//This is a awful system for keeping track of the current date, but it works for now
//I know contexts exist, I just want to goto bed. Sorry future me :P
export let currentDate = null;

function Entry(props){
  const date = props.date;
  const [entry, setEntry] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getEntry();
  }
  ,[]);

  async function getEntry() {
    const result = await fetch(`/api/daily/${date}`);
    const json = await result.json();
    console.log(json);
    setEntry(json);
    setLoading(false);
  }

  if(loading){
    return <div key = {date}>Loading...</div>
  }
  else if((entry.meals.length) > 0){
    return (<div key = {date}>
      {
        entry.meals.map((meal) => 
          <Meal refreshParentCallback = {props.refreshParentCallback} meal_path = {meal.name} key = {meal.name} className = "meal-details" meal = {meal}></Meal>
        )
      }
    </div>);
  }
  else{
    return (<div>
      <h1>Entry</h1>
      <p>No meals for this date</p>
    </div>);
  }

}

function Dates(){
  const [dates, setDates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeDate, setActiveDate_] = useState(null);

  function setActiveDate(date){
    setActiveDate_(date);
    currentDate = date;
  }

  useEffect(() => {
    getDates();
  },[]);

  async function getDates() {
    const result = await fetch("/api/summaries/dates");
    const json = await result.json();
    console.log(json);
    setDates(json);
    setActiveDate(json[0]);
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
      <section name = "journal">
        {activeDate !== null?
        <div>
            <div className = "journal-header">
              <h2 className = "inline">Journal for {activeDate}</h2>
              <button className = "inline right-aligned" onClick = {refreshEntry}>Refresh</button>
            </div>
            <Entry refreshParentCallback={refreshEntry} key={activeDate} date={activeDate}></Entry>
        </div>:
        <div>
          <h2>Journal</h2>
          <p>No date selected</p>
        </div>}
      </section>
      
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
