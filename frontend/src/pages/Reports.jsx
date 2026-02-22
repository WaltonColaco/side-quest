import { Link } from "react-router-dom";
import backButton from "../assets/images/back-button.png";
import logo from "../assets/images/hacked-logo.png";

function Reports() {
  const reports = JSON.parse(localStorage.getItem("sidequest_reports") || "[]");

  return (
    <section className="reports-page" aria-label="My reports">
      <Link className="location-status-back" to="/score-project" aria-label="Back to score project">
        <img src={backButton} alt="Back" />
      </Link>

      <div className="reports-content-card">
        <h1 className="reports-title">My Reports</h1>
        {reports.length === 0 ? (
          <p className="reports-empty">No reports yet. Run an audit from New Audits to populate this page.</p>
        ) : (
          <div className="reports-list">
            {reports.map((report) => (
              <article key={report.id} className="report-item">
                <h2>{report.fileName}</h2>
                <p>{report.address}</p>
                <small>{new Date(report.createdAt).toLocaleString()}</small>
              </article>
            ))}
          </div>
        )}
      </div>

      <img className="location-status-logo" src={logo} alt="Hacked logo" />
    </section>
  );
}

export default Reports;

