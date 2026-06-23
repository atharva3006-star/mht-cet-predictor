import { Link } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="container navbar__inner">
        <Link to="/" className="navbar__brand">
          <span className="navbar__mark">MH</span>
          <span className="navbar__title">
            Engineering College Predictor
            <span className="navbar__subtitle">Maharashtra · CAP 2026</span>
          </span>
        </Link>
        <nav className="navbar__links">
          <Link to="/mhtcet">MHT-CET</Link>
          <Link to="/jee">JEE</Link>
        </nav>
      </div>
    </header>
  );
}
