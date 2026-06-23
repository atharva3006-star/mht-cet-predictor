import { useState } from "react";
import ResultCard from "./ResultCard.jsx";
import "./ResultsView.css";

const BUCKETS = [
  { key: "safe", label: "Safe", hint: "Comfortably above last year's cutoff" },
  { key: "target", label: "Target", hint: "Close to last year's cutoff — could go either way" },
  { key: "reach", label: "Reach", hint: "A stretch, but not unrealistic" },
];

export default function ResultsView({ data }) {
  const [openReach, setOpenReach] = useState(false);

  if (!data || data.total_results === 0) {
    return (
      <div className="results-empty">
        <p>
          No colleges matched these filters within a realistic range of your
          percentile. Try widening the branch filter or removing it.
        </p>
      </div>
    );
  }

  return (
    <div className="results-view">
      <div className="results-view__summary mono">{data.total_results} results found</div>

      {BUCKETS.map(({ key, label, hint }) => {
        const list = data[key];
        if (!list || list.length === 0) return null;

        const isReach = key === "reach";
        const collapsed = isReach && !openReach;

        return (
          <section key={key} className="bucket-section">
            <div
              className={`bucket-section__header ${isReach ? "bucket-section__header--toggle" : ""}`}
              onClick={isReach ? () => setOpenReach((v) => !v) : undefined}
              role={isReach ? "button" : undefined}
              tabIndex={isReach ? 0 : undefined}
            >
              <h2 className={`bucket-section__title bucket-section__title--${key}`}>
                {label} <span className="mono bucket-section__count">({list.length})</span>
              </h2>
              <p className="bucket-section__hint">{hint}</p>
              {isReach && (
                <span className="bucket-section__caret">{collapsed ? "Show ▾" : "Hide ▴"}</span>
              )}
            </div>

            {!collapsed && (
              <div className="bucket-section__list">
                {list.map((r) => (
                  <ResultCard key={`${r.college_code}-${r.branch_code}-${r.seat_pool}`} result={r} />
                ))}
              </div>
            )}
          </section>
        );
      })}
    </div>
  );
}
