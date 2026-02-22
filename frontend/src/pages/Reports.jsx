import { Link } from "react-router-dom";
import backButton from "../assets/images/back-button.png";
import logo from "../assets/images/hacked-logo.png";

function Reports() {
  const reports = JSON.parse(localStorage.getItem("sidequest_reports") || "[]");
  const fallbackScores = [95, 28, 32, 74, 61, 43];
  const rows = Array.from({ length: 3 }, (_, index) => reports[index] || { id: `sample-${index + 1}` });

  return (
    <section className="reports-page" aria-label="My reports">
      <Link className="location-status-back" to="/score-project" aria-label="Back to score project">
        <img src={backButton} alt="Back" />
      </Link>

      <div className="reports-wrap">
        <h1 className="reports-title">My Audit Reports</h1>
        <div className="reports-list">
          {rows.map((report, index) => (
            <article key={report.id || index} className="report-row">
              <p className="report-score">{report.score != null ? `${Math.round(report.score * 100)}%` : `${fallbackScores[index % fallbackScores.length]}%`}</p>
              <p className="report-address">
                {report.address && report.address !== "Location not detected" ? report.address : "Address or Location"}
              </p>
              <Link className="report-view-more" to="/final-score">
                View More
              </Link>
            </article>
          ))}
        </div>

        <div className="reports-actions">
          <button type="button" className="reports-view-all">
            View All
          </button>
          <Link className="reports-return-home" to="/home">
            Return to Home
          </Link>
        </div>
      </div>

      <img className="location-status-logo" src={logo} alt="Hacked logo" />
    </section>
  );
}

export default Reports;
