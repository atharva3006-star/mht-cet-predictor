import { Link } from "react-router-dom";
import "./JeeComingSoon.css";

export default function JeeComingSoon() {
  return (
    <section className="jee-soon">
      <div className="container jee-soon__inner">
        <div className="jee-soon__ledger" aria-hidden="true">
          <div className="jee-soon__row jee-soon__row--fill" style={{ animationDelay: "0s" }} />
          <div className="jee-soon__row jee-soon__row--fill" style={{ animationDelay: "0.15s" }} />
          <div className="jee-soon__row jee-soon__row--fill" style={{ animationDelay: "0.3s" }} />
          <div className="jee-soon__row jee-soon__row--fill" style={{ animationDelay: "0.45s" }} />
        </div>

        <div className="home__eyebrow">JEE Main · Maharashtra Institutes</div>
        <h1>We're building this ledger.</h1>
        <p className="jee-soon__lede">
          JEE-based predictions are being compiled from official JEE Main
          cutoff data, the same way our MHT-CET model was. It'll be ready soon.
        </p>

        <Link to="/mhtcet" className="jee-soon__back">
          ← Use the MHT-CET predictor instead
        </Link>
      </div>
    </section>
  );
}
