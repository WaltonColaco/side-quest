import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import backButton from "../assets/images/back-button.png";
import logo from "../assets/images/hacked-logo.png";
import { fetchMyLocations } from "../services/api";

const INITIAL_LIMIT = 3;

function Reports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    fetchMyLocations()
      .then(setReports)
      .catch((e) => setError(e.response?.data?.detail || "Failed to load reports."))
      .finally(() => setLoading(false));
  }, []);

  const displayed = showAll ? reports : reports.slice(0, INITIAL_LIMIT);

  return (
    <section className="reports-page" aria-label="My reports">
      <Link className="location-status-back" to="/score-project" aria-label="Back to score project">
        <img src={backButton} alt="Back" />
      </Link>

      <div className="reports-wrap">
        <h1 className="reports-title">My Audit Reports</h1>

        {loading ? (
          <p className="reports-loading">Loading reports…</p>
        ) : error ? (
          <p className="reports-error">{error}</p>
        ) : reports.length === 0 ? (
          <p className="reports-empty">No reports yet. Upload a project to get started.</p>
        ) : (
          <>
            <div className="reports-list">
              {displayed.map((report) => (
                <article key={report.id} className="report-row">
                  <p className="report-score">
                    {report.score != null ? `${Math.round(report.score * 100)}%` : "—"}
                  </p>
                  <p className="report-address">
                    {report.address && report.address !== "Location not detected"
                      ? report.address
                      : report.source_doc || "Unknown location"}
                  </p>
                  <Link className="report-view-more" to={`/final-score?id=${report.id}`}>
                    View More
                  </Link>
                </article>
              ))}
            </div>

            <div className="reports-actions">
              {reports.length > INITIAL_LIMIT && (
                <button
                  type="button"
                  className="reports-view-all"
                  onClick={() => setShowAll((prev) => !prev)}
                >
                  {showAll ? "Show Less" : "View All"}
                </button>
              )}
              <Link className="reports-return-home" to="/home">
                Return to Home
              </Link>
            </div>
          </>
        )}
      </div>

      <img className="location-status-logo" src={logo} alt="Hacked logo" />
    </section>
  );
}

export default Reports;
