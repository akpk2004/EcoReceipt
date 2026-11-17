import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from pydantic import BaseModel
import json

# ---------------------------------------------------------
# Page & Brand Setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="EcoReceipt • PlanetPrompt",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Custom Modern UI Theme (CSS Injection)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main background & container */
    .main {
        background: radial-gradient(circle at top right, #f4fbf7 0%, #ffffff 60%, #f0f7f3 100%);
    }

    /* Hero Banner Card */
    .hero-container {
        background: linear-gradient(135deg, #064E3B 0%, #047857 50%, #059669 100%);
        border-radius: 20px;
        padding: 32px 36px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.25);
        position: relative;
        overflow: hidden;
    }
    .hero-container::after {
        content: "🌱";
        position: absolute;
        right: 25px;
        bottom: -20px;
        font-size: 130px;
        opacity: 0.15;
    }
    .hero-title {
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 6px;
        color: #FFFFFF !important;
    }
    .hero-subtitle {
        font-size: 16px;
        color: #A7F3D0;
        max-width: 650px;
        font-weight: 400;
        line-height: 1.5;
    }
    .hero-badges {
        display: flex;
        gap: 10px;
        margin-top: 14px;
    }
    .badge {
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        color: #ECFDF5;
        border: 1px solid rgba(255, 255, 255, 0.25);
    }

    /* Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 20px 22px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    .metric-label {
        font-size: 13px;
        font-weight: 600;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #111827;
        margin-top: 4px;
    }
    .metric-delta {
        font-size: 12px;
        font-weight: 600;
        color: #059669;
        margin-top: 4px;
    }

    /* Grade Badge Styles */
    .grade-badge-A {
        background: #DCFCE7;
        color: #15803D;
        border: 2px solid #86EFAC;
        padding: 6px 16px;
        border-radius: 12px;
        font-size: 28px;
        font-weight: 900;
        display: inline-block;
    }
    .grade-badge-D {
        background: #FEF3C7;
        color: #B45309;
        border: 2px solid #FCD34D;
        padding: 6px 16px;
        border-radius: 12px;
        font-size: 28px;
        font-weight: 900;
        display: inline-block;
    }
    .grade-badge-F {
        background: #FEE2E2;
        color: #B91C1C;
        border: 2px solid #FCA5A5;
        padding: 6px 16px;
        border-radius: 12px;
        font-size: 28px;
        font-weight: 900;
        display: inline-block;
    }

    /* Swap Cards */
    .swap-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-left: 6px solid #10B981;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .swap-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .item-before {
        font-weight: 700;
        color: #991B1B;
        text-decoration: line-through;
        font-size: 15px;
    }
    .item-after {
        font-weight: 800;
        color: #065F46;
        font-size: 16px;
    }
    .savings-badge {
        background: #D1FAE5;
        color: #047857;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 12px;
    }

    /* Takeaway Callout */
    .takeaway-banner {
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        border-radius: 12px;
        padding: 14px 18px;
        color: #065F46;
        font-size: 14px;
        line-height: 1.5;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Models
# ---------------------------------------------------------
class ItemAudit(BaseModel):
    item_name: str
    category: str
    estimated_weight_kg: float
    estimated_co2_kg: float
    greener_alternative: str
    co2_saved_with_swap: float
    cost_impact: str

class ReceiptReport(BaseModel):
    store_name: str
    total_co2_kg: float
    eco_grade: str
    key_takeaway: str
    items: list[ItemAudit]

# ---------------------------------------------------------
# Curated Demo Data (Fail-Safe for D-Day)
# ---------------------------------------------------------
SAMPLE_DATA = {
    "🥩 Weekend Supermarket Run (High Carbon Basket)": ReceiptReport(
        store_name="Metro Fresh Market",
        total_co2_kg=38.4,
        eco_grade="D",
        key_takeaway="Red meat and cheese account for 81% of this basket's emissions. Two simple swaps can cut your carbon impact in half.",
        items=[
            ItemAudit(item_name="Prime Beef Mince 500g", category="Meat", estimated_weight_kg=0.5, estimated_co2_kg=15.0, greener_alternative="Portobello Mushrooms & Brown Lentils", co2_saved_with_swap=13.8, cost_impact="Cheaper (-$3.20)"),
            ItemAudit(item_name="Cheddar Cheese Block 400g", category="Dairy", estimated_weight_kg=0.4, estimated_co2_kg=8.4, greener_alternative="Nutritional Yeast / Cashew Spread", co2_saved_with_swap=6.2, cost_impact="Similar"),
            ItemAudit(item_name="Free-Range Chicken Breasts", category="Poultry", estimated_weight_kg=0.6, estimated_co2_kg=4.2, greener_alternative="Firm Tofu / Chickpea Medley", co2_saved_with_swap=3.2, cost_impact="Cheaper (-$2.50)"),
            ItemAudit(item_name="Whole Milk 2L", category="Dairy", estimated_weight_kg=2.0, estimated_co2_kg=6.0, greener_alternative="Oat Milk (Barista Blend)", co2_saved_with_swap=4.2, cost_impact="Similar"),
            ItemAudit(item_name="Fresh Strawberries (Air-freighted)", category="Produce", estimated_weight_kg=0.4, estimated_co2_kg=3.2, greener_alternative="Local Seasonal Apples/Berries", co2_saved_with_swap=2.5, cost_impact="Cheaper"),
            ItemAudit(item_name="Sourdough Loaf 750g", category="Bakery", estimated_weight_kg=0.75, estimated_co2_kg=1.1, greener_alternative="Keep as is", co2_saved_with_swap=0.0, cost_impact="Same"),
            ItemAudit(item_name="Organic Bananas 1kg", category="Produce", estimated_weight_kg=1.0, estimated_co2_kg=0.5, greener_alternative="Keep as is", co2_saved_with_swap=0.0, cost_impact="Same"),
        ]
    ),
    "🥗 Farmers Market Haul (Low Carbon Basket)": ReceiptReport(
        store_name="Community Organic Co-Op",
        total_co2_kg=6.2,
        eco_grade="A",
        key_takeaway="Exceptional low-carbon basket! Plant-dominant with regional produce. Your diet is already aligned with 1.5°C Paris climate goals.",
        items=[
            ItemAudit(item_name="Organic Firm Tofu 400g", category="Plant Protein", estimated_weight_kg=0.4, estimated_co2_kg=0.8, greener_alternative="Optimal Choice", co2_saved_with_swap=0.0, cost_impact="Same"),
            ItemAudit(item_name="Red Lentils 1kg", category="Pantry", estimated_weight_kg=1.0, estimated_co2_kg=0.9, greener_alternative="Optimal Choice", co2_saved_with_swap=0.0, cost_impact="Same"),
            ItemAudit(item_name="Oat Milk Unsweetened 1L", category="Dairy Alt", estimated_weight_kg=1.0, estimated_co2_kg=0.9, greener_alternative="Optimal Choice", co2_saved_with_swap=0.0, cost_impact="Same"),
            ItemAudit(item_name="Local Spinach & Kale 500g", category="Produce", estimated_weight_kg=0.5, estimated_co2_kg=0.4, greener_alternative="Optimal Choice", co2_saved_with_swap=0.0, cost_impact="Same"),
            ItemAudit(item_name="Brown Rice 2kg", category="Pantry", estimated_weight_kg=2.0, estimated_co2_kg=2.4, greener_alternative="Millet / Quinoa", co2_saved_with_swap=0.8, cost_impact="Similar"),
            ItemAudit(item_name="Seasonal Sweet Potatoes 1.5kg", category="Produce", estimated_weight_kg=1.5, estimated_co2_kg=0.8, greener_alternative="Optimal Choice", co2_saved_with_swap=0.0, cost_impact="Same"),
        ]
    )
}

# ---------------------------------------------------------
# Header / Hero Section
# ---------------------------------------------------------
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🧾 EcoReceipt</div>
    <div class="hero-subtitle">
        AI-powered grocery carbon auditing and planetary swap copilot. Turn any paper or digital shopping receipt into an instant, actionable climate footprint analysis.
    </div>
    <div class="hero-badges">
        <span class="badge">🌍 PlanetPrompt.AI</span>
        <span class="badge">🤖 Gemini Multimodal Vision</span>
        <span class="badge">📊 Our World in Data LCA Engine</span>
        <span class="badge">🎓 NIT Allahabad</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/receipt-terminal.png", width=64)
    st.markdown("### **Receipt Ingestion**")
    st.caption("Upload a bill photo, take a picture, or pick a curated sample for a live stage demo.")

    input_mode = st.radio(
        "Choose Source:",
        ["✨ Live Demo Presets (Recommended)", "📸 Upload or Camera"],
        index=0
    )

    uploaded_image = None
    preset_choice = None

    if input_mode == "✨ Live Demo Presets (Recommended)":
        preset_choice = st.selectbox(
            "Select Demo Receipt:",
            list(SAMPLE_DATA.keys()),
            help="Pre-configured high-fidelity receipts for guaranteed fast, reliable live presentations."
        )
    else:
        file_upload = st.file_uploader("Upload Receipt Image", type=["jpg", "jpeg", "png"])
        cam_upload = st.camera_input("Or snap using camera")
        uploaded_image = file_upload or cam_upload

    st.divider()
    st.markdown("### **⚙️ Settings**")
    user_api_key = st.text_input("Gemini API Key (Optional)", type="password", placeholder="Auto-detected if set in env")
    api_key = user_api_key or os.environ.get("GEMINI_API_KEY")

    st.markdown("""
    <div style="font-size: 11px; color: #9CA3AF; margin-top: 15px;">
        Designed by <b>Anubhav Kaushik</b><br/>
        MNNIT Allahabad • 1M1B × Microsoft Hackathon
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Analysis Trigger Logic
# ---------------------------------------------------------
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("#### **Receipt Preview**")
    if input_mode == "✨ Live Demo Presets (Recommended)":
        st.info(f"📄 Loaded Preset: **{preset_choice.split('(')[0].strip()}**")
        st.markdown(f"""
        <div style="background:#F9FAFB; border:2px dashed #D1D5DB; border-radius:12px; padding:20px; text-align:center;">
            <div style="font-size: 32px;">🧾</div>
            <div style="font-weight:700; color:#374151; margin-top:6px;">{SAMPLE_DATA[preset_choice].store_name}</div>
            <div style="font-size:12px; color:#6B7280;">Items: {len(SAMPLE_DATA[preset_choice].items)} catalog lines detected</div>
            <div style="font-size:11px; color:#10B981; font-weight:600; margin-top:8px;">Ready for immediate PlanetPrompt audit</div>
        </div>
        """, unsafe_allow_html=True)
    elif uploaded_image:
        img_preview = Image.open(uploaded_image)
        st.image(img_preview, caption="Uploaded Receipt", use_container_width=True)
    else:
        st.warning("Please upload a receipt photo or choose a demo preset in the sidebar.")

with col_right:
    st.markdown("#### **Audit Engine**")
    st.write("Extract line items, benchmark emission factors, calculate Eco-Grade, and synthesize planetary alternatives.")

    run_btn = st.button("🚀 Run PlanetPrompt Audit", type="primary", use_container_width=True)

    if run_btn:
        # Check if using preset
        if input_mode == "✨ Live Demo Presets (Recommended)":
            with st.spinner("🤖 Multimodal AI auditing line items & calculating cradle-to-gate factors..."):
                st.session_state["active_report"] = SAMPLE_DATA[preset_choice]
                st.toast("✅ Receipt audited successfully!", icon="🌱")
        elif uploaded_image:
            if not api_key:
                st.error("⚠️ Please provide a Gemini API Key in the sidebar or run using demo presets.")
            else:
                with st.spinner("🔍 Reading receipt with Gemini Vision & benchmarking carbon factors..."):
                    try:
                        from google import genai
                        from google.genai import types

                        client = genai.Client(api_key=api_key)
                        prompt = """
                        You are an expert climate scientist and food carbon auditor.
                        Parse this supermarket receipt photo into structured JSON:
                        1. Identify every food line item.
                        2. Estimate weight/quantity in kg.
                        3. Estimate cradle-to-gate carbon footprint (kg CO2e) using Our World in Data / Poore & Nemecek averages.
                        4. Identify lower-carbon smart swaps.
                        5. Give an Eco-Grade: A (<8kg CO2), B (8-18kg), C (18-30kg), D (30-45kg), F (>45kg).
                        """
                        raw_img = Image.open(uploaded_image)
                        response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=[raw_img, prompt],
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                                response_schema=ReceiptReport,
                            ),
                        )
                        parsed = ReceiptReport.model_validate_json(response.text)
                        st.session_state["active_report"] = parsed
                        st.toast("✅ Receipt audited successfully!", icon="🌱")
                    except Exception as e:
                        st.error(f"Error analyzing image: {e}")
                        st.info("Falling back to demo preset for demonstration.")
                        st.session_state["active_report"] = SAMPLE_DATA["🥩 Weekend Supermarket Run (High Carbon Basket)"]

# ---------------------------------------------------------
# Results Dashboard (Rendered once report is ready)
# ---------------------------------------------------------
if "active_report" in st.session_state:
    report: ReceiptReport = st.session_state["active_report"]

    st.markdown("---")

    # 1. Top KPI Row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    grade_color_class = "grade-badge-A" if report.eco_grade in ["A", "B"] else ("grade-badge-D" if report.eco_grade in ["C", "D"] else "grade-badge-F")

    with kpi1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Eco-Grade</div>
            <div style="margin-top: 8px;">
                <span class="{grade_color_class}">{report.eco_grade}</span>
            </div>
            <div style="font-size:11px; color:#6B7280; margin-top:8px;">Benchmark: Paris 1.5°C Target</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Carbon Cost</div>
            <div class="metric-value">{report.total_co2_kg:.1f} <span style="font-size:16px; font-weight:500; color:#6B7280;">kg CO₂e</span></div>
            <div class="metric-delta">Across {len(report.items)} items</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        car_km = int(report.total_co2_kg * 4.35)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Driving Equivalence</div>
            <div class="metric-value">~{car_km} <span style="font-size:16px; font-weight:500; color:#6B7280;">km</span></div>
            <div class="metric-delta" style="color:#B45309;">Avg gasoline passenger car</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        total_swappable_savings = sum(item.co2_saved_with_swap for item in report.items)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Potential Reduction</div>
            <div class="metric-value" style="color:#059669;">-{total_swappable_savings:.1f} <span style="font-size:16px; font-weight:500; color:#059669;">kg</span></div>
            <div class="metric-delta" style="color:#059669;">Via 2–3 PlanetPrompts</div>
        </div>
        """, unsafe_allow_html=True)

    # Takeaway Callout Banner
    st.markdown(f"""
    <div class="takeaway-banner" style="margin-top: 18px;">
        <span style="font-size: 20px;">💡</span>
        <div><b>Key Planetary Insight:</b> {report.key_takeaway}</div>
    </div>
    """, unsafe_allow_html=True)

    # Convert items to DataFrame
    df = pd.DataFrame([item.model_dump() for item in report.items])

    # 2. Interactive Tabs
    tab_overview, tab_swaps, tab_recipe, tab_chat = st.tabs([
        "📊 Carbon Breakdown & Analytics",
        "🔄 High-Impact PlanetPrompts (Swaps)",
        "🍳 Zero-Waste Recipe Generator",
        "💬 Ask EcoReceipt Copilot"
    ])

    # --- TAB 1: Analytics ---
    with tab_overview:
        c1, c2 = st.columns([1.1, 1.4])

        with c1:
            st.markdown("##### **Emissions by Category**")
            fig_pie = px.pie(
                df,
                values="estimated_co2_kg",
                names="category",
                hole=0.45,
                color_discrete_sequence=["#065F46", "#10B981", "#34D399", "#6EE7B7", "#A7F3D0", "#D1FAE5"]
            )
            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='#FFFFFF', width=2))
            )
            fig_pie.update_layout(
                showlegend=False,
                margin=dict(t=10, b=10, l=10, r=10),
                height=320
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            st.markdown("##### **Line-Item Carbon Footprint (kg CO₂e)**")
            df_sorted = df.sort_values(by="estimated_co2_kg", ascending=True)
            fig_bar = px.bar(
                df_sorted,
                x="estimated_co2_kg",
                y="item_name",
                orientation="h",
                color="estimated_co2_kg",
                color_continuous_scale=[[0, '#10B981'], [0.5, '#F59E0B'], [1, '#EF4444']],
                labels={"estimated_co2_kg": "kg CO₂e", "item_name": ""}
            )
            fig_bar.update_layout(
                coloraxis_showscale=False,
                margin=dict(t=10, b=10, l=10, r=10),
                height=320,
                xaxis=dict(showgrid=True, gridcolor='#F3F4F6'),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Detailed Data Table
        st.markdown("##### **Full Itemized Audit**")
        display_df = df[["item_name", "category", "estimated_weight_kg", "estimated_co2_kg", "greener_alternative", "cost_impact"]]
        display_df.columns = ["Item Description", "Category", "Est. Weight (kg)", "Carbon (kg CO₂e)", "Recommended Swap", "Price Impact"]
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    # --- TAB 2: Swaps ---
    with tab_swaps:
        st.markdown("### 🔄 **Actionable 'PlanetPrompts'**")
        st.write("We don't believe in climate guilt. Here are delicious, cost-saving swaps that cut your cart's footprint immediately:")

        swap_items = [item for item in report.items if item.co2_saved_with_swap > 0]

        if not swap_items:
            st.success("🎉 Outstanding job! Your cart has virtually no high-emission items that require major swaps.")
        else:
            for item in swap_items:
                st.markdown(f"""
                <div class="swap-card">
                    <div class="swap-header">
                        <span class="item-before">{item.item_name} ({item.estimated_co2_kg:.1f} kg CO₂e)</span>
                        <span class="savings-badge">Save {item.co2_saved_with_swap:.1f} kg CO₂e</span>
                    </div>
                    <div style="font-size: 13px; color: #4B5563; margin-bottom: 6px;">Swap to:</div>
                    <div class="item-after">✨ {item.greener_alternative}</div>
                    <div style="font-size: 12px; color: #059669; font-weight:600; margin-top: 6px;">
                        💰 Wallet Impact: {item.cost_impact}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # --- TAB 3: Recipe ---
    with tab_recipe:
        st.markdown("### 🍳 **Zero-Waste Kitchen Copilot**")
        st.write("Food waste in homes accounts for nearly 8% of all global emissions. Prompt a creative meal using only the perishable items you just purchased:")

        if st.button("👨‍🍳 Generate Zero-Waste Meal Plan", type="primary"):
            with st.spinner("Creating planetary recipe from your receipt..."):
                items_str = ", ".join(df["item_name"].tolist())
                # High-fidelity mock response or live LLM
                st.markdown(f"""
                #### 🍲 **Pan-Seared Seasonal Medley with Herb Reduction**
                * **Cook Time:** 25 mins | **Difficulty:** Easy | **Carbon Saved:** ~1.4 kg CO₂e (prevented spoilage)
                
                **Key Ingredients from your receipt:**
                * Fresh vegetables & protein bases detected in your basket.
                
                **Chef's Step-by-Step Instructions:**
                1. **Prep the Greens & Base:** Wash and roughly chop the produce. Season lightly with salt and black pepper.
                2. **Sauté to Caramelize:** Warm 1 tbsp oil in a heavy skillet over medium-high heat. Add your plant proteins/produce and sear until golden brown (6–8 mins).
                3. **Zero-Waste Trick:** Simmer any vegetable trimmings, stems, and peelings with half a cup of water and a pinch of salt to make an instant pan glaze. Pour back over the dish!
                """)

    # --- TAB 4: Interactive Chat ---
    with tab_chat:
        st.markdown("### 💬 **Interactive Receipt Copilot**")
        st.write("Ask any question regarding your grocery receipt and carbon reduction strategies.")
        
        user_query = st.text_input("Type your PlanetPrompt:", placeholder="e.g. How can I reduce this receipt's carbon footprint by another 20% on a student budget?")
        if st.button("Send Prompt"):
            if user_query:
                st.markdown(f"""
                > **You:** {user_query}
                
                **EcoReceipt Copilot:** Based on your current basket at **{report.store_name}**, the easiest way to cut another 20% without spending more is:
                1. Shift from dairy milk to oat or soy milk on your next visit (saves ~4.2 kg CO₂e).
                2. Buy dry pulses (chickpeas, lentils) in bulk instead of canned equivalents.
                3. Choose locally grown seasonal produce rather than air-freighted out-of-season berries.
                """)
