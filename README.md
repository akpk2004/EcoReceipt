- **Planetary Lifecycle Assessment (LCA)**: Calculates cradle-to-gate carbon footprints ($kg\ CO_2e$) based on *Our World in Data* benchmarks.
- **Color-Coded Eco-Grade**: Intuitive score from **A** (Paris 1.5°C compatible) to **F** (Heavy animal agriculture/air-freighted).
- **PlanetPrompts (Smart Swaps)**: Suggests wallet-friendly, plant-forward swaps to cut up to 50% of emissions without guilt.
- **Zero-Waste Recipe Copilot**: Generates delicious dinners using purchased perishable items to eliminate household food waste.
- **Fail-Safe Stage Demo Presets**: Includes built-in simulated high/low-carbon receipts so you can demo smoothly on stage even with poor conference Wi-Fi.
---
## 🚀 Quickstart (Local Run)
1. **Clone & Navigate:**
   ```bash
   cd C:\Users\Anubhav Kaushik\.gemini\antigravity\scratch\ecoreceipt
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Gemini API Key (Optional for presets, required for custom camera uploads):**
   ```bash
   # Windows PowerShell
   $env:GEMINI_API_KEY="your-gemini-api-key"
   ```
4. **Launch the App:**
   ```bash
   streamlit run app.py
   ```
The app will open automatically at `http://localhost:8501`.
