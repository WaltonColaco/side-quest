import { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import { extractFile } from "../services/api";

const ACCEPTED_TYPES = ".pdf,.png,.jpg,.jpeg,.webp,.gif,.bmp,.tiff,.tif,.txt,.md";

function ScoreProject() {
  const [file, setFile] = useState(null);
  const [buildingType, setBuildingType] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [dragging, setDragging] = useState(false);
  const fileInputRef = useRef(null);
  const resultsRef = useRef(null);

  // Scroll to results when they arrive
  useEffect(() => {
    if (result && resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [result]);

  const handleFile = (f) => {
    setFile(f);
    setResult(null);
    setError(null);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      // If no file selected yet, prompt for one instead of silently doing nothing.
      fileInputRef.current?.click();
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await extractFile(file, buildingType || null);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.error || err.message || "Extraction failed.");
    } finally {
      setLoading(false);
    }
  };

  const location = result?.result?.location;
  const extracted = result?.result?.extracted || [];
  const notFound = result?.result?.not_found || [];

  const byCategory = {};
  for (const item of extracted) {
    const cat = item.category || "Other";
    if (!byCategory[cat]) byCategory[cat] = [];
    byCategory[cat].push(item);
  }

  return (
    <section className="hero-card score-shell">
      <p className="eyebrow">Accessibility Extractor</p>
      <h1>Score a project</h1>
      <p className="lead">
        Upload a PDF, image, or text file to extract accessibility features and generate a report.
      </p>

      <form className="extract-form" onSubmit={handleSubmit}>
        <div
          className={`drop-zone${dragging ? " drag-over" : ""}`}
          onDragOver={(e) => {
            e.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept={ACCEPTED_TYPES}
            style={{ display: "none" }}
            onChange={(e) => {
              if (e.target.files[0]) handleFile(e.target.files[0]);
            }}
          />
          {file ? (
            <p>{file.name}</p>
          ) : (
            <p>
              Drop a file here or click to browse
              <br />
              <small>PDF · PNG · JPG · WEBP · TXT · and more</small>
            </p>
          )}
        </div>

        <div className="form-row">
          <label>Building type</label>
          <select value={buildingType} onChange={(e) => setBuildingType(e.target.value)}>
            <option value="">Auto-detect</option>
            <option value="commercial">Commercial</option>
            <option value="housing">Housing</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="landing-action"
        >
          {loading ? "analysing… this may take a minute" : file ? "extract features" : "choose a file to extract"}
        </button>
      </form>

      {loading && (
        <div className="extract-loading">
          <span className="extract-spinner" />
          <p>Analysing file — this usually takes 30–60 seconds…</p>
        </div>
      )}

      {error && <p className="extract-error">{error}</p>}

      {result && (
        <div className="extract-results" ref={resultsRef}>
          {location && (location.address || location.raw || location.coordinates?.lat != null) && (
            <div className="result-section">
              <h2>Location</h2>
              {(location.address || location.raw) && (
                <p>
                  <strong>{location.address || location.raw}</strong>
                </p>
              )}
              {location.coordinates?.lat != null && (
                <p style={{ color: "var(--stone)", fontSize: "0.9rem" }}>
                  {location.coordinates.lat}, {location.coordinates.lon}
                </p>
              )}
            </div>
          )}

          {Object.keys(byCategory).length > 0 && (
            <div className="result-section">
              <h2>Found Requirements ({extracted.length})</h2>
              {Object.entries(byCategory).map(([cat, items]) => (
                <div key={cat}>
                  <h3>{cat}</h3>
                  <ul>
                    {items.map((item, i) => (
                      <li key={i}>
                        <strong>{item.requirement}</strong> —{" "}
                        {Math.round((item.confidence ?? 0) * 100)}% confidence
                        {item.description && (
                          <>
                            <br />
                            <small>{item.description}</small>
                          </>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          )}

          {notFound.length > 0 && (
            <div className="result-section">
              <h2>Not Found ({notFound.length})</h2>
              <ul className="not-found-list">
                {notFound.map((req, i) => (
                  <li key={i}>{req}</li>
                ))}
              </ul>
            </div>
          )}

          {result.markdown && (
            <div className="result-section">
              <h2>Full Report</h2>
              <pre className="markdown-raw">{result.markdown}</pre>
            </div>
          )}
        </div>
      )}

      <Link className="landing-action score-back" to="/">
        back to home
      </Link>
    </section>
  );
}

export default ScoreProject;
