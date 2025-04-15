import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSummarize = async () => {
    setLoading(true);
    setSummary(""); // Clear previous summary
    try {
      const res = await axios.post("http://localhost:5002/summarize", { text });
      setSummary(res.data.summary);
    } catch (error) {
      setSummary("Error fetching summary.");
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1 className="title">📝 Text Summarization Tool</h1>
      <div className="content">
        <div className="left-pane">
          <textarea
            rows="20"
            placeholder="Paste your text here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button onClick={handleSummarize} disabled={loading || !text.trim()}>
            {loading ? "Summarizing..." : "Summarize"}
          </button>
        </div>
        <div className="right-pane">
          {loading && (
            <div className="loader-container">
              <div className="loader"></div>
              <p>Generating summary...</p>
            </div>
          )}
          {!loading && (
            <textarea
              className="summary-box"
              rows="20"
              value={summary}
              onChange={(e) => setSummary(e.target.value)}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
