import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="GAM Assurance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Dropify-inspired clean UI
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

:root {
    --green:      #085424;
    --green-light:#0d7a35;
    --green-pale: #e8f5ec;
    --lime:       #bbca14;
    --lime-pale:  #f5f7d6;
    --bg:         #F5F7FA;
    --surface:    #FFFFFF;
    --surface2:   #F0F2F5;
    --border:     #E8ECF0;
    --border2:    #D4DAE3;
    --red:        #F05252;
    --red-pale:   #FEF2F2;
    --blue:       #3B82F6;
    --blue-pale:  #EFF6FF;
    --amber:      #F59E0B;
    --amber-pale: #FFFBEB;
    --text:       #343C6A;
    --text2:      #6B7280;
    --text3:      #9CA3AF;
    --font:       'Plus Jakarta Sans', sans-serif;
    --radius:     16px;
    --radius-sm:  10px;
    --shadow:     0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    --shadow-md:  0 4px 16px rgba(0,0,0,0.08);
}

/* ── GLOBAL ── */
html, body, [class*="css"], .main {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font) !important;
}
.main .block-container {
    padding: 1.5rem 2rem 2rem !important;
    max-width: 100% !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}
[data-testid="stSidebar"] .stSlider > label,
[data-testid="stSidebar"] .stSelectbox > label,
[data-testid="stSidebar"] .stMultiselect > label,
[data-testid="stSidebar"] .stNumberInput > label {
    color: var(--text2) !important;
    font-size: 0.75rem !important;
    font-family: var(--font) !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"] > div {
    border-radius: var(--radius-sm) !important;
    border-color: var(--border2) !important;
    background: var(--surface2) !important;
}

/* ── LOGO AREA ── */
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 1.4rem 1.2rem 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}
.sidebar-logo-icon {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, var(--green), var(--green-light));
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(8,84,36,0.25);
}
.sidebar-logo-text {
    font-weight: 700;
    font-size: 1.05rem;
    color: var(--text);
    line-height: 1.1;
}
.sidebar-logo-sub {
    font-size: 0.68rem;
    color: var(--text3);
    font-weight: 400;
}

/* ── SIDEBAR SECTIONS ── */
.sidebar-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1rem 0;
}
.sidebar-section-title {
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--text3);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0 0 0.5rem 0;
}

/* ── PAGE HEADER ── */
.page-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    gap: 1rem;
}
.page-header-left h1 {
    font-size: 1.5rem !important;
    font-weight: 800 !important;
    color: var(--text) !important;
    margin: 0 0 0.25rem !important;
    letter-spacing: -0.02em;
    line-height: 1.2;
}
.page-header-left .subtitle {
    font-size: 0.82rem;
    color: var(--text2);
    font-weight: 400;
}
.badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 0.6rem;
}
.badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: var(--surface);
    border: 1px solid var(--border2);
    color: var(--text2);
    font-size: 0.67rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.03em;
}

/* ── KPI CARDS ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.1rem 1.2rem 1rem;
    box-shadow: var(--shadow);
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.2s, transform 0.2s;
}
.kpi-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}
.kpi-card-icon {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
    margin-bottom: 0.8rem;
}
.kpi-card.blue  .kpi-card-icon { background: var(--blue-pale);  }
.kpi-card.green .kpi-card-icon { background: var(--green-pale); }
.kpi-card.red   .kpi-card-icon { background: var(--red-pale);   }
.kpi-card.amber .kpi-card-icon { background: var(--amber-pale); }
.kpi-card.lime  .kpi-card-icon { background: var(--lime-pale);  }
.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text2);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.25rem;
}
.kpi-value {
    font-size: 1.75rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1;
    letter-spacing: -0.02em;
}
.kpi-sub {
    font-size: 0.72rem;
    color: var(--text3);
    margin-top: 0.3rem;
    font-weight: 400;
}
.kpi-card.blue  .kpi-value { color: var(--blue);  }
.kpi-card.green .kpi-value { color: var(--green); }
.kpi-card.red   .kpi-value { color: var(--red);   }
.kpi-card.amber .kpi-value { color: var(--amber); }
.kpi-card.lime  .kpi-value { color: #8a9a00;      }

/* ── TABS ── */
[data-testid="stTabs"] [role="tablist"] {
    gap: 0 !important;
    border-bottom: 2px solid var(--border) !important;
    background: transparent !important;
    padding: 0 !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: var(--font) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    color: var(--text2) !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 10px 20px !important;
    border-radius: 0 !important;
    letter-spacing: 0.02em;
    margin-bottom: -2px !important;
    transition: color 0.15s;
}
[data-testid="stTabs"] [role="tab"]:hover {
    color: var(--text) !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: var(--green) !important;
    border-bottom: 2px solid var(--green) !important;
    background: transparent !important;
}

/* ── CONTENT CARDS ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.3rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
}
.card-title {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 6px;
}
.card-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
    margin-left: 8px;
}

/* ── PROGRESS BARS ── */
.prog-wrap { margin: 5px 0 8px; }
.prog-label {
    font-size: 0.75rem;
    color: var(--text2);
    margin-bottom: 4px;
    display: flex;
    justify-content: space-between;
    font-weight: 500;
}
.prog-bar-bg {
    background: var(--surface2);
    border-radius: 6px;
    height: 7px;
    overflow: hidden;
}
.prog-bar-fill {
    height: 100%;
    border-radius: 6px;
    transition: width 0.5s cubic-bezier(.4,0,.2,1);
}

/* ── INSIGHT BOX ── */
.insight-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--green);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    padding: 1rem 1.2rem;
    font-size: 0.86rem;
    color: var(--text);
    line-height: 1.65;
    box-shadow: var(--shadow);
}
.insight-title {
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--green);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.4rem;
}

/* ── DATA TABLE ── */
[data-testid="stDataFrame"] {
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow) !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }

/* ── MINI KPI (inside tabs) ── */
.mini-kpi {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 0.75rem 1rem;
    margin-bottom: 8px;
    box-shadow: var(--shadow);
}
.mini-kpi-label { font-size: 0.68rem; color: var(--text3); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px; }
.mini-kpi-value { font-size: 1.2rem; font-weight: 800; color: var(--text); letter-spacing: -0.01em; }
.mini-kpi-sub   { font-size: 0.68rem; color: var(--text3); margin-top: 1px; }

/* ── STATUS PILL ── */
.pill {
    display: inline-block;
    padding: 2px 9px;
    border-radius: 20px;
    font-size: 0.66rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}
.pill-green  { background: var(--green-pale); color: var(--green); }
.pill-amber  { background: var(--amber-pale); color: #b45309; }
.pill-red    { background: var(--red-pale);   color: var(--red); }

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# WILAYA COORDINATES
# ─────────────────────────────────────────────
WILAYA_COORDS = {
    "SETIF":             (36.190,  5.408),
    "ORAN":              (35.697, -0.633),
    "TIZI OUZOU":        (36.712,  4.046),
    "TLEMCEN":           (34.878, -1.315),
    "DJELFA":            (34.671,  3.263),
    "TIARET":            (35.370,  1.317),
    "CONSTANTINE":       (36.365,  6.615),
    "CHLEF":             (36.165,  1.330),
    "BATNA":             (35.556,  6.174),
    "BLIDA":             (36.470,  2.830),
    "MASCARA":           (35.396,  0.140),
    "MEDEA":             (36.264,  2.751),
    "BOUIRA":            (36.374,  3.901),
    "MOSTAGANEM":        (35.931,  0.089),
    "SKIKDA":            (36.876,  6.908),
    "OUARGLA":           (31.952,  5.325),
    "MILA":              (36.450,  6.264),
    "JIJEL":             (36.819,  5.766),
    "BEJAIA":            (36.756,  5.084),
    "RELIZANE":          (35.738,  0.556),
    "TEBESSA":           (35.405,  8.119),
    "AIN DEFLA":         (36.264,  1.967),
    "BOUMERDES":         (36.761,  3.478),
    "TIPAZA":            (36.589,  2.449),
    "ANNABA":            (36.900,  7.765),
    "GHARDAIA":          (32.490,  3.674),
    "BISKRA":            (34.850,  5.728),
    "OUM EL BOUAGHI":    (35.877,  7.113),
    "SIDI BEL ABBES":    (35.190, -0.630),
    "AIN TEMOUCHENT":    (35.298, -1.141),
    "SAIDA":             (34.831,  0.152),
    "SOUK AHRAS":        (36.285,  7.951),
    "GUELMA":            (36.462,  7.428),
    "EL OUED":           (33.368,  6.864),
    "EL TARF":           (36.767,  8.313),
    "KHENCHELA":         (35.435,  7.143),
    "ADRAR":             (27.874, -0.294),
    "LAGHOUAT":          (33.799,  2.864),
    "BECHAR":            (31.617, -2.216),
    "TISSEMSILT":        (35.607,  1.811),
    "EL BAYADH":         (33.682,  1.017),
    "TAMANRASSET":       (22.785,  5.523),
    "NAAMA":             (33.267, -0.313),
    "TINDOUF":           (27.674, -8.149),
    "ILLIZI":            (26.507,  8.483),
    "ALGER":             (36.737,  3.086),
    "M'SILA":            (35.706,  4.543),
    "BORDJ BOU ARRERIDJ":(36.073,  4.763),
}

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def generate_data():
    df = pd.read_csv("data/zones.csv")
    df["wilaya"] = df["wilaya"].str.strip().str.upper()

    ag = pd.read_csv("data/agencies.csv")
    ag["wilaya"] = ag["wilaya"].str.strip().str.upper()

    df = df.merge(
        ag[["wilaya", "Region", "CAAT", "CAAR", "SAA",
            "TRUST", "CASH", "CIAR", "AMANA", "Competitor Count"]],
        on="wilaya", how="left"
    )

    df = df.rename(columns={
        "Population":           "population",
        "GAM_Agencies":         "existing_agencies",
        "Final_Priority_Score": "score_raw",
        "D":                    "demand",
        "G":                    "gam_coverage",
        "C":                    "comp_inv",
        "Competitor Count":     "competition",
        "Region":               "region",
    })

    df["score"]        = (df["score_raw"] * 100).round(1)
    df["income_index"] = df["demand"].round(3)
    df["density"]      = (df["population"] / 1000).round(1)
    df["industrial_zones"] = 0
    df["zone"]         = df["wilaya"]

    df["lat"] = df["wilaya"].map(lambda w: WILAYA_COORDS.get(w, (None, None))[0])
    df["lon"] = df["wilaya"].map(lambda w: WILAYA_COORDS.get(w, (None, None))[1])
    df = df.dropna(subset=["lat", "lon"])

    companies = ["CAAT", "CAAR", "SAA", "TRUST", "CASH", "CIAR", "AMANA"]
    np.random.seed(42)
    agency_rows = []
    for _, row in df.iterrows():
        for company in companies:
            count = int(row[company]) if pd.notna(row.get(company)) else 0
            for _ in range(count):
                agency_rows.append({
                    "zone":    row["wilaya"],
                    "wilaya":  row["wilaya"],
                    "region":  row.get("region", ""),
                    "lat":     row["lat"] + np.random.uniform(-0.15, 0.15),
                    "lon":     row["lon"] + np.random.uniform(-0.15, 0.15),
                    "company": company,
                })
    agencies_df = pd.DataFrame(agency_rows)
    return df, agencies_df

df_base, agencies_df = generate_data()

# ─────────────────────────────────────────────
# SCORING FUNCTION
# ─────────────────────────────────────────────
def compute_scores(df, w_demo, w_eco, w_ind, w_comp, rule_pop=15000):
    df = df.copy()
    demand   = df["demand"].clip(0, 1)
    eco      = df["income_index"].clip(0, 1)
    gam_cov  = df["gam_coverage"].clip(0, 1)
    other_ag = df["comp_inv"].clip(0, 1)

    total = w_demo + w_eco + w_ind + w_comp
    if total == 0:
        total = 1

    df["score"] = (
        demand   * (w_demo / total) +
        eco      * (w_eco  / total) +
        gam_cov  * (w_ind  / total) +
        other_ag * (w_comp / total)
    ) * 100

    base_required  = df["population"] / rule_pop
    density_factor = np.log1p(df["population"]) / np.log1p(df["population"].max())
    df["required_agencies"] = (
        base_required * (0.65 + 0.35 * density_factor)
    ).apply(lambda x: max(1, round(x)))

    df["gap"]      = df["required_agencies"] - df["existing_agencies"]
    df["coverage"] = (df["existing_agencies"] / df["required_agencies"]).clip(0, 2).round(2)
    df["rank"]     = df["score"].rank(ascending=False).astype(int)
    return df

# ─────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans, sans-serif", color="#343C6A", size=11),
    xaxis=dict(gridcolor="#E8ECF0", linecolor="#E8ECF0", zerolinecolor="#E8ECF0"),
    yaxis=dict(gridcolor="#E8ECF0", linecolor="#E8ECF0", zerolinecolor="#E8ECF0"),
    legend=dict(bgcolor="rgba(255,255,255,0.9)", bordercolor="#E8ECF0", font=dict(size=11)),
    coloraxis_colorbar=dict(tickfont=dict(color="#343C6A")),
   
)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
      <div class="sidebar-logo-icon">
  <img src="data/gam.png" style="width:42px;height:42px;object-fit:contain;">
</div>
        <div class="sidebar-logo-text">GAM Assurance</div>
        <div class="sidebar-logo-sub">Location Intelligence</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sidebar-section-title'>Filters</div>", unsafe_allow_html=True)
    wilayas_list = sorted(df_base["wilaya"].unique().tolist())
    sel_wilaya   = st.multiselect("Wilaya", wilayas_list, default=wilayas_list)

    regions_available = sorted(df_base[df_base["wilaya"].isin(sel_wilaya)]["region"].dropna().unique().tolist())
    sel_region = st.multiselect("Region (optional)", regions_available, default=[])

    pop_min, pop_max = int(df_base["population"].min()), int(df_base["population"].max())
    sel_pop = st.slider("Population range", pop_min, pop_max, (pop_min, pop_max),
                        step=10000, format="%d")

    score_thresh = st.slider("Min score threshold", 0, 100, 0)

    comp_max_val = int(df_base["competition"].max())
    comp_max = st.slider("Max competitor count", 0, comp_max_val, comp_max_val)

    st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-section-title'>⚖️ Scoring Weights</div>", unsafe_allow_html=True)
    w_demo = st.slider("D — Demand",        0.0, 1.0, 0.30, 0.05)
    w_eco  = st.slider("Eco / Income",      0.0, 1.0, 0.25, 0.05)
    w_ind  = st.slider("G — GAM Coverage",  0.0, 1.0, 0.20, 0.05)
    w_comp = st.slider("C — Competition",   0.0, 1.0, 0.25, 0.05)

    st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-section-title'>📐 Rule Parameters</div>", unsafe_allow_html=True)
    rule_pop = st.number_input("1 agency per N inhabitants", min_value=5000,
                               max_value=50000, value=15000, step=1000)

# ─────────────────────────────────────────────
# COMPUTE FILTERED DATA
# ─────────────────────────────────────────────
df = compute_scores(df_base.copy(), w_demo, w_eco, w_ind, w_comp, rule_pop)

mask = (
    df["wilaya"].isin(sel_wilaya) &
    df["population"].between(sel_pop[0], sel_pop[1]) &
    (df["score"] >= score_thresh) &
    (df["competition"] <= comp_max)
)
if sel_region:
    mask &= df["region"].isin(sel_region)

df_f = df[mask].copy()

# ─────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <div class="page-header-left">
    <h1>Insurance Agency Optimizer</h1>
    <div class="subtitle">Spatial scoring &amp; gap analysis · Algeria Insurance Market</div>
    <div class="badge-row">
      <span class="badge">🌍 AI / GIS</span>
      <span class="badge">📊 Spatial Analysis</span>
      <span class="badge">🎯 Multi-Criteria Scoring</span>
      <span class="badge">📍 Coverage Optimization</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
total_gap = df_f["gap"].clip(0).sum()
avg_score = df_f["score"].mean() if len(df_f) else 0
avg_cov   = df_f["coverage"].mean() if len(df_f) else 0
n_opport  = (df_f["gap"] > 0).sum()

k1, k2, k3, k4, k5 = st.columns(5)

for col, icon, label, value, sub, cls in [
    (k1, "🗺️",  "Wilayas",         len(df_f),             "after filters",       "blue"),
    (k2, "⭐",  "Avg. Score",       f"{avg_score:.1f}",    "out of 100",          "amber"),
    (k3, "📉",  "GAM Gap",          int(total_gap),         "agencies needed",     "red"),
    (k4, "🎯",  "Opportunities",    int(n_opport),          "gap > 0 wilayas",     "green"),
    (k5, "📊",  "GAM Coverage",     f"{avg_cov*100:.0f}%",  "existing / required", "lime"),
]:
    with col:
        st.markdown(f"""
        <div class="kpi-card {cls}">
          <div class="kpi-card-icon">{icon}</div>
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️  Geographic Analysis",
    "📊  Scoring & Ranking",
    "📉  Gap & Coverage",
    "🔍  Wilaya Detail",
    "🔄  Scenario Simulation",
])

# ══════════════════════════════════════════════
# TAB 1 — GEOGRAPHIC ANALYSIS
# ══════════════════════════════════════════════
with tab1:
    col_map, col_ctrl = st.columns([3, 1])

    with col_ctrl:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Map Options</div>", unsafe_allow_html=True)
        map_layer     = st.radio("Overlay", ["Score", "Gap", "Coverage"], index=0)
        show_agencies = st.checkbox("Show competitors", value=True)
        show_gam      = st.checkbox("Show GAM agencies", value=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_map:
        st.markdown("<div class='card-title'>Attractiveness Map — Wilayas scored by opportunity index</div>", unsafe_allow_html=True)
        if len(df_f) == 0:
            st.warning("No zones match current filters.")
        else:
            if map_layer == "Score":
                color_col   = "score"
                color_scale = [[0, "#56d364"], [0.5, "#F59E0B"], [1, "#F05252"]]
                range_c     = [0, 100]
                map_label   = "Score"
            elif map_layer == "Gap":
                color_col   = "gap"
                color_scale = [[0, "#56d364"], [0.5, "#F59E0B"], [1, "#F05252"]]
                range_c     = [df_f["gap"].min(), df_f["gap"].max()]
                map_label   = "Gap"
            else:
                color_col   = "coverage"
                color_scale = [[0, "#F05252"], [0.5, "#F59E0B"], [1, "#085424"]]
                range_c     = [0, 2]
                map_label   = "Coverage"

            fig_map = px.scatter_mapbox(
                df_f,
                lat="lat", lon="lon",
                color=color_col,
                size="population",
                size_max=28,
                hover_name="wilaya",
                hover_data={
                    "region": True,
                    "score":  ":.1f",
                    "population": ":,",
                    "gap": True,
                    "coverage": ":.2f",
                    "competition": True,
                    "existing_agencies": True,
                    "lat": False, "lon": False,
                },
                color_continuous_scale=color_scale,
                range_color=range_c,
                mapbox_style="carto-positron",
                zoom=4,
                center={"lat": 28.0, "lon": 3.0},
                labels={color_col: map_label},
                opacity=0.85,
            )

            if show_agencies and len(agencies_df) > 0:
                ags = agencies_df[agencies_df["wilaya"].isin(sel_wilaya)]
                company_colors = {
                    "CAAT": "#3B82F6", "CAAR": "#8B5CF6",
                    "SAA":  "#F59E0B", "TRUST": "#F05252",
                    "CASH": "#10B981", "CIAR":  "#6B7280",
                    "AMANA":"#EC4899",
                }
                for company, grp in ags.groupby("company"):
                    fig_map.add_trace(go.Scattermapbox(
                        lat=grp["lat"], lon=grp["lon"],
                        mode="markers",
                        marker=dict(size=5, color=company_colors.get(company, "#999")),
                        name=company,
                        hovertemplate=f"<b>{company}</b><br>%{{text}}<extra></extra>",
                        text=grp["zone"],
                    ))

            if show_gam:
                gam_df = df_f[df_f["existing_agencies"] > 0]
                fig_map.add_trace(go.Scattermapbox(
                    lat=gam_df["lat"], lon=gam_df["lon"],
                    mode="markers",
                    marker=dict(size=12, color="#085424"),
                    name="GAM",
                    hovertemplate="<b>GAM</b> — %{text}<extra></extra>",
                    text=gam_df["wilaya"] + " (" + gam_df["existing_agencies"].astype(str) + " ag.)",
                ))

            fig_map.update_layout(
                height=540,
                paper_bgcolor="rgba(0,0,0,0)",
                legend=dict(
                    bgcolor="rgba(255,255,255,0.95)",
                    bordercolor="#E8ECF0",
                    font=dict(color="#343C6A", size=10),
                ),
                margin=dict(l=0, r=0, t=0, b=0),
            )
            st.plotly_chart(fig_map, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 2 — SCORING & RANKING
# ══════════════════════════════════════════════
with tab2:
    if len(df_f) == 0:
        st.warning("No data to display.")
    else:
        left, right = st.columns([1.6, 1])

        with left:
            st.markdown("<div class='card-title'>Wilaya Ranking Table</div>", unsafe_allow_html=True)
            display_df = df_f[[
                "rank", "wilaya", "region", "score", "population",
                "demand", "gam_coverage", "comp_inv", "competition",
                "existing_agencies", "gap", "coverage"
            ]].sort_values("rank").reset_index(drop=True)
            display_df.columns = [
                "Rank", "Wilaya", "Region", "Score", "Population",
                "D (Demand)", "G (GAM Cov.)", "C (1-Comp)", "Other Agencies",
                "GAM Agencies", "Gap", "Coverage"
            ]
            st.dataframe(
                display_df.style
                    .background_gradient(subset=["Score"], cmap="RdYlGn")
                    .format({
                        "Score":         "{:.1f}",
                        "Population":    "{:,}",
                        "D (Demand)":    "{:.3f}",
                        "G (GAM Cov.)":  "{:.3f}",
                        "C (1-Comp)":    "{:.3f}",
                        "Coverage":      "{:.2f}",
                    }),
                use_container_width=True, height=320,
            )

        with right:
            st.markdown("<div class='card-title'>Top 10 Wilayas — Score</div>", unsafe_allow_html=True)
            top10 = df_f.nlargest(10, "score")
            fig_bar = px.bar(
                top10.sort_values("score"),
                x="score", y="wilaya", orientation="h",
                color="score",
                color_continuous_scale=[[0, "#bbca14"], [1, "#085424"]],
                labels={"score": "Score", "wilaya": ""},
            )
            fig_bar.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=False,
                                  coloraxis_showscale=False)
            fig_bar.update_traces(marker_line_width=0)
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("<div class='card-title'>Score Factor Breakdown — Selected Wilaya</div>", unsafe_allow_html=True)
        sel_zone_rank = st.selectbox("Select wilaya", df_f.sort_values("rank")["wilaya"].tolist(),
                                     key="rank_zone")
        zrow = df_f[df_f["wilaya"] == sel_zone_rank].iloc[0]

        total_w = w_demo + w_eco + w_ind + w_comp if (w_demo + w_eco + w_ind + w_comp) > 0 else 1
        factors = {
            "D — Demand":        zrow["demand"]       * (w_demo / total_w) * 100,
            "Eco / Income":      zrow["income_index"] * (w_eco  / total_w) * 100,
            "G — GAM Coverage":  zrow["gam_coverage"] * (w_ind  / total_w) * 100,
            "C — 1-Competition": zrow["comp_inv"]     * (w_comp / total_w) * 100,
        }
        colors = ["#3B82F6", "#F59E0B", "#085424", "#F05252"]

        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            for k, v in factors.items():
                pct   = min(v / (zrow["score"] + 0.001) * 100, 100)
                color = colors[list(factors.keys()).index(k)]
                st.markdown(f"""
                <div class="prog-wrap">
                  <div class="prog-label"><span>{k}</span><span style="color:{color};font-weight:700">{v:.1f}pts</span></div>
                  <div class="prog-bar-bg">
                    <div class="prog-bar-fill" style="width:{pct}%;background:{color}"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

        with c2:
            fig_radar = go.Figure(go.Scatterpolar(
                r=list(factors.values()),
                theta=list(factors.keys()),
                fill="toself",
                fillcolor="rgba(8,84,36,0.1)",
                line=dict(color="#085424", width=2),
                marker=dict(color="#085424", size=6),
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 35],
                                    gridcolor="#E8ECF0", linecolor="#E8ECF0",
                                    tickfont=dict(color="#6B7280")),
                    angularaxis=dict(gridcolor="#E8ECF0", linecolor="#E8ECF0",
                                     tickfont=dict(color="#343C6A")),
                    bgcolor="rgba(0,0,0,0)",
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=40, r=40, t=20, b=20),
                height=240,
                showlegend=False,
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with c3:
            for lbl, val, cls in [
                ("Overall Score",  f"{zrow['score']:.1f}",             "red"),
                ("Population",     f"{zrow['population']:,}",          "blue"),
                ("Competitors",    str(int(zrow["competition"])),       "amber"),
                ("GAM Agencies",   str(int(zrow["existing_agencies"])), "green"),
            ]:
                st.markdown(f"""
                <div class="mini-kpi" style="border-left:3px solid var(--{'red' if cls=='red' else 'blue' if cls=='blue' else 'amber' if cls=='amber' else 'green'})">
                  <div class="mini-kpi-label">{lbl}</div>
                  <div class="mini-kpi-value">{val}</div>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 3 — GAP & COVERAGE
# ══════════════════════════════════════════════
with tab3:
    if len(df_f) == 0:
        st.warning("No data to display.")
    else:
        left_g, right_g = st.columns([1.2, 1])

        with left_g:
            st.markdown("<div class='card-title'>Coverage Map — Required vs Existing GAM Agencies</div>", unsafe_allow_html=True)
            fig_gap_map = px.scatter_mapbox(
                df_f,
                lat="lat", lon="lon",
                color="gap",
                size=df_f["gap"].abs() + 1,
                size_max=25,
                hover_name="wilaya",
                hover_data={
                    "gap": True,
                    "required_agencies": True,
                    "existing_agencies": True,
                    "coverage": ":.2f",
                    "lat": False, "lon": False,
                },
                color_continuous_scale=[[0, "#085424"], [0.5, "#F59E0B"], [1, "#F05252"]],
                range_color=[df_f["gap"].min(), df_f["gap"].max()],
                mapbox_style="carto-positron",
                zoom=4,
                center={"lat": 28.0, "lon": 3.0},
                labels={"gap": "GAM Gap"},
                opacity=0.9,
            )
            fig_gap_map.update_layout(
                height=420, paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=0, b=0),
            )
            st.plotly_chart(fig_gap_map, use_container_width=True)

        with right_g:
            st.markdown("<div class='card-title'>GAM Coverage by Wilaya</div>", unsafe_allow_html=True)
            sorted_cov = df_f.sort_values("gap", ascending=False)[
                ["wilaya", "coverage", "gap", "required_agencies", "existing_agencies"]
            ]
            for _, row in sorted_cov.iterrows():
                cov_pct = min(row["coverage"] * 100, 200)
                if cov_pct < 40:
                    bar_color = "#F05252"
                    status    = "Under-served"
                elif cov_pct <= 100:
                    bar_color = "#F59E0B"
                    status    = "Developing"
                else:
                    bar_color = "#085424"
                    status    = "Covered"
                pill_cls = "pill-red" if cov_pct < 40 else ("pill-amber" if cov_pct <= 100 else "pill-green")
                st.markdown(f"""
                <div class="prog-wrap">
                  <div class="prog-label">
                    <span style="font-weight:600">{row['wilaya']}</span>
                    <span>
                      <span class="pill {pill_cls}">{status}</span>
                      &nbsp;<span style="color:{bar_color};font-size:0.72rem;font-weight:600">
                        {int(row['existing_agencies'])}/{int(row['required_agencies'])} · {cov_pct:.0f}%
                      </span>
                    </span>
                  </div>
                  <div class="prog-bar-bg">
                    <div class="prog-bar-fill" style="width:{min(cov_pct,100)}%;background:{bar_color}"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("<div class='card-title'>Gap Distribution</div>", unsafe_allow_html=True)
            fig_hist = px.histogram(df_f, x="gap", nbins=20,
                                    color_discrete_sequence=["#085424"])
            fig_hist.add_vline(x=0, line_dash="dash", line_color="#9CA3AF")
            fig_hist.update_layout(**PLOTLY_LAYOUT, height=260,
                                   xaxis_title="Gap (GAM agencies)", yaxis_title="# Wilayas")
            st.plotly_chart(fig_hist, use_container_width=True)

        with c2:
            st.markdown("<div class='card-title'>Required vs Existing GAM — Scatter</div>", unsafe_allow_html=True)
            fig_sc = px.scatter(
                df_f, x="required_agencies", y="existing_agencies",
                color="gap",
                color_continuous_scale=["#F05252", "#F59E0B", "#085424"],
                hover_name="wilaya",
                size="population", size_max=20,
                labels={"required_agencies": "Required", "existing_agencies": "GAM Existing"},
            )
            max_val = max(df_f["required_agencies"].max(), df_f["existing_agencies"].max()) + 1
            fig_sc.add_shape(type="line", x0=0, y0=0, x1=max_val, y1=max_val,
                             line=dict(color="#9CA3AF", dash="dot", width=1))
            fig_sc.update_layout(**PLOTLY_LAYOUT, height=260, coloraxis_showscale=False)
            st.plotly_chart(fig_sc, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 4 — WILAYA DETAIL
# ══════════════════════════════════════════════
with tab4:
    if len(df_f) == 0:
        st.warning("No data to display.")
    else:
        sel_zone_detail = st.selectbox(
            "Select wilaya to explore",
            df_f.sort_values("score", ascending=False)["wilaya"].tolist(),
            key="detail_zone",
        )
        zd = df_f[df_f["wilaya"] == sel_zone_detail].iloc[0]

        st.markdown("<div class='card-title'>Key Indicators</div>", unsafe_allow_html=True)
        cols = st.columns(5)
        metrics = [
            ("🎯", "Priority Score",  f"{zd['score']:.1f}",          "/ 100",              "red"),
            ("📉", "GAM Gap",         int(zd["gap"]),                  "agencies needed",    "amber"),
            ("👥", "Population",      f"{zd['population']:,}",         "inhabitants",        "blue"),
            ("🏢", "Other Agencies",  int(zd["competition"]),          "total agencies",     "lime"),
            ("📊", "GAM Coverage",    f"{zd['coverage']*100:.0f}%",   "existing/required",  "green"),
        ]
        for col, (icon, lbl, val, sub, cls) in zip(cols, metrics):
            with col:
                st.markdown(f"""
                <div class="kpi-card {cls}">
                  <div class="kpi-card-icon">{icon}</div>
                  <div class="kpi-label">{lbl}</div>
                  <div class="kpi-value">{val}</div>
                  <div class="kpi-sub">{sub}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("<div class='card-title'>D / G / C Profile</div>", unsafe_allow_html=True)
            profile_data = {
                "D — Demand index":   zd["demand"],
                "G — GAM coverage":   zd["gam_coverage"],
                "C — 1-Concurrence":  zd["comp_inv"],
                "Score (norm.)":      zd["score"] / 100,
            }
            for k, v in profile_data.items():
                color = "#085424" if v > 0.6 else ("#F59E0B" if v > 0.3 else "#F05252")
                st.markdown(f"""
                <div class="prog-wrap">
                  <div class="prog-label"><span style="font-weight:500">{k}</span><span style="color:{color};font-weight:700">{v:.3f}</span></div>
                  <div class="prog-bar-bg">
                    <div class="prog-bar-fill" style="width:{v*100:.1f}%;background:{color}"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown("<div class='card-title'>Competitor Breakdown</div>", unsafe_allow_html=True)
            wilaya_agencies = agencies_df[agencies_df["wilaya"] == sel_zone_detail]
            company_counts  = wilaya_agencies.groupby("company").size().reset_index(name="count")
            if len(company_counts) > 0:
                fig_comp = px.bar(
                    company_counts.sort_values("count", ascending=True),
                    x="count", y="company", orientation="h",
                    color="company",
                    color_discrete_sequence=["#3B82F6","#8B5CF6","#F59E0B",
                                             "#F05252","#085424","#6B7280","#EC4899"],
                    labels={"count": "Agencies", "company": ""},
                )
                fig_comp.update_layout(**PLOTLY_LAYOUT, height=220, showlegend=False,
                                       margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig_comp, use_container_width=True)
            else:
                st.info("No competitor data for this wilaya.")

        with c3:
            st.markdown("<div class='card-title'>GAM Position</div>", unsafe_allow_html=True)
            gam_g     = round(zd["gam_coverage"] * 100, 1)
            gam_color = "#085424" if gam_g >= 70 else ("#F59E0B" if gam_g >= 40 else "#F05252")
            nat_avg   = df["score"].mean()
            delta     = zd["score"] - nat_avg
            d_color   = "#085424" if delta >= 0 else "#F05252"
            d_sign    = "+" if delta >= 0 else ""

            st.markdown(f"""
            <div style="display:grid;gap:8px">
              <div class="mini-kpi" style="border-left:3px solid var(--green)">
                <div class="mini-kpi-label">G — GAM Coverage</div>
                <div class="mini-kpi-value" style="color:{gam_color}">{gam_g}%</div>
                <div class="mini-kpi-sub">{'Strong' if gam_g>=70 else ('Moderate' if gam_g>=40 else 'Weak')}</div>
              </div>
              <div class="mini-kpi" style="border-left:3px solid var(--blue)">
                <div class="mini-kpi-label">GAM Agencies</div>
                <div class="mini-kpi-value">{int(zd['existing_agencies'])}</div>
                <div class="mini-kpi-sub">Required: {int(zd['required_agencies'])}</div>
              </div>
              <div class="mini-kpi" style="border-left:3px solid var(--amber)">
                <div class="mini-kpi-label">vs National avg</div>
                <div class="mini-kpi-value" style="color:{d_color}">{d_sign}{delta:.1f}</div>
                <div class="mini-kpi-sub">Avg: {nat_avg:.1f}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        gap_v    = zd["gap"]
        comp_v   = zd["competition"]
        demand_v = zd["demand"]
        gam_v    = zd["gam_coverage"]
        c_v      = zd["comp_inv"]

        if gap_v > 5 and c_v >= 0.85:
            insight        = f"🟢 <b>Prime expansion zone.</b> GAM has only {int(zd['existing_agencies'])} agenc{'y' if zd['existing_agencies']==1 else 'ies'} vs {int(zd['required_agencies'])} required (gap = {int(gap_v)}). Very low competition (C = {c_v:.2f}) and strong demand (D = {demand_v:.3f}) make this a top-priority wilaya for immediate branch opening."
            insight_border = "#085424"
        elif gap_v > 0 and c_v >= 0.70:
            insight        = f"🟡 <b>Solid opportunity.</b> A GAM gap of {int(gap_v)} agencies exists with manageable competition (C = {c_v:.2f}). GAM coverage index G = {gam_v:.3f}. This wilaya fits a medium-term expansion plan."
            insight_border = "#F59E0B"
        elif gap_v <= 0 and c_v < 0.70:
            insight        = f"🔴 <b>Saturated & competitive.</b> GAM already meets the required threshold and faces high competition ({int(comp_v)} competitors, C = {c_v:.2f}). Focus on retention and product differentiation rather than new branches."
            insight_border = "#F05252"
        elif gap_v <= 0:
            insight        = f"🔵 <b>Covered market.</b> With {int(zd['existing_agencies'])} existing GAM agencies the wilaya is adequately served. Monitor population growth to trigger future reassessment."
            insight_border = "#3B82F6"
        else:
            insight        = f"🟠 <b>Mixed signals.</b> Gap of {int(gap_v)} exists but competition is high ({int(comp_v)} competitors, C = {c_v:.2f}). A niche, digital-first, or micro-agency strategy may outperform a traditional branch model here."
            insight_border = "#F59E0B"

        st.markdown(f"""
        <div class="insight-box" style="border-left-color:{insight_border}">
          <div class="insight-title">📍 Strategic Insight — {sel_zone_detail}</div>
          {insight}
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 5 — SCENARIO SIMULATION
# ══════════════════════════════════════════════
with tab5:
    st.markdown("<div class='card-title'>Scenario Engine — Adjust weights & rules to recompute live</div>", unsafe_allow_html=True)

    sc1, sc2 = st.columns(2)

    with sc1:
        st.markdown("""
        <div class="card">
          <div class="card-title" style="color:var(--blue)">🔵 Scenario A — Current</div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:0.82rem;color:var(--text2);line-height:2.3">
          D — Demand: <span style="color:var(--text);font-weight:700">{w_demo:.2f}</span><br>
          Eco / Income: <span style="color:var(--text);font-weight:700">{w_eco:.2f}</span><br>
          G — GAM Coverage: <span style="color:var(--text);font-weight:700">{w_ind:.2f}</span><br>
          C — Competition: <span style="color:var(--text);font-weight:700">{w_comp:.2f}</span><br>
          Rule: <span style="color:var(--text);font-weight:700">1 agency / {rule_pop:,} inhabitants</span>
        </div>
        </div>""", unsafe_allow_html=True)

    with sc2:
        st.markdown("<div class='card'><div class='card-title' style='color:#F59E0B'>🟠 Scenario B — Alternative</div>", unsafe_allow_html=True)
        s_w_demo = st.slider("D — Demand B",        0.0, 1.0, 0.40, 0.05, key="s_demo")
        s_w_eco  = st.slider("Eco B",               0.0, 1.0, 0.20, 0.05, key="s_eco")
        s_w_ind  = st.slider("G — GAM Coverage B",  0.0, 1.0, 0.15, 0.05, key="s_ind")
        s_w_comp = st.slider("C — Competition B",   0.0, 1.0, 0.25, 0.05, key="s_comp")
        s_rule   = st.number_input("Rule B (1 agency / N)", 5000, 50000, 12000, 1000, key="s_rule")
        st.markdown("</div>", unsafe_allow_html=True)

    df_b = compute_scores(df_base.copy(), s_w_demo, s_w_eco, s_w_ind, s_w_comp, s_rule)
    df_b = df_b[df_b["wilaya"].isin(sel_wilaya)]

    st.markdown("<div class='card-title'>Before / After — Rank Changes</div>", unsafe_allow_html=True)
    top_a = df_f.nlargest(30, "score")[["wilaya", "score", "rank"]].rename(
        columns={"score": "Score A", "rank": "Rank A"})
    top_b = df_b[df_b["wilaya"].isin(top_a["wilaya"])][["wilaya", "score", "rank"]].rename(
        columns={"score": "Score B", "rank": "Rank B"})
    comparison = top_a.merge(top_b, on="wilaya", how="left").sort_values("Rank A")
    comparison["Δ Rank"]  = comparison["Rank A"] - comparison["Rank B"]
    comparison["Δ Score"] = (comparison["Score B"] - comparison["Score A"]).round(1)

    st.dataframe(
        comparison.style
            .background_gradient(subset=["Score A", "Score B"], cmap="RdYlGn")
            .map(lambda v: "color:#085424;font-weight:700" if v > 0 else ("color:#F05252;font-weight:700" if v < 0 else ""),
                 subset=["Δ Rank", "Δ Score"])
            .format({"Score A": "{:.1f}", "Score B": "{:.1f}",
                     "Δ Score": "{:+.1f}", "Δ Rank": "{:+d}"}),
        use_container_width=True, height=380,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='card-title'>Score Distribution — A vs B</div>", unsafe_allow_html=True)
        fig_dist = go.Figure()
        fig_dist.add_trace(go.Histogram(x=df_f["score"], name="Scenario A",
                                        marker_color="#3B82F6", opacity=0.7, nbinsx=15))
        fig_dist.add_trace(go.Histogram(x=df_b["score"], name="Scenario B",
                                        marker_color="#085424", opacity=0.7, nbinsx=15))
        fig_dist.update_layout(**PLOTLY_LAYOUT, barmode="overlay", height=250,
                               xaxis_title="Score", yaxis_title="# Wilayas")
        st.plotly_chart(fig_dist, use_container_width=True)

    with c2:
        st.markdown("<div class='card-title'>Total GAM Gap — A vs B</div>", unsafe_allow_html=True)
        gap_a = int(df_f["gap"].clip(0).sum())
        gap_b = int(df_b["gap"].clip(0).sum())
        fig_gap_cmp = go.Figure(go.Bar(
            x=["Scenario A", "Scenario B"],
            y=[gap_a, gap_b],
            marker_color=["#3B82F6", "#085424"],
            text=[gap_a, gap_b],
            textposition="outside",
            textfont=dict(color="#343C6A", family="Plus Jakarta Sans"),
        ))
        fig_gap_cmp.update_layout(**PLOTLY_LAYOUT, height=250,
                                  yaxis_title="Total GAM agency gap", showlegend=False)
        st.plotly_chart(fig_gap_cmp, use_container_width=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="border-top:1px solid #E8ECF0;margin-top:2rem;padding-top:1.2rem;
            text-align:center;font-size:0.72rem;color:#9CA3AF;
            font-family:'Plus Jakarta Sans',sans-serif;font-weight:500;
            letter-spacing:0.04em">
  🛡️ GAM Assurance &nbsp;·&nbsp; Insurance Agency Location Optimizer
  &nbsp;·&nbsp; Algeria &nbsp;·&nbsp; AI / GIS Decision Support System
</div>
""", unsafe_allow_html=True)