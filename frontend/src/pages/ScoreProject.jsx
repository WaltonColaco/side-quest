import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchAssessments, fetchComparisons } from "../services/api";

function ScoreProject() {
  const [assessments, setAssessments] = useState([]);
  const [comparisons, setComparisons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [a, c] = await Promise.all([fetchAssessments(), fetchComparisons()]);
        setAssessments(a);
        setComparisons(c);
      } catch (err) {
        console.error(err);
        setError("Could not load scoring data from the backend.");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <section className="hero-card score-shell">
      <p className="eyebrow">Scoring Data</p>
      <h1>Score a project</h1>
      <p className="lead">
        Live data is fetched from the Django backend (assessments and comparisons). Authentication is
        temporarily disabled until the login UI is ready.
      </p>

      {loading && <p>Loading…</p>}
      {error && <p className="error">{error}</p>}

      {!loading && !error && (
        <>
          <div className="table-block">
            <h2>Assessments</h2>
            {assessments.length === 0 ? (
              <p>No assessments yet.</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Project</th>
                    <th>Score</th>
                    <th>Rubric</th>
                    <th>Created</th>
                  </tr>
                </thead>
                <tbody>
                  {assessments.map((a) => (
                    <tr key={a.id}>
                      <td>{a.project_name}</td>
                      <td>{a.overall_score?.toFixed(3)}</td>
                      <td>{a.rubric_version}</td>
                      <td>{a.created_at}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          <div className="table-block">
            <h2>Comparisons</h2>
            {comparisons.length === 0 ? (
              <p>No comparisons yet.</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Mode</th>
                    <th>Strong</th>
                    <th>Partial</th>
                    <th>Missing</th>
                    <th>Score</th>
                    <th>Created</th>
                  </tr>
                </thead>
                <tbody>
                  {comparisons.map((c) => (
                    <tr key={c.id}>
                      <td>{c.id}</td>
                      <td>{c.mode}</td>
                      <td>{c.strong_count}</td>
                      <td>{c.partial_count}</td>
                      <td>{c.missing_count}</td>
                      <td>{c.overall_score?.toFixed(3)}</td>
                      <td>{c.created_at}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </>
      )}

      <Link className="landing-action score-back" to="/">
        back to home
      </Link>
    </section>
  );
}

export default ScoreProject;
