import "./PredictorForm.css";

export default function PredictorForm({
  form,
  onChange,
  onSubmit,
  categories,
  universities,
  loading,
}) {
  return (
    <form className="predictor-form" onSubmit={onSubmit}>
      <div className="predictor-form__row">
        <label htmlFor="percentile">
          MHT-CET Percentile <span className="required">*</span>
        </label>
        <input
          id="percentile"
          type="number"
          min="0"
          max="100"
          step="0.01"
          required
          placeholder="e.g. 92.45"
          value={form.percentile}
          onChange={(e) => onChange("percentile", e.target.value)}
        />
      </div>

      <div className="predictor-form__row">
        <label htmlFor="category">
          Category <span className="required">*</span>
        </label>
        <select
          id="category"
          required
          value={form.category}
          onChange={(e) => onChange("category", e.target.value)}
        >
          <option value="" disabled>Select your category</option>
          {categories.map((c) => (
            <option key={c.code} value={c.code}>
              {c.label} ({c.code})
            </option>
          ))}
        </select>
      </div>

      <div className="predictor-form__row">
        <label htmlFor="home_university">Home University</label>
        <select
          id="home_university"
          value={form.home_university}
          onChange={(e) => onChange("home_university", e.target.value)}
        >
          <option value="">Not sure / skip</option>
          {universities.map((u) => (
            <option key={u} value={u}>{u}</option>
          ))}
        </select>
        <p className="predictor-form__hint">
          Affects Home-University quota seats. Leave blank to see State-level seats only.
        </p>
      </div>

      <div className="predictor-form__row">
        <label htmlFor="branch">Preferred Branch (optional)</label>
        <input
          id="branch"
          type="text"
          placeholder="e.g. Computer, Mechanical, AI"
          value={form.branch}
          onChange={(e) => onChange("branch", e.target.value)}
        />
      </div>

      <button type="submit" className="predictor-form__submit" disabled={loading}>
        {loading ? "Searching..." : "Predict colleges"}
      </button>
    </form>
  );
}
