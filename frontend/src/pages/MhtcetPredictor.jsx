import { useEffect, useState } from "react";
import PredictorForm from "../components/PredictorForm.jsx";
import ResultsView from "../components/ResultsView.jsx";
import { fetchCategories, fetchUniversities, predictMhtcet } from "../api/client.js";
import "./MhtcetPredictor.css";

const EMPTY_FORM = { percentile: "", category: "", home_university: "", branch: "" };

export default function MhtcetPredictor() {
  const [categories, setCategories] = useState([]);
  const [universities, setUniversities] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dropdownsError, setDropdownsError] = useState(null);

  useEffect(() => {
    Promise.all([fetchCategories(), fetchUniversities()])
      .then(([catRes, uniRes]) => {
        setCategories(catRes.categories);
        setUniversities(uniRes.universities);
      })
      .catch(() => {
        setDropdownsError(
          "Couldn't load category/university options. Make sure the backend server is running."
        );
      });
  }, []);

  function handleChange(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults(null);
    try {
      const data = await predictMhtcet(form);
      setResults(data);
    } catch (err) {
      setError(err.message || "Something went wrong while predicting. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="mhtcet-page">
      <div className="container mhtcet-page__inner">
        <div className="mhtcet-page__form-col">
          <div className="home__eyebrow">MHT-CET · State CET Cell Data</div>
          <h1 className="mhtcet-page__heading">Predict your colleges</h1>
          <p className="mhtcet-page__lede">
            Based on the last two years of official CAP round cutoffs.
          </p>

          {dropdownsError && <div className="mhtcet-page__error">{dropdownsError}</div>}

          <PredictorForm
            form={form}
            onChange={handleChange}
            onSubmit={handleSubmit}
            categories={categories}
            universities={universities}
            loading={loading}
          />
        </div>

        <div className="mhtcet-page__results-col">
          {error && <div className="mhtcet-page__error">{error}</div>}

          {!error && !results && !loading && (
            <div className="mhtcet-page__placeholder">
              Fill in your percentile and category, then click Predict colleges
              to see your Safe, Target, and Reach options.
            </div>
          )}

          {loading && <div className="mhtcet-page__placeholder">Searching cutoffs…</div>}

          {results && !loading && <ResultsView data={results} />}
        </div>
      </div>
    </section>
  );
}
