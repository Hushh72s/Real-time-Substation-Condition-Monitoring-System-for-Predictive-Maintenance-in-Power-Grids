import React, { useEffect, useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement);

function App() {
  const [history, setHistory] = useState([]);
  const [status, setStatus] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      axios.get("http://127.0.0.1:8001/latest")
        .then(res => {
          setHistory(prev => [...prev.slice(-20), res.data]);
          setStatus(res.data.anomaly);
        });
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const labels = history.map((_, i) => i);

  const makeDataset = (label, key, color) => ({
    labels,
    datasets: [
      {
        label,
        data: history.map(d => d[key]),
        borderColor: color,
        fill: false
      }
    ]
  });

  return (
    <div style={{ background:"#0f172a", minHeight:"100vh", color:"white", padding:"20px" }}>
      
      <h1 style={{textAlign:"center"}}>⚡ Substation Monitoring Dashboard</h1>

      <h2 style={{color: status ? "red":"lime", textAlign:"center"}}>
        {status ? "⚠ ANOMALY DETECTED" : "✔ SYSTEM NORMAL"}
      </h2>

      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:"20px"}}>

        <Line data={makeDataset("Temperature","temperature","orange")} />
        <Line data={makeDataset("Humidity","humidity","cyan")} />

        <Line data={makeDataset("Voltage","voltage","yellow")} />
        <Line data={makeDataset("Vibration","vibration","magenta")} />

      </div>

    </div>
  );
}

export default App;