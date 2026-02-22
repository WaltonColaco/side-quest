import { useEffect, useRef, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import backButton from "../assets/images/back-button.png";
import logo from "../assets/images/hacked-logo.png";
import checkIcon from "../assets/images/tick-mark.png";
import crossIcon from "../assets/images/cross-mark.png";
import { fetchLocationDetail } from "../services/api";

const MAX_BAR_HEIGHT = 300; // px — tallest bar will reach this height
const POLL_INTERVAL_MS = 8000; // re-fetch every 8 s while score is null
const MAX_POLLS = 15; // give up after ~2 minutes

function FinalScore() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const locationId = searchParams.get("id");

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const pollCount = useRef(0);
  const timerRef = useRef(null);

  useEffect(() => {
    const load = async () => {
      try {
        const result = await fetchLocationDetail(locationId);
        setData(result);
        if (result.score == null && pollCount.current < MAX_POLLS) {
          pollCount.current += 1;
          timerRef.current = setTimeout(load, POLL_INTERVAL_MS);
        }
      } catch (e) {
        setError(e.response?.data?.detail || "Failed to load report.");
      } finally {
        setLoading(false);
      }
    };

    load();
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, [locationId]);

  const scorePct = data?.score != null ? Math.round(data.score * 100) : null;
  const address = data?.address || data?.source || "Address not available";
  const breakdown = data?.breakdown || [];
  const passes = data?.passes || [];
  const fails = data?.fails || [];

  const maxTotal = Math.max(...breakdown.map((b) => b.found + b.missing), 1);
  const barHeight = (count) =>
    `${Math.round((count / maxTotal) * MAX_BAR_HEIGHT)}px`;

  return (
    <section
      className="final-score-page"
      aria-label="Final score page"
      style={{
        height: "100vh",
        minHeight: "100vh",
        overflowY: "auto",
        overflowX: "hidden",
      }}
    >
      <button
        className="location-status-back"
        type="button"
        onClick={() => navigate(-1)}
        aria-label="Back"
        style={{ background: "none", border: "none", cursor: "pointer", padding: 0 }}
      >
        <img src={backButton} alt="Back" />
      </button>

      <div className="final-score-wrap">
        {/* LEFT — bar chart */}
        <div className="final-score-left">
          <div className="final-score-graph-block">
          <div className="final-score-legend">
            <div className="final-score-legend-item">
              <span className="legend-box legend-missing" />
              <span>Criteria Not Found</span>
            </div>
            <div className="final-score-legend-item">
              <span className="legend-box legend-found" />
              <span>Criteria Found</span>
            </div>
          </div>

          <div className="final-score-chart">
            {loading ? (
              <p style={{ color: "#989896", fontSize: 16, alignSelf: "center" }}>
                Loading…
              </p>
            ) : error ? (
              <p style={{ color: "#c00", fontSize: 16, alignSelf: "center" }}>
                {error}
              </p>
            ) : breakdown.length === 0 ? (
              <p style={{ color: "#989896", fontSize: 16, alignSelf: "center" }}>
                Score computing — check back shortly.
              </p>
            ) : (
              breakdown.map((bar, index) => (
                <div key={index} className="final-score-bar" title={bar.name}>
                  <div
                    className="bar-found"
                    style={{ height: barHeight(bar.found) }}
                  />
                  <div
                    className="bar-missing"
                    style={{ height: barHeight(bar.missing) }}
                  />
                </div>
              ))
            )}
          </div>

          {breakdown.length > 0 && (
            <div
              style={{
                display: "flex",
                gap: "var(--bar-gap)",
                paddingLeft: "var(--chart-inset)",
                marginTop: "6px",
              }}
            >
              {breakdown.map((bar, i) => (
                <div
                  key={i}
                  style={{
                    width: "var(--bar-width)",
                    fontSize: "12px",
                    textAlign: "center",
                    color: "#31493c",
                    fontWeight: 600,
                    lineHeight: 1.2,
                  }}
                >
                  {bar.name}
                </div>
              ))}
            </div>
          )}

          <div className="final-score-base" />
          </div>
        </div>

        {/* RIGHT — score + address + checklist */}
        <div className="final-score-right">
          <div className="final-score-percent-row">
            {scorePct !== null ? (
              <h1>{scorePct}%</h1>
            ) : (
              <h1 style={{ fontSize: "42px", color: "#989896" }}>
                {loading ? "Loading…" : "Computing…"}
              </h1>
            )}
          </div>

          <h2>{address}</h2>

          <div className="final-score-reasons">
            {passes.slice(0, 6).map((item, idx) => (
              <div key={`p-${idx}`} className="reason-row">
                <img src={checkIcon} alt="Criteria met" />
                <span>{item.label}</span>
              </div>
            ))}
            {fails.slice(0, 3).map((item, idx) => (
              <div key={`f-${idx}`} className="reason-row">
                <img src={crossIcon} alt="Criteria not met" />
                <span>{item.label}</span>
              </div>
            ))}
            {!loading && passes.length === 0 && fails.length === 0 && (
              <p style={{ color: "#989896", fontSize: 16 }}>
                Detailed results will appear once scoring completes (~60 s).
              </p>
            )}
          </div>

          <div className="final-score-actions">
            <Link className="final-score-home" to="/home">
              Return to Home
            </Link>
            {locationId ? (
              <a
                className="final-score-download"
                href={`/api/location/download/?id=${locationId}`}
                download
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                Download PDF
              </a>
            ) : (
              <Link
                className="final-score-download"
                to="/map-heat"
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                View on Map
              </Link>
            )}
          </div>
        </div>
      </div>

      <img className="location-status-logo" src={logo} alt="Hacked logo" />
    </section>
  );
}

export default FinalScore;
