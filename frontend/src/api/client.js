const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

async function handleResponse(res) {
  if (!res.ok) {
    let detail = "Something went wrong. Please try again.";
    try {
      const body = await res.json();
      detail = body.detail || body.error || detail;
    } catch {
      /* ignore parse errors */
    }
    throw new Error(detail);
  }
  return res.json();
}

export async function fetchCategories() {
  const res = await fetch(`${API_BASE}/predict/mhtcet/categories`);
  return handleResponse(res);
}

export async function fetchUniversities() {
  const res = await fetch(`${API_BASE}/predict/mhtcet/universities`);
  return handleResponse(res);
}

export async function predictMhtcet({ percentile, category, home_university, branch, region }) {
  const res = await fetch(`${API_BASE}/predict/mhtcet`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      percentile: Number(percentile),
      category,
      home_university: home_university || null,
      branch: branch || null,
      region: region || null,
    }),
  });
  return handleResponse(res);
}
