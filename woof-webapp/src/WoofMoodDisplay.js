// import "./styles.css";
import React from "react";
const moodEmojis = {
    happy: "😀",
    excited:"😆", 
    alert:"😳", 
    idle: "😴", 
    angry: "😡",
    sad: "😓"
}

function WoofMoodDisplay({moodData}) {
    let mood;
    {moodData.map((item) => (
        mood = item.Value
    ))}

  return (
    <div className="container">
      <h3>Mood</h3>
      {/* <span role="img" aria-label="emoji">{moodEmojis[mood]}</span> */}
      <h4>{mood}</h4>
    </div>
  );
}
export default WoofMoodDisplay;