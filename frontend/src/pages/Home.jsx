import { Link } from "react-router-dom";
import "./Home.css";

export default function Home() {
  return (
    <section className="home">
      <div className="container">
        <div className="home__eyebrow">CAP 2026 · Engineering Admissions</div>
        <h1 className="home__heading">
          Find which engineering colleges<br />your score can realistically reach.
        </h1>
        <p className="home__lede">
          Built on two years of official State CET Cell cutoff data across every
          CAP round. Choose the exam you've appeared for to begin.
        </p>

        <div className="option-grid">
          <Link to="/mhtcet" className="option-card">
            <div className="option-card__index">01</div>
            <h2>Predict by MHT-CET Score</h2>
            <p>
              Enter your MHT-CET percentile, category, and home university
              to see colleges sorted into Safe, Target, and Reach.
            </p>
            <span className="option-card__cta">Start prediction →</span>
          </Link>

          <Link to="/jee" className="option-card option-card--muted">
            <div className="option-card__index">02</div>
            <h2>Predict by JEE Score</h2>
            <p>
              JEE-based predictions for Maharashtra institutes are being
              built using official JEE Main cutoff data.
            </p>
            <span className="option-card__cta">Coming soon →</span>
          </Link>
        </div>
      </div>
    </section>
  );
}
