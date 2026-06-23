import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar.jsx";
import Footer from "./components/Footer.jsx";
import Home from "./pages/Home.jsx";
import MhtcetPredictor from "./pages/MhtcetPredictor.jsx";
import JeeComingSoon from "./pages/JeeComingSoon.jsx";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <main style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/mhtcet" element={<MhtcetPredictor />} />
          <Route path="/jee" element={<JeeComingSoon />} />
        </Routes>
      </main>
      <Footer />
    </BrowserRouter>
  );
}
