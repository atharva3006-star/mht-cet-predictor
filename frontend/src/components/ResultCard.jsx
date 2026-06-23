import "./ResultCard.css";

const TREND_LABEL = {
  rising: "Cutoff rising",
  falling: "Cutoff falling",
  stable: "Cutoff stable",
  new: "No prior-year data",
};

export default function ResultCard({ result }) {
  const bucketClass = `result-card--${result.bucket.toLowerCase()}`;
  return (
    <article className={`result-card ${bucketClass}`}>
      <div className="result-card__main">
        <h3 className="result-card__college">{result.college_name}</h3>
        <p className="result-card__branch">{result.branch_name}</p>
        <div className="result-card__meta">
          <span>{result.seat_pool.replace(/_/g, " → ")}</span>
          
        </div>
      </div>
      <div className="result-card__stats">
        <div className="result-card__cutoff">
          <span className="result-card__cutoff-label">Latest cutoff</span>
          <span className="mono result-card__cutoff-value">
            {result.latest_cutoff_percentile.toFixed(2)}
          </span>
        </div>
        <div className="result-card__trend">{TREND_LABEL[result.trend] || result.trend}</div>
      </div>
    </article>
  );
}
