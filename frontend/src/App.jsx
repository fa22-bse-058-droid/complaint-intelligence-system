import { useState } from "react";

const API_URL = "http://127.0.0.1:8000";

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
    <div style={{ maxWidth: 800, margin: "0 auto", padding: 24 }}>
      <h1>Complaint Intelligence System</h1>

      <textarea
        rows={5}
        style={{ width: "100%" }}
        placeholder="Paste a citizen complaint here..."
        value={complaint}
        onChange={(e) => setComplaint(e.target.value)}
      />

      <button onClick={handleAnalyze} disabled={loading || !complaint.trim()}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}

export default App;