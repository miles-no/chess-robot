import React, { useState, useEffect } from "react";

function App() {
  const [data, setdata] = useState([
    {
      name: "",
      age: "",
      date: "",
      programming: "",
    },
  ]);

  useEffect(() => {
    fetch("/data")
      .then((res) => res.json())
      .then((data) => {
        setdata({
          name: data.Name,
          age: data.Age,
          date: data.Date,
          programming: data.Programming,
        });
        console.log(data);
      });
  }, []);

  return (
    <div>
      <p>{data.name}</p>
      <p>{data.age}</p>
      <p>{data.date}</p>
      <p>{data.programming}</p>
    </div>
  );
}

export default App;
