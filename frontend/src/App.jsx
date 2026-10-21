import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

// Small helper: turns "Critical" into the CSS class "badge badge-critical"
function PriorityBadge({ priority }) {
  const known = ["low", "medium", "high", "critical"];
  const key = priority.toLowerCase();
  const style = known.includes(key) ? key : "other";
  return <span className={`badge badge-${style}`}>{priority}</span>;
}

function App() {
  const [complaint, setComplaint] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleAnalyze() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/api/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ complaint }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Request failed");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Complaint Intelligence System</h1>
        <p>Paste a citizen complaint and get an instant analysis.</p>
      </header>

      <div className="card">
        <textarea
          rows={5}
          placeholder="e.g. There has been a water leak on Main Street for 2 days and the road is flooded"
          value={complaint}
          onChange={(e) => setComplaint(e.target.value)}
        />
        <button onClick={handleAnalyze} disabled={loading || !complaint.trim()}>
          {loading ? "Analyzing..." : "Analyze Complaint"}
        </button>
        {error && <div className="error">Error: {error}</div>}
      </div>

      {result && (
        <>
          <div className="card">
            <h2>Analysis</h2>

            <div className="result-top">
              <span className="badge badge-category">{result.category}</span>
              <PriorityBadge priority={result.priority} />
            </div>

            <div className="info-grid">
              <div>
                <div className="label">Location</div>
                <p className="value">{result.location}</p>
              </div>
              <div>
                <div className="label">Duration</div>
                <p className="value">{result.duration}</p>
              </div>
            </div>

            <div className="section">
              <div className="label">Problem summary</div>
              <p className="value">{result.problem_summary}</p>
            </div>

            <div className="section">
              <div className="label">Recommended action</div>
              <p className="action-box">{result.recommended_action}</p>
            </div>
          </div>

          <div className="card">
            <h2>Similar past complaints</h2>
            {result.similar_complaints.length === 0 ? (
              <p className="empty">No similar past complaints found.</p>
            ) : (
              result.similar_complaints.map((item) => (
                <div className="similar-item" key={item.complaint_id}>
                  <p className="similar-text">{item.complaint_text}</p>
                  <div className="similar-meta">
                    <span>#{item.complaint_id}</span>
                    <span className="badge badge-category">{item.category}</span>
                    <PriorityBadge priority={item.priority} />
                  </div>
                </div>
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default App;