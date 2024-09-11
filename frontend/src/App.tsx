import './App.css';
import "path";

import { useState, useEffect, ChangeEvent } from "react";
import { Item, ItemViewer } from "./ItemViewer";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
const APP_REFRESH_INTERVAL_MS = 5000;

function App() {
  const [items, setItems] = useState<Item[]>([]);
  const [showValues, setShowValues] = useState<boolean>(true);
  const [file, setFile] = useState<File>();
  const [uploadSuccess, setUploadSuccess] = useState<boolean>(true);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  }

  const updateItems = async () => {
    const response = await fetch(`${BACKEND_URL}/db/list_values`, {
      method: "GET",
      headers: {
        "Access-Control-Allow-Origin": "*"
      }
    });
    const values: Map<number, number[]> = new Map(
      Object.entries(await response.json())
        .map(([id, values]) => [Number(id), values as number[]])
    );
    const items: Item[] = Array.from(values.entries())
      .map(([id, values]) => ({ id, values }));
    setItems(items);
  };
  
  const addItems = async () => {
    if (!file) {
      return;
    }

    const response = await fetch(`${BACKEND_URL}/db/bulk_add_items`, {
      method: "POST",
      body: await file.text(),
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      }
    });
    const responseJson = await response.json();
    setUploadSuccess(responseJson["success"]);
  }

  useEffect(() => {
    const id = setInterval(updateItems, APP_REFRESH_INTERVAL_MS);
    return () => clearInterval(id);
  }, []);

  useEffect(() => {
    updateItems();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <ItemViewer items={items} showValues={showValues} />
        <label>
          <input type="checkbox" checked={showValues} onChange={() => setShowValues(!showValues)}/>
          Show Values
        </label>
        <button onClick={updateItems}>Refresh</button>
        <label>
          <h1>
            File Upload
          </h1>
          <input type="file" onChange={handleFileChange}/>
          <button onClick={addItems}>Upload</button>
        </label>
        {!uploadSuccess && <div style={{color: "red"}}>Something went wrong with file upload.</div>}
      </header>
    </div>
  );
}

export default App
