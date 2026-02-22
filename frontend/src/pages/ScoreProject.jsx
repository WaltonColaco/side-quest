import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import logo from "../assets/images/hacked-logo.png";
import { extractFile } from "../services/api";

const ACCEPTED_TYPES = ".pdf,.png,.jpg,.jpeg,.webp,.gif,.bmp,.tiff,.tif,.txt,.md";

function ScoreProject() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [buildingType, setBuildingType] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragging, setDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleFile = (selectedFile) => {
    setFile(selectedFile);
    setError(null);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragging(false);
    const dropped = event.dataTransfer.files[0];
    if (dropped) handleFile(dropped);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);
    try {
      const data = await extractFile(file, buildingType || null);
      // Only treat as "found" when real coordinates were extracted.
      // An address string alone (without coords) still routes to LocationNotFound
      // so the user can confirm/edit it before we geocode and save.
      const found = data?.lat != null && data?.lng != null;
      const reportRecord = {
        id: Date.now(),
        fileName: file?.name || "Untitled",
        createdAt: new Date().toISOString(),
        address: data?.address || "Location not detected",
        found,
      };
      const existing = JSON.parse(localStorage.getItem("sidequest_reports") || "[]");
      localStorage.setItem("sidequest_reports", JSON.stringify([reportRecord, ...existing].slice(0, 30)));
      sessionStorage.setItem("sidequest_pending_filename", file?.name || "Untitled");
      navigate(found ? "/location-found" : "/location-not-found", {
        state: {
          address: data?.address || null,  // null when not found — never send fallback garbage to geocoder
          lat: data?.lat ?? null,
          lng: data?.lng ?? null,
          fileName: file?.name || "Untitled",
        },
      });
    } catch (err) {
      setError(err.response?.data?.error || err.message || "Extraction failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="score-project-screen">
      <img className="score-project-logo" src={logo} alt="Hacked logo" />

      <div className="score-project-card score-shell">
        <p className="eyebrow">Accessibility Extractor</p>
        <h1>Score a project</h1>
        <p className="lead">
          Upload a PDF, image, or text file to extract accessibility features and generate a report.
        </p>

        <form className="extract-form" onSubmit={handleSubmit}>
          <div
            className={`drop-zone${dragging ? " drag-over" : ""}`}
            onDragOver={(event) => {
              event.preventDefault();
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
              onChange={(event) => {
                if (event.target.files[0]) handleFile(event.target.files[0]);
              }}
            />
            {file ? (
              <p>{file.name}</p>
            ) : (
              <p>
                Drop a file here or click to browse
                <br />
                <small>PDF - PNG - JPG - WEBP - TXT - and more</small>
              </p>
            )}
          </div>

          <div className="form-row">
            <label htmlFor="building-type">Building type</label>
            <select id="building-type" value={buildingType} onChange={(event) => setBuildingType(event.target.value)}>
              <option value="">Auto-detect</option>
              <option value="commercial">Commercial</option>
              <option value="housing">Housing</option>
            </select>
          </div>

          <button type="submit" disabled={loading || !file} className="landing-action">
            {loading ? "analysing... this may take a minute" : "Extract Information"}
          </button>
        </form>

        {loading ? (
          <div className="extract-loading">
            <span className="extract-spinner" />
            <p>Analysing file - this usually takes 30-60 seconds...</p>
          </div>
        ) : null}

        {error ? <p className="extract-error">{error}</p> : null}
      </div>
    </section>
  );
}

export default ScoreProject;
