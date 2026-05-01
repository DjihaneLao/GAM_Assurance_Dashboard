import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import base64, os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="GAM Assurance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)# logo
import base64

def get_base64_image(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
logo_base64 = get_base64_image("data/gam.png")

# ─────────────────────────────────────────────
# CUSTOM CSS
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

html, body, [class*="css"], .main {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font) !important;
}
.main .block-container { padding: 1.5rem 2rem 2rem !important; max-width: 100% !important; }

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
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

/* ── LOGO AREA ── */
            .sidebar-logo-img {
    width: 42px;
    height: 42px;
    object-fit: contain;
    border-radius: 10px;
}
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


.sidebar-section-title {
    font-size: 0.65rem; font-weight: 700; color: var(--text3);
    text-transform: uppercase; letter-spacing: 0.1em; padding: 0 0 0.5rem 0;
}

.page-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 1.5rem; gap: 1rem; }
.page-header-left h1 { font-size: 1.5rem !important; font-weight: 800 !important; color: var(--text) !important; margin: 0 0 0.25rem !important; letter-spacing: -0.02em; line-height: 1.2; }
.page-header-left .subtitle { font-size: 0.82rem; color: var(--text2); font-weight: 400; }
.badge-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 0.6rem; }
.badge { display: inline-flex; align-items: center; gap: 4px; background: var(--surface); border: 1px solid var(--border2); color: var(--text2); font-size: 0.67rem; font-weight: 600; padding: 3px 10px; border-radius: 20px; letter-spacing: 0.03em; }

.kpi-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.1rem 1.2rem 1rem; box-shadow: var(--shadow); position: relative; overflow: hidden; transition: box-shadow 0.2s, transform 0.2s; }
.kpi-card:hover { box-shadow: var(--shadow-md); transform: translateY(-1px); }
.kpi-label { font-size: 0.72rem; font-weight: 600; color: var(--text2); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.25rem; }
.kpi-value { font-size: 1.75rem; font-weight: 800; color: var(--text); line-height: 1; letter-spacing: -0.02em; }
.kpi-sub { font-size: 0.72rem; color: var(--text3); margin-top: 0.3rem; font-weight: 400; }
.kpi-card.blue  .kpi-value { color: var(--blue);  }
.kpi-card.green .kpi-value { color: var(--green); }
.kpi-card.red   .kpi-value { color: var(--red);   }
.kpi-card.amber .kpi-value { color: var(--amber); }
.kpi-card.lime  .kpi-value { color: #8a9a00;      }

[data-testid="stTabs"] [role="tablist"] { gap: 0 !important; border-bottom: 2px solid var(--border) !important; background: transparent !important; padding: 0 !important; }
[data-testid="stTabs"] [role="tab"] { font-family: var(--font) !important; font-size: 0.78rem !important; font-weight: 600 !important; color: var(--text2) !important; background: transparent !important; border: none !important; border-bottom: 2px solid transparent !important; padding: 10px 20px !important; border-radius: 0 !important; letter-spacing: 0.02em; margin-bottom: -2px !important; }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] { color: var(--green) !important; border-bottom: 2px solid var(--green) !important; background: transparent !important; }

.card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.2rem 1.3rem; box-shadow: var(--shadow); margin-bottom: 1rem; }
.card-title { font-size: 0.8rem; font-weight: 700; color: var(--text); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 1rem; display: flex; align-items: center; gap: 6px; }
.card-title::after { content: ''; flex: 1; height: 1px; background: var(--border); margin-left: 8px; }

.prog-wrap { margin: 5px 0 8px; }
.prog-label { font-size: 0.75rem; color: var(--text2); margin-bottom: 4px; display: flex; justify-content: space-between; font-weight: 500; }
.prog-bar-bg { background: var(--surface2); border-radius: 6px; height: 7px; overflow: hidden; }
.prog-bar-fill { height: 100%; border-radius: 6px; transition: width 0.5s cubic-bezier(.4,0,.2,1); }

.insight-box { background: var(--surface); border: 1px solid var(--border); border-left: 4px solid var(--green); border-radius: 0 var(--radius-sm) var(--radius-sm) 0; padding: 1rem 1.2rem; font-size: 0.86rem; color: var(--text); line-height: 1.65; box-shadow: var(--shadow); }
.insight-title { font-size: 0.65rem; font-weight: 700; color: var(--green); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.4rem; }

[data-testid="stDataFrame"] { border-radius: var(--radius) !important; overflow: hidden !important; box-shadow: var(--shadow) !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }

.mini-kpi { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 0.75rem 1rem; margin-bottom: 8px; box-shadow: var(--shadow); }
.mini-kpi-label { font-size: 0.68rem; color: var(--text3); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px; }
.mini-kpi-value { font-size: 1.2rem; font-weight: 800; color: var(--text); letter-spacing: -0.01em; }
.mini-kpi-sub   { font-size: 0.68rem; color: var(--text3); margin-top: 1px; }

.pill { display: inline-block; padding: 2px 9px; border-radius: 20px; font-size: 0.66rem; font-weight: 700; letter-spacing: 0.04em; }
.pill-green { background: var(--green-pale); color: var(--green); }
.pill-amber { background: var(--amber-pale); color: #b45309; }
.pill-red   { background: var(--red-pale);   color: var(--red); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# WILAYA COORDINATES
# ─────────────────────────────────────────────
WILAYA_COORDS = {
    "SETIF": (36.190, 5.408), "ORAN": (35.697, -0.633), "TIZI OUZOU": (36.712, 4.046),
    "TLEMCEN": (34.878, -1.315), "DJELFA": (34.671, 3.263), "TIARET": (35.370, 1.317),
    "CONSTANTINE": (36.365, 6.615), "CHLEF": (36.165, 1.330), "BATNA": (35.556, 6.174),
    "BLIDA": (36.470, 2.830), "MASCARA": (35.396, 0.140), "MEDEA": (36.264, 2.751),
    "BOUIRA": (36.374, 3.901), "MOSTAGANEM": (35.931, 0.089), "SKIKDA": (36.876, 6.908),
    "OUARGLA": (31.952, 5.325), "MILA": (36.450, 6.264), "JIJEL": (36.819, 5.766),
    "BEJAIA": (36.756, 5.084), "RELIZANE": (35.738, 0.556), "TEBESSA": (35.405, 8.119),
    "AIN DEFLA": (36.264, 1.967), "BOUMERDES": (36.761, 3.478), "TIPAZA": (36.589, 2.449),
    "ANNABA": (36.900, 7.765), "GHARDAIA": (32.490, 3.674), "BISKRA": (34.850, 5.728),
    "OUM EL BOUAGHI": (35.877, 7.113), "SIDI BEL ABBES": (35.190, -0.630),
    "AIN TEMOUCHENT": (35.298, -1.141), "SAIDA": (34.831, 0.152),
    "SOUK AHRAS": (36.285, 7.951), "GUELMA": (36.462, 7.428), "EL OUED": (33.368, 6.864),
    "EL TARF": (36.767, 8.313), "KHENCHELA": (35.435, 7.143), "ADRAR": (27.874, -0.294),
    "LAGHOUAT": (33.799, 2.864), "BECHAR": (31.617, -2.216), "TISSEMSILT": (35.607, 1.811),
    "EL BAYADH": (33.682, 1.017), "TAMANRASSET": (22.785, 5.523), "NAAMA": (33.267, -0.313),
    "TINDOUF": (27.674, -8.149), "ILLIZI": (26.507, 8.483), "ALGER": (36.737, 3.086),
    "M'SILA": (35.706, 4.543), "BORDJ BOU ARRERIDJ": (36.073, 4.763),
}

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data(path="data/Scoring_with_region_ranksData.csv"):
    df = pd.read_csv(path)
    df["Wilaya"] = df["Wilaya"].str.strip().str.upper()
    df = df.rename(columns={
        "Wilaya":               "wilaya",
        "Population":           "population",
        "GAM_Agencies":         "existing_agencies",
        "Final_Priority_Score": "score_raw",
        "D":                    "demand",
        "G":                    "gam_coverage",
        "C":                    "comp_inv",
        "R":                    "risk",
        "Attractivite":         "attractivite",
        "Region":               "region",
        "Region_Rank":          "region_rank",
    })
    df["score"] = (df["score_raw"] * 100).round(1)
    df["lat"] = df["wilaya"].map(lambda w: WILAYA_COORDS.get(w, (None, None))[0])
    df["lon"] = df["wilaya"].map(lambda w: WILAYA_COORDS.get(w, (None, None))[1])
    df = df.dropna(subset=["lat", "lon"])
    return df

@st.cache_data
def load_region_summary(path="data/Scoring_with_region_ranksData.csv"):
    return pd.read_csv(path)

df_base = load_data()
region_summary = load_region_summary()

# ─────────────────────────────────────────────
# SCORING / COVERAGE FUNCTION
# ─────────────────────────────────────────────
def compute_coverage(df, w_demand, w_gap, w_comp, w_risk, rule_pop=15000):
    df = df.copy()
    total = w_demand + w_gap + w_comp + w_risk or 1
    df["score_sim"] = (
        df["demand"]      * (w_demand / total) +
        df["gam_coverage"]* (w_gap    / total) +
        df["comp_inv"]    * (w_comp   / total) +
        df["risk"]        * (w_risk   / total)
    ) * 100

    base_req  = df["population"] / rule_pop
    dens_fac  = np.log1p(df["population"]) / np.log1p(df["population"].max())
    df["required_agencies"] = (base_req * (0.65 + 0.35 * dens_fac)).apply(lambda x: max(1, round(x)))
    df["gap"]      = df["required_agencies"] - df["existing_agencies"]
    df["coverage"] = (df["existing_agencies"] / df["required_agencies"]).clip(0, 2).round(2)
    df["rank"]     = df["score"].rank(ascending=False).astype(int)
    return df

RULE_POP = 15000
df_base = compute_coverage(df_base, 0.40, 0.20, 0.20, 0.20, RULE_POP)
#function simulation 
# ─────────────────────────────────────────────
# FINANCIAL SIMULATION FUNCTION
# ─────────────────────────────────────────────
@st.cache_data
def run_financial_simulation(df, top_n, total_ca, total_agencies):

    df = df.copy()

    base_ca_per_agency = total_ca / total_agencies

    df = df.sort_values("score_raw", ascending=False).reset_index(drop=True)
    top = df.head(top_n).copy()

    top["Score_Factor"] = 0.8 + 0.4 * top["score_raw"]

    top["CA_full"] = base_ca_per_agency * top["Score_Factor"]
    top["CA_Y1"] = top["CA_full"] * 0.60
    top["CA_Y2"] = top["CA_full"] * 0.85
    top["CA_Y3"] = top["CA_full"]

    top["CA_Y3_pess"] = top["CA_Y3"] * 0.80
    top["CA_Y3_opt"]  = top["CA_Y3"] * 1.20

    top["pop_per_ag_before"] = top["population"] / top["existing_agencies"].replace(0, np.nan)
    top["pop_per_ag_after"]  = top["population"] / (top["existing_agencies"] + 1)

    top["coverage_improvement"] = (
        (top["pop_per_ag_before"] - top["pop_per_ag_after"])
        / top["pop_per_ag_before"]
    ) * 100

    return top.round(2), base_ca_per_agency
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
)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-logo">
        <img src="data:image/png;base64,{logo_base64}" class="sidebar-logo-img">
        <div>
            <div class="sidebar-logo-text">GAM Assurance</div>
            <div class="sidebar-logo-sub"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sidebar-section-title'>Filters</div>", unsafe_allow_html=True)
    wilayas_list = sorted(df_base["wilaya"].unique().tolist())
    sel_wilaya   = st.multiselect("Wilaya", wilayas_list, default=wilayas_list)

# ─────────────────────────────────────────────
# FILTER
# ─────────────────────────────────────────────
mask = (
    df_base["wilaya"].isin(sel_wilaya) 
    
    
    
)
df_f = df_base[mask].copy()

# ─────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <div class="page-header-left">
    <h1>Optimisation des Agences d'Assurance</h1>
    <div class="subtitle">Scoring spatial & analyse des écarts · Marché Algérien</div>
    <div class="badge-row">
      <span class="badge">GIS</span>
      <span class="badge">Spatial Analysis</span>
      <span class="badge">Multi-Criteria Scoring</span>
      <span class="badge">Coverage Optimization</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
total_gap  = df_f["gap"].clip(0).sum()
avg_score  = df_f["score"].mean() if len(df_f) else 0
avg_cov    = df_f["coverage"].mean() if len(df_f) else 0
n_plus     = (df_f["attractivite"] == "Plus Attractive").sum()

k1, k2, k3, k4 = st.columns(4)
for col, label, value, sub, cls in [
    (k1, "Wilayas",         len(df_f),              "after filters",          "blue"),
    (k2, "Avg. Score",      f"{avg_score:.1f}",     "out of 100",             "amber"),
    (k3, "Plus Attractive", int(n_plus),             "top-tier wilayas",       "green"),
    (k4, "GAM Coverage",    f"{avg_cov*100:.0f}%",   "existing / required",    "lime"),
]:
    with col:
        st.markdown(f"""
        <div class="kpi-card {cls}">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Geographic Analysis",
    "Scoring & Ranking",
    "Wilaya Detail",
    "Scenario Simulation",
])

# ══════════════════════════════════════════════
# TAB 1 — GEOGRAPHIC ANALYSIS
# ══════════════════════════════════════════════
with tab1:
    col_map, col_ctrl = st.columns([3, 1])

    with col_ctrl:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Map Options</div>", unsafe_allow_html=True)
        map_layer = st.radio("Overlay", ["Score", "Gap", "Coverage", "Risk"], index=0)
        show_gam  = st.checkbox("Show GAM agencies", value=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Region summary mini-table
        st.markdown("<div class='card-title'>Region Rankings</div>", unsafe_allow_html=True)
        for _, row in region_summary.iterrows():
            rank_color = ["#085424","#3B82F6","#F59E0B","#F05252"][int(row["Region_Rank"])-1]
            st.markdown(f"""
            <div class="mini-kpi" style="border-left:3px solid {rank_color}">
              <div class="mini-kpi-label">#{int(row['Region_Rank'])} {row['Region']}</div>
              <div class="mini-kpi-value" style="font-size:0.95rem">{row['Wilaya']}</div>
              <div class="mini-kpi-sub">Score: {row['Final_Priority_Score']*100:.1f}</div>
            </div>""", unsafe_allow_html=True)

    with col_map:
        st.markdown("<div class='card-title'>Attractiveness Map — Wilayas scored by opportunity index</div>", unsafe_allow_html=True)
        if len(df_f) == 0:
            st.warning("No zones match current filters.")
        else:
            layer_cfg = {
                "Score":    ("score",    [[0,"#56d364"],[0.5,"#F59E0B"],[1,"#F05252"]], [0,100],   "Score"),
                "Gap":      ("gap",      [[0,"#56d364"],[0.5,"#F59E0B"],[1,"#F05252"]], None,       "Gap"),
                "Coverage": ("coverage", [[0,"#F05252"],[0.5,"#F59E0B"],[1,"#085424"]], [0,2],      "Coverage"),
                "Risk":     ("risk",     [[0,"#EFF6FF"],[0.5,"#3B82F6"],[1,"#1e3a8a"]], [0,1],      "Risk (R)"),
            }
            col_field, cscale, rng, clabel = layer_cfg[map_layer]
            rng = rng or [df_f[col_field].min(), df_f[col_field].max()]

            # Attractivite → symbol
            sym_map = {"Plus Attractive": "circle", "Moyennement Attractive": "circle-open", "Moins Attractive": "x"}
            df_f["symbol"] = df_f["attractivite"].map(sym_map).fillna("circle")

            fig_map = px.scatter_mapbox(
                df_f, lat="lat", lon="lon",
                color=col_field, size="population", size_max=28,
                hover_name="wilaya",
                hover_data={
                    "region": True, "attractivite": True,
                    "score": ":.1f", "population": ":,",
                    "gap": True, "coverage": ":.2f",
                    "demand": ":.3f", "risk": ":.3f",
                    "lat": False, "lon": False,
                },
                color_continuous_scale=cscale,
                range_color=rng,
                mapbox_style="carto-positron",
                zoom=4, center={"lat": 28.0, "lon": 3.0},
                labels={col_field: clabel},
                opacity=0.85,
            )

            if show_gam:
                gam_df = df_f[df_f["existing_agencies"] > 0]
                fig_map.add_trace(go.Scattermapbox(
                    lat=gam_df["lat"], lon=gam_df["lon"],
                    mode="markers",
                    marker=dict(size=11, color="#085424"),
                    name="GAM present",
                    hovertemplate="<b>GAM</b> — %{text}<extra></extra>",
                    text=gam_df["wilaya"] + " (" + gam_df["existing_agencies"].astype(str) + " ag.)",
                ))

            fig_map.update_layout(
                height=540, paper_bgcolor="rgba(0,0,0,0)",
                legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor="#E8ECF0", font=dict(color="#343C6A", size=10)),
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
            disp = df_f[[
                "rank", "wilaya", "region", "attractivite", "score",
                "population", "demand", "gam_coverage", "comp_inv", "risk",
                "existing_agencies", "coverage"
            ]].sort_values("rank").reset_index(drop=True)
            disp.columns = [
                "Rank", "Wilaya", "Region", "Attractivité", "Score",
                "Population", "D (Demand)", "G (GAM Cov.)", "C (1-Comp)", "R (Risk)",
                "GAM Agencies", "Coverage"
            ]
            st.dataframe(
                disp.style
                    .background_gradient(subset=["Score"], cmap="RdYlGn")
                    .format({
                        "Score": "{:.1f}", "Population": "{:,}",
                        "D (Demand)": "{:.3f}", "G (GAM Cov.)": "{:.3f}",
                        "C (1-Comp)": "{:.3f}", "R (Risk)": "{:.3f}",
                        "Coverage": "{:.2f}",
                    }),
                use_container_width=True, height=340,
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
            fig_bar.update_layout(**PLOTLY_LAYOUT, height=340, showlegend=False, coloraxis_showscale=False)
            fig_bar.update_traces(marker_line_width=0)
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("<div class='card-title'>Score Factor Breakdown — Selected Wilaya</div>", unsafe_allow_html=True)
        sel_zone = st.selectbox("Select wilaya", df_f.sort_values("rank")["wilaya"].tolist(), key="rank_zone")
        zrow = df_f[df_f["wilaya"] == sel_zone].iloc[0]

        factors = {
            "D — Demand":        zrow["demand"]       * 0.40 * 100,
            "G — GAM Coverage":  zrow["gam_coverage"] * 0.20 * 100,
            "C — 1-Competition": zrow["comp_inv"]     * 0.20 * 100,
            "R — Risk":          zrow["risk"]          * 0.20 * 100,
        }
        colors = ["#3B82F6", "#085424", "#F05252", "#F59E0B"]

        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            for (k, v), color in zip(factors.items(), colors):
                pct = min(v / (zrow["score"] + 0.001) * 100, 100)
                st.markdown(f"""
                <div class="prog-wrap">
                  <div class="prog-label"><span>{k}</span><span style="color:{color};font-weight:700">{v:.1f}pts</span></div>
                  <div class="prog-bar-bg"><div class="prog-bar-fill" style="width:{pct}%;background:{color}"></div></div>
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
                    radialaxis=dict(visible=True, range=[0, 45], gridcolor="#E8ECF0", linecolor="#E8ECF0", tickfont=dict(color="#6B7280")),
                    angularaxis=dict(gridcolor="#E8ECF0", linecolor="#E8ECF0", tickfont=dict(color="#343C6A")),
                    bgcolor="rgba(0,0,0,0)",
                ),
                paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=40, r=40, t=20, b=20),
                height=260, showlegend=False,
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with c3:
            attract_color = {"Plus Attractive": "green", "Moyennement Attractive": "amber", "Moins Attractive": "red"}.get(zrow["attractivite"], "blue")
            for lbl, val, border in [
                ("Overall Score",    f"{zrow['score']:.1f}",              "--red"),
                ("Attractivité",     zrow["attractivite"].replace(" ","<br>"), f"--{attract_color}"),
                ("Population",       f"{zrow['population']:,}",            "--blue"),
                ("GAM Agencies",     str(int(zrow["existing_agencies"])),  "--green"),
            ]:
                st.markdown(f"""
                <div class="mini-kpi" style="border-left:3px solid var({border})">
                  <div class="mini-kpi-label">{lbl}</div>
                  <div class="mini-kpi-value" style="font-size:1rem">{val}</div>
                </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 — WILAYA DETAIL
# ══════════════════════════════════════════════
with tab3:
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
        cols = st.columns(4)
        attract_col = {"Plus Attractive": "green", "Moyennement Attractive": "amber", "Moins Attractive": "red"}.get(zd["attractivite"], "blue")
        for col, lbl, val, sub, cls in zip(cols, [
            "Priority Score", "Attractivité", "Population", "Risk Score"
        ], [
            f"{zd['score']:.1f}", zd["attractivite"].replace(" Attractive",""),
            f"{zd['population']:,}", f"{zd['risk']:.3f}"
        ], [
            "/ 100", "classification", "agencies needed", "inhabitants", "0–1 index"
        ], ["red", attract_col, "amber", "blue", "lime"]):
            with col:
                st.markdown(f"""
                <div class="kpi-card {cls}">
                  <div class="kpi-label">{lbl}</div>
                  <div class="kpi-value" style="font-size:{'1.3rem' if len(str(val))>6 else '1.75rem'}">{val}</div>
                  <div class="kpi-sub">{sub}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("<div class='card-title'>D / G / C / R Profile</div>", unsafe_allow_html=True)
            for k, v, color in [
                ("D — Demand index",    zd["demand"],       "#3B82F6"),
                ("G — GAM coverage",    zd["gam_coverage"], "#085424"),
                ("C — 1-Competition",   zd["comp_inv"],     "#F05252"),
                ("R — Risk index",      zd["risk"],         "#F59E0B"),
                ("Score (normalised)",  zd["score"]/100,    "#8B5CF6"),
            ]:
                color = "#085424" if v > 0.6 else ("#F59E0B" if v > 0.3 else "#F05252")
                st.markdown(f"""
                <div class="prog-wrap">
                  <div class="prog-label"><span style="font-weight:500">{k}</span><span style="color:{color};font-weight:700">{v:.3f}</span></div>
                  <div class="prog-bar-bg"><div class="prog-bar-fill" style="width:{v*100:.1f}%;background:{color}"></div></div>
                </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown("<div class='card-title'>Factor Radar</div>", unsafe_allow_html=True)
            radar_vals = {
                "D — Demand": zd["demand"] * 0.40 * 100,
                "G — GAM Cov.": zd["gam_coverage"] * 0.20 * 100,
                "C — 1-Comp": zd["comp_inv"] * 0.20 * 100,
                "R — Risk": zd["risk"] * 0.20 * 100,
            }
            fig_radar2 = go.Figure(go.Scatterpolar(
                r=list(radar_vals.values()), theta=list(radar_vals.keys()),
                fill="toself", fillcolor="rgba(8,84,36,0.1)",
                line=dict(color="#085424", width=2), marker=dict(color="#085424", size=6),
            ))
            fig_radar2.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 45], gridcolor="#E8ECF0", tickfont=dict(color="#6B7280")),
                    angularaxis=dict(gridcolor="#E8ECF0", tickfont=dict(color="#343C6A")),
                    bgcolor="rgba(0,0,0,0)",
                ),
                paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=40, r=40, t=20, b=20),
                height=260, showlegend=False,
            )
            st.plotly_chart(fig_radar2, use_container_width=True)

        with c3:
            st.markdown("<div class='card-title'>GAM Position</div>", unsafe_allow_html=True)
            gam_g = round(zd["gam_coverage"] * 100, 1)
            gam_color = "#085424" if gam_g >= 70 else ("#F59E0B" if gam_g >= 40 else "#F05252")
            nat_avg = df_base["score"].mean()
            delta = zd["score"] - nat_avg
            d_color = "#085424" if delta >= 0 else "#F05252"
            d_sign = "+" if delta >= 0 else ""
            reg_rank = int(zd["region_rank"])

            st.markdown(f"""
            <div style="display:grid;gap:8px">
              <div class="mini-kpi" style="border-left:3px solid var(--green)">
                <div class="mini-kpi-label">G — GAM Coverage</div>
                <div class="mini-kpi-value" style="color:{gam_color}">{gam_g}%</div>
                <div class="mini-kpi-sub">{'Strong' if gam_g>=70 else ('Moderate' if gam_g>=40 else 'Weak')}</div>
              </div>
              <div class="mini-kpi" style="border-left:3px solid var(--blue)">
                <div class="mini-kpi-label">Region</div>
                <div class="mini-kpi-value" style="font-size:1rem">{zd['region']} · Rank #{reg_rank}</div>
              </div>
              <div class="mini-kpi" style="border-left:3px solid var(--amber)">
                <div class="mini-kpi-label">vs National avg</div>
                <div class="mini-kpi-value" style="color:{d_color}">{d_sign}{delta:.1f}</div>
                <div class="mini-kpi-sub">Avg: {nat_avg:.1f}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        # Strategic insight
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        gap_v  = zd["gap"]
        c_v    = zd["comp_inv"]
        d_v    = zd["demand"]
        r_v    = zd["risk"]
        att    = zd["attractivite"]

        if att == "Plus Attractive" and gap_v > 0:
            insight = f"<b>Prime expansion zone.</b> Ranked as <i>Plus Attractive</i> with a GAM gap of {int(gap_v)} agencies. High demand (D={d_v:.3f}) and low competition (C={c_v:.3f}) — top priority for immediate branch opening."
            insight_border = "#085424"
        elif att == "Moyennement Attractive" and gap_v > 0:
            insight = f"<b>Solid opportunity.</b> Classified <i>Moyennement Attractive</i>. Gap of {int(gap_v)} with manageable competition (C={c_v:.3f}) and risk index R={r_v:.3f}. Fits a medium-term expansion plan."
            insight_border = "#F59E0B"
        elif att == "Moins Attractive" and gap_v > 0:
            insight = f"<b>Mixed signals.</b> Despite a gap of {int(gap_v)} agencies, this wilaya is <i>Moins Attractive</i> due to weak demand (D={d_v:.3f}). A niche or digital-first strategy may outperform a traditional branch here."
            insight_border = "#F59E0B"
        elif gap_v <= 0:
            insight = f"<b>Covered market.</b> With {int(zd['existing_agencies'])} existing GAM agencies the wilaya meets the required threshold. Monitor population growth to trigger future reassessment."
            insight_border = "#3B82F6"
        else:
            insight = f"<b>Saturated & competitive.</b> High competition (C={c_v:.3f}) limits expansion viability. Focus on retention and product differentiation."
            insight_border = "#F05252"

        st.markdown(f"""
        <div class="insight-box" style="border-left-color:{insight_border}">
          <div class="insight-title">Strategic Insight — {sel_zone_detail}</div>
          {insight}
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 5 — SCENARIO SIMULATION
# ══════════════════════════════════════════════
with tab4:
    st.markdown("<div class='card-title'>Financial Simulation — New Agency Impact</div>", unsafe_allow_html=True)

    # ── CONTROLS
    c1, c2, c3 = st.columns(3)

    with c1:
        top_n = st.slider("Top locations to simulate", 1, 10, 4)

    with c2:
        total_ca = st.number_input("GAM Total CA (Million DA)", value=3019)

    with c3:
        total_agencies = st.number_input("Total agencies", value=204)

    # ── RUN SIMULATION
    sim_df, base_ca = run_financial_simulation(df_f, top_n, total_ca, total_agencies)

    # ── KPI ROW
    total_y1 = sim_df["CA_Y1"].sum()
    total_y2 = sim_df["CA_Y2"].sum()
    total_y3 = sim_df["CA_Y3"].sum()

    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Base CA / Agency", f"{base_ca:.1f} MDA")
    k2.metric("Year 1 Total", f"{total_y1:.1f} MDA")
    k3.metric("Year 2 Total", f"{total_y2:.1f} MDA")
    k4.metric("Year 3 Total", f"{total_y3:.1f} MDA")

    # ── BAR CHART (REPLACE MATPLOTLIB)
    fig = px.bar(
        sim_df,
        x="wilaya",
        y=["CA_Y1", "CA_Y2", "CA_Y3"],
        barmode="group",
        labels={"value": "CA (Million DA)", "variable": "Year"},
        color_discrete_map={
        "CA_Y1": "#085424",
        "CA_Y2": "#5bb862",
        "CA_Y3": "#c4cf84"
    }
    )

    fig.update_layout(**PLOTLY_LAYOUT, height=400)
    st.plotly_chart(fig, use_container_width=True)


    # ── TABLE
    st.markdown("<div class='card-title'>Detailed Financial Table</div>", unsafe_allow_html=True)

    st.dataframe(
        sim_df[[
            "wilaya",
            "population",
            "existing_agencies",
            "score_raw",
            "CA_Y1",
            "CA_Y2",
            "CA_Y3",
            "coverage_improvement"
        ]],
        use_container_width=True
    )

    # ── DOWNLOAD
    csv = sim_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Download Results CSV", csv, "simulation_results.csv")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="border-top:1px solid #E8ECF0;margin-top:2rem;padding-top:1.2rem;
            text-align:center;font-size:0.72rem;color:#9CA3AF;
            font-family:'Plus Jakarta Sans',sans-serif;font-weight:500;letter-spacing:0.04em">
  GAM Assurance &nbsp;·&nbsp; Insurance Agency Location Optimizer
  &nbsp;·&nbsp; Algeria &nbsp;·&nbsp; Decision Support System
</div>
""", unsafe_allow_html=True)