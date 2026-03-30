import streamlit as st
import pandas as pd
import numpy as np
import os

# ─────────────────────────────────────────────────────────
# FILE PATHS  <-- edit these to match your disk location
# ─────────────────────────────────────────────────────────
IMPORT_FILE = "./import_data.csv"
EXPORT_FILE = "./export_data.csv"

# ─────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India – West Asia Trade Risk Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────
# HSN 2-DIGIT DESCRIPTION MAP
# ─────────────────────────────────────────────────────────
HSN2_DESC = {
    "01": "Live animals",
    "02": "Meat and edible meat offal",
    "03": "Fish and crustaceans, molluscs and other aquatic invertebrates",
    "04": "Dairy produce; birds' eggs; natural honey; edible products of animal origin",
    "05": "Products of animal origin, not elsewhere specified or included",
    "06": "Live trees and other plants; bulbs, roots; cut flowers and ornamental foliage",
    "07": "Edible vegetables and certain roots and tubers",
    "08": "Edible fruit and nuts; peel of citrus fruit or melons",
    "09": "Coffee, tea, maté and spices",
    "10": "Cereals",
    "11": "Products of the milling industry; malt; starches; inulin; wheat gluten",
    "12": "Oil seeds and oleaginous fruits; miscellaneous grains, seeds and fruit; industrial or medicinal plants",
    "13": "Lac; gums, resins and other vegetable saps and extracts",
    "14": "Vegetable plaiting materials; vegetable products not elsewhere specified",
    "15": "Animal or vegetable fats and oils and their cleavage products; prepared edible fats",
    "16": "Preparations of meat, of fish or of crustaceans, molluscs or other aquatic invertebrates",
    "17": "Sugars and sugar confectionery",
    "18": "Cocoa and cocoa preparations",
    "19": "Preparations of cereals, flour, starch or milk; pastrycooks' products",
    "20": "Preparations of vegetables, fruit, nuts or other parts of plants",
    "21": "Miscellaneous edible preparations",
    "22": "Beverages, spirits and vinegar",
    "23": "Residues and waste from the food industries; prepared animal fodder",
    "24": "Tobacco and manufactured tobacco substitutes",
    "25": "Salt; sulphur; earths and stone; plastering materials, lime and cement",
    "26": "Ores, slag and ash",
    "27": "Mineral fuels, mineral oils and products of their distillation; bituminous substances",
    "28": "Inorganic chemicals; organic or inorganic compounds of precious metals",
    "29": "Organic chemicals",
    "30": "Pharmaceutical products",
    "31": "Fertilisers",
    "32": "Tanning or dyeing extracts; dyes, pigments; paints and varnishes; inks",
    "33": "Essential oils and resinoids; perfumery, cosmetic or toilet preparations",
    "34": "Soap, organic surface-active agents, washing preparations, lubricating preparations",
    "35": "Albuminoidal substances; modified starches; glues; enzymes",
    "36": "Explosives; pyrotechnic products; matches; pyrophoric alloys",
    "37": "Photographic or cinematographic goods",
    "38": "Miscellaneous chemical products",
    "39": "Plastics and articles thereof",
    "40": "Rubber and articles thereof",
    "41": "Raw hides and skins (other than furskins) and leather",
    "42": "Articles of leather; saddlery and harness; travel goods, handbags",
    "43": "Furskins and artificial fur; manufactures thereof",
    "44": "Wood and articles of wood; wood charcoal",
    "45": "Cork and articles of cork",
    "46": "Manufactures of straw, of esparto or of other plaiting materials; basketware",
    "47": "Pulp of wood or of other fibrous cellulosic material; recovered paper or paperboard",
    "48": "Paper and paperboard; articles of paper pulp, of paper or of paperboard",
    "49": "Printed books, newspapers, pictures and other products of the printing industry",
    "50": "Silk",
    "51": "Wool, fine or coarse animal hair; horsehair yarn and woven fabric",
    "52": "Cotton",
    "53": "Other vegetable textile fibres; paper yarn and woven fabrics of paper yarn",
    "54": "Man-made filaments",
    "55": "Man-made staple fibres",
    "56": "Wadding, felt and nonwovens; special yarns; twine, cordage, ropes and cables",
    "57": "Carpets and other textile floor coverings",
    "58": "Special woven fabrics; tufted textile fabrics; lace; tapestries; trimmings; embroidery",
    "59": "Impregnated, coated, covered or laminated textile fabrics; industrial textile articles",
    "60": "Knitted or crocheted fabrics",
    "61": "Articles of apparel and clothing accessories, knitted or crocheted",
    "62": "Articles of apparel and clothing accessories, not knitted or crocheted",
    "63": "Other made up textile articles; sets; worn clothing and worn textile articles; rags",
    "64": "Footwear, gaiters and the like; parts of such articles",
    "65": "Headgear and parts thereof",
    "66": "Umbrellas, sun umbrellas, walking-sticks, whips, riding-crops and parts thereof",
    "67": "Prepared feathers and down; artificial flowers; articles of human hair",
    "68": "Articles of stone, plaster, cement, asbestos, mica or similar materials",
    "69": "Ceramic products",
    "70": "Glass and glassware",
    "71": "Natural or cultured pearls, precious or semi-precious stones, precious metals; coin",
    "72": "Iron and steel",
    "73": "Articles of iron or steel",
    "74": "Copper and articles thereof",
    "75": "Nickel and articles thereof",
    "76": "Aluminium and articles thereof",
    "77": "Reserved for possible future use",
    "78": "Lead and articles thereof",
    "79": "Zinc and articles thereof",
    "80": "Tin and articles thereof",
    "81": "Other base metals; cermets; articles thereof",
    "82": "Tools, implements, cutlery, spoons and forks, of base metal; parts thereof",
    "83": "Miscellaneous articles of base metal",
    "84": "Nuclear reactors, boilers, machinery and mechanical appliances; parts thereof",
    "85": "Electrical machinery and equipment and parts thereof; sound and video recorders",
    "86": "Railway or tramway locomotives, rolling-stock and parts thereof",
    "87": "Vehicles other than railway or tramway rolling-stock, and parts and accessories thereof",
    "88": "Aircraft, spacecraft, and parts thereof",
    "89": "Ships, boats and floating structures",
    "90": "Optical, photographic, measuring, checking, precision, medical or surgical instruments",
    "91": "Clocks and watches and parts thereof",
    "92": "Musical instruments; parts and accessories of such articles",
    "93": "Arms and ammunition; parts and accessories thereof",
    "94": "Furniture; bedding, mattresses; lamps and lighting fittings; prefabricated buildings",
    "95": "Toys, games and sports requisites; parts and accessories thereof",
    "96": "Miscellaneous manufactured articles",
    "97": "Works of art, collectors' pieces and antiques",
    "98": "Project imports; laboratory chemicals; passengers' baggage; personal importations",
}

WEST_ASIA_COUNTRIES = [
    "U ARAB EMTS", "KUWAIT", "SYRIA", "OMAN",
    "BAHARAIN IS", "ISRAEL", "IRAN", "IRAQ",
    "JORDAN", "SAUDI ARAB", "YEMEN REPUBLC",
    "LEBANON", "QATAR"
]
WA_UPPER = [c.upper() for c in WEST_ASIA_COUNTRIES]

# ─────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600&family=DM+Sans:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main-header {
    background: linear-gradient(135deg, #0f2340 0%, #1a3a5c 60%, #0d3b6e 100%);
    padding: 2.2rem 2.5rem 1.8rem 2.5rem;
    border-radius: 12px;
    margin-bottom: 1.8rem;
    border-bottom: 3px solid #c9a84c;
    box-shadow: 0 4px 24px rgba(0,0,0,0.18);
}
.main-header h1 {
    font-family: 'EB Garamond', serif;
    color: #f0e6cc; font-size: 2.1rem; font-weight: 600;
    margin: 0 0 0.3rem 0; letter-spacing: 0.02em;
}
.main-header p {
    color: #a8c0d6; font-size: 0.88rem; margin: 0;
    font-weight: 300; letter-spacing: 0.04em; text-transform: uppercase;
}
.data-status {
    display:flex; align-items:center; gap:0.5rem;
    background:#eaf4ee; border:1px solid #86c49a; border-radius:8px;
    padding:0.6rem 1rem; font-size:0.82rem; color:#1a5c34; margin-bottom:1.2rem;
}
.data-status-err { background:#fef2f2; border:1px solid #f5a0a0; color:#991b1b; }
.section-label {
    font-family: 'EB Garamond', serif; font-size:1.35rem; font-weight:500;
    color:#0f2340; border-left:4px solid #c9a84c; padding-left:0.75rem;
    margin:1.5rem 0 0.9rem 0;
}
.sub-section {
    font-family: 'EB Garamond', serif; font-size:1.1rem; font-weight:500;
    color:#1a3a5c; border-left:3px solid #a8c0d6; padding-left:0.6rem;
    margin:1.2rem 0 0.6rem 0;
}
.metric-card {
    background:#f8f9fb; border:1px solid #dde3ec; border-radius:8px;
    padding:1rem 1.2rem; text-align:center; border-top:3px solid #0f2340;
}
.metric-card .metric-val {
    font-family:'EB Garamond',serif; font-size:1.7rem; font-weight:600;
    color:#0f2340; line-height:1.2;
}
.metric-card .metric-lab {
    font-size:0.73rem; color:#6b7a8d; text-transform:uppercase;
    letter-spacing:0.06em; margin-top:0.15rem;
}
.stTabs [data-baseweb="tab-list"] {
    gap:4px; background:#f0f3f7; border-radius:8px; padding:4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius:6px; font-family:'DM Sans',sans-serif; font-size:0.83rem;
    font-weight:500; color:#445566; letter-spacing:0.03em; padding:0.45rem 1.1rem;
}
.stTabs [aria-selected="true"] { background:#0f2340 !important; color:#f0e6cc !important; }
div[data-testid="stDataFrame"] { font-size:0.82rem; }
footer { display:none !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🌐 India – West Asia Trade Risk Dashboard</h1>
  <p>Sectoral exposure analysis &nbsp;|&nbsp; Conflict impact assessment &nbsp;|&nbsp; March 2026</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# DATA LOADING FROM DISK
# ─────────────────────────────────────────────────────────
@st.cache_data
def load_from_disk(filepath, label):
    df = pd.read_csv(filepath, dtype={"HS Code": str})
    df.columns = df.columns.str.strip()
    required = {"HS Code", "Commodity", "Country of Destination", "Month", "Value"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{label}: Missing columns -> {missing}")
    df["HS Code"]                = df["HS Code"].str.strip().str.zfill(8)
    df["Country of Destination"] = df["Country of Destination"].str.strip().str.upper()
    df["Commodity"]              = df["Commodity"].str.strip()
    df["Value"]                  = pd.to_numeric(df["Value"], errors="coerce").fillna(0)
    df["HSN2"]                   = df["HS Code"].str[:2]
    return df

errors = []
for path, label in [(IMPORT_FILE, "Import"), (EXPORT_FILE, "Export")]:
    if not os.path.exists(path):
        errors.append(f"{label} file not found: <code>{os.path.abspath(path)}</code>")

if errors:
    for err in errors:
        st.markdown(f'<div class="data-status data-status-err">⚠️ {err}</div>', unsafe_allow_html=True)
    st.info("Update **IMPORT_FILE** and **EXPORT_FILE** paths at the top of the script and restart.")
    st.stop()

try:
    imp = load_from_disk(IMPORT_FILE, "Import")
    exp = load_from_disk(EXPORT_FILE, "Export")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

st.markdown(
    f'<div class="data-status">✅ Data loaded — '
    f'<strong>Import:</strong> {len(imp):,} rows &nbsp;|&nbsp; '
    f'<strong>Export:</strong> {len(exp):,} rows &nbsp;|&nbsp; '
    f'<strong>Import path:</strong> {os.path.abspath(IMPORT_FILE)} &nbsp;|&nbsp; '
    f'<strong>Export path:</strong> {os.path.abspath(EXPORT_FILE)}'
    f'</div>', unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────
# SIDEBAR — THRESHOLDS
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Analysis Thresholds")

    st.markdown("**Tab 1 — Monthly Average (HS8 → HS2)**")
    t1_abs   = st.number_input("Avg monthly absolute (USD M)", value=10.0, step=1.0,  key="t1a",
                                help="Min total avg monthly value for an HS8 code (all countries)") * 1e6
    t1_share = st.number_input("WA share threshold (%)",       value=30.0, step=5.0,  key="t1s",
                                min_value=0.0, max_value=100.0,
                                help="WA share of avg monthly trade for an HS8 code")

    st.markdown("**Tab 2 — Annual HSN-2**")
    t2_annual = st.number_input("Annual value (USD B)",    value=1.5,   step=0.1,  key="t2a") * 1e9
    t2_wa     = st.number_input("WA annual value (USD M)", value=750.0, step=50.0, key="t2w") * 1e6

    st.markdown("**Tab 3 — Annual HSN-8 → HSN-2 Rollup**")
    t3_abs   = st.number_input("HS8 annual value (USD M)", value=10.0, step=1.0, key="t3a") * 1e6
    t3_share = st.number_input("HS8 WA share (%)",         value=50.0, step=5.0, key="t3s",
                                min_value=0.0, max_value=100.0)

    st.markdown("---")
    st.caption(f"📥 Import: `{IMPORT_FILE}`")
    st.caption(f"📤 Export: `{EXPORT_FILE}`")
    st.markdown("---")
    st.caption("**West Asia scope ({} countries):**\n{}".format(
        len(WEST_ASIA_COUNTRIES), "\n".join(f"• {c}" for c in WEST_ASIA_COUNTRIES)
    ))

# ─────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────
def fmt_usd(val, decimals=1):
    if abs(val) >= 1e9:  return f"${val/1e9:.{decimals}f}B"
    if abs(val) >= 1e6:  return f"${val/1e6:.{decimals}f}M"
    if abs(val) >= 1e3:  return f"${val/1e3:.{decimals}f}K"
    return f"${val:,.0f}"

def add_desc(df, code_col="HSN2"):
    df = df.copy()
    df.insert(1, "Sector Description", df[code_col].map(HSN2_DESC).fillna("—"))
    return df

def render_hs2_rollup_table(rollup_df, label):
    """Render the Tab 1 rollup table with two column groups:
      Group A — Flagged HS8 codes only (the codes that triggered the flag)
      Group B — Full HSN2 sector (all HS8 codes under the sector)
    Numeric columns kept as floats so column-header sorting works correctly.
    Display formatting applied via st.column_config, not string conversion.
    """
    if rollup_df.empty:
        st.warning(f"No sectors meet the current thresholds for **{label}**.")
        return
    disp = add_desc(rollup_df)
    out = disp[[
        "HSN2", "Sector Description", "Flagged_HS8_Count",
        "Flagged_HS8_Total_Value", "Flagged_HS8_WA_Value", "Flagged_HS8_WA_Share_Pct",
        "HSN2_Total_Avg_Monthly_Value", "HSN2_WA_Avg_Monthly_Value", "HSN2_WA_Share_Pct",
    ]].copy().reset_index(drop=True)

    # Convert value columns to USD Million
    for c in ["Flagged_HS8_Total_Value", "Flagged_HS8_WA_Value",
              "HSN2_Total_Avg_Monthly_Value", "HSN2_WA_Avg_Monthly_Value"]:
        out[c] = (out[c] / 1e6).round(2)

    col_cfg = {
        "HSN2":                          st.column_config.TextColumn("HSN2", width="small"),
        "Sector Description":            st.column_config.TextColumn("Sector Description", width="large"),
        "Flagged_HS8_Count":             st.column_config.NumberColumn("# Flagged HS8", format="%d", width="small"),
        "Flagged_HS8_Total_Value":       st.column_config.NumberColumn(
                                             "Flagged HS8 — Avg Monthly Value ($M)",
                                             format="%.2f", help="Sum of avg monthly value of flagged HS8 codes only"),
        "Flagged_HS8_WA_Value":          st.column_config.NumberColumn(
                                             "Flagged HS8 — WA Value ($M)",
                                             format="%.2f", help="WA portion of flagged HS8 codes only"),
        "Flagged_HS8_WA_Share_Pct":      st.column_config.NumberColumn(
                                             "Flagged HS8 — WA Share (%)",
                                             format="%.1f %%", help="WA% of flagged HS8 codes only"),
        "HSN2_Total_Avg_Monthly_Value":  st.column_config.NumberColumn(
                                             "Sector (All HS8) — Avg Monthly Value ($M)",
                                             format="%.2f", help="Total avg monthly value across ALL HS8 codes in this sector"),
        "HSN2_WA_Avg_Monthly_Value":     st.column_config.NumberColumn(
                                             "Sector (All HS8) — WA Value ($M)",
                                             format="%.2f", help="WA avg monthly value across ALL HS8 codes in this sector"),
        "HSN2_WA_Share_Pct":             st.column_config.NumberColumn(
                                             "Sector (All HS8) — WA Share (%)",
                                             format="%.1f %%", help="WA share of the full sector"),
    }

    st.caption("📌 All values in USD Million (USD M)")
    st.dataframe(out, use_container_width=True,
                 column_config=col_cfg,
                 height=min(60 + len(out)*38, 520))
    m1, m2, m3 = st.columns(3)
    m1.metric("HS2 Sectors affected",     len(rollup_df))
    m2.metric("Flagged HS8 codes",        int(rollup_df["Flagged_HS8_Count"].sum()))
    m3.metric("Sector WA exposure (all)", fmt_usd(rollup_df["HSN2_WA_Avg_Monthly_Value"].sum()))

def render_hs2_annual_table(result_df, total_col, wa_col, share_col, label):
    """Render standard annual HS2 result table. Numeric columns kept as floats for sortability."""
    if result_df.empty:
        st.warning(f"No sectors meet the current thresholds for **{label}**.")
        return
    disp = add_desc(result_df)
    out = disp[["HSN2", "Sector Description", total_col, wa_col, share_col]].copy().reset_index(drop=True)
    out[total_col] = (out[total_col] / 1e6).round(2)
    out[wa_col]    = (out[wa_col]    / 1e6).round(2)
    col_cfg = {
        "HSN2":            st.column_config.TextColumn("HSN2", width="small"),
        "Sector Description": st.column_config.TextColumn("Sector Description", width="large"),
        total_col:         st.column_config.NumberColumn("Annual Value ($M)",    format="%.2f"),
        wa_col:            st.column_config.NumberColumn("WA Annual Value ($M)", format="%.2f"),
        share_col:         st.column_config.NumberColumn("WA Share (%)",         format="%.1f %%"),
    }
    st.caption("📌 All values in USD Million (USD M)")
    st.dataframe(out, use_container_width=True, column_config=col_cfg,
                 height=min(60 + len(out)*38, 520))
    m1, m2, m3 = st.columns(3)
    m1.metric("Sectors flagged",    len(result_df))
    m2.metric("Total annual value", fmt_usd(result_df[total_col].sum()))
    m3.metric("Total WA exposure",  fmt_usd(result_df[wa_col].sum()))

# ─────────────────────────────────────────────────────────
# TOP SUMMARY METRICS
# ─────────────────────────────────────────────────────────
total_imp    = imp["Value"].sum()
total_exp    = exp["Value"].sum()
imp_wa_total = imp[imp["Country of Destination"].isin(WA_UPPER)]["Value"].sum()
exp_wa_total = exp[exp["Country of Destination"].isin(WA_UPPER)]["Value"].sum()

c1, c2, c3, c4 = st.columns(4)
for col, val, lab in [
    (c1, total_imp,    "Total Import Value"),
    (c2, total_exp,    "Total Export Value"),
    (c3, imp_wa_total, "WA Import Exposure"),
    (c4, exp_wa_total, "WA Export Exposure"),
]:
    col.markdown(f"""
    <div class="metric-card">
      <div class="metric-val">{fmt_usd(val)}</div>
      <div class="metric-lab">{lab}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("")

# ─────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📅  Monthly Average Analysis",
    "📊  Annual HSN-2 Sector Analysis",
    "🔬  Annual HSN-8 → HSN-2 Rollup",
])

# ════════════════════════════════════════════════════════
# TAB 1 — MONTHLY AVERAGE: HS8 identification → HS2 rollup
#
# Methodology:
#   Step 1. For each (HS Code, Country, Month) group → sum value.
#   Step 2. Average across months PER (HS Code, Country) — only months
#           in which that code had any trade are counted (natural mean).
#   Step 3. Sum averaged country values within each HS Code:
#             Total avg monthly value  = sum over all countries
#             WA avg monthly value     = sum over WA countries only
#   Step 4. WA share % = WA avg / Total avg × 100
#   Step 5. Flag HS8 codes where BOTH:
#             Total avg monthly value > absolute threshold
#             WA share % > share threshold
#   Step 6. Roll flagged HS8 codes up to 2-digit sector (HS2).
# ════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-label">Monthly Average Analysis — HS8 Risk Identification → HS2 Rollup</div>',
                unsafe_allow_html=True)
    st.caption(
        f"**Methodology:** Average monthly trade value is computed per (HS8 code, Country) "
        f"only over months where trade existed. HS8 codes are flagged where total avg monthly value "
        f"> **{fmt_usd(t1_abs)}** AND WA share > **{t1_share:.0f}%**. "
        f"Flagged codes are then aggregated to their 2-digit sector for the output table."
    )

    @st.cache_data
    def tab1_analyse(imp_hash, exp_hash, abs_thresh, share_thresh):
        results = {}
        for df, label in [(imp, "Import"), (exp, "Export")]:

            # ── Step 1+2: Average monthly value per (HS Code, Country) ────────
            # Group by HS Code × Country × Month → then take mean across months.
            # This naturally only averages months where data exists (no zero-padding).
            monthly = (
                df.groupby(["HS Code", "HSN2", "Commodity", "Country of Destination", "Month"],
                           as_index=False)["Value"].sum()
            )
            avg_by_country = (
                monthly.groupby(["HS Code", "HSN2", "Commodity", "Country of Destination"],
                                as_index=False)["Value"].mean()
                       .rename(columns={"Value": "Avg_Monthly_Value"})
            )

            # ── Step 3: Total avg monthly value per HS8 (all countries) ───────
            total_avg = (
                avg_by_country
                .groupby(["HS Code", "HSN2", "Commodity"], as_index=False)["Avg_Monthly_Value"]
                .sum()
                .rename(columns={"Avg_Monthly_Value": "Total_Avg_Monthly_Value"})
            )

            # ── Step 3: WA avg monthly value per HS8 ──────────────────────────
            wa_avg = (
                avg_by_country[avg_by_country["Country of Destination"].isin(WA_UPPER)]
                .groupby(["HS Code"], as_index=False)["Avg_Monthly_Value"]
                .sum()
                .rename(columns={"Avg_Monthly_Value": "WA_Avg_Monthly_Value"})
            )

            # ── Step 4: Merge and compute WA share ────────────────────────────
            hs8 = total_avg.merge(wa_avg, on="HS Code", how="left").fillna(0)
            hs8["WA_Share_Pct"] = (
                hs8["WA_Avg_Monthly_Value"] /
                hs8["Total_Avg_Monthly_Value"].replace(0, np.nan) * 100
            ).round(2).fillna(0)

            # ── Step 5: Flag ──────────────────────────────────────────────────
            hs8["Flag_High_Abs"]   = hs8["Total_Avg_Monthly_Value"] > abs_thresh
            hs8["Flag_High_Share"] = hs8["WA_Share_Pct"]            > share_thresh
            hs8["Flag_High_Risk"]  = hs8["Flag_High_Abs"] & hs8["Flag_High_Share"]
            hs8.sort_values("Total_Avg_Monthly_Value", ascending=False, inplace=True)

            # ── Step 6: Roll up flagged HS8 → HS2 ────────────────────────────
            # The output shows values for the ENTIRE 2-digit sector (all its HS8
            # codes), not just the flagged ones. Flagged codes only determine
            # which HSN2 sectors appear in the output list.
            flagged = hs8[hs8["Flag_High_Risk"]]
            if flagged.empty:
                rollup = pd.DataFrame(columns=[
                    "HSN2", "Flagged_HS8_Count",
                    "Flagged_HS8_Total_Value", "Flagged_HS8_WA_Value", "Flagged_HS8_WA_Share_Pct",
                    "HSN2_Total_Avg_Monthly_Value", "HSN2_WA_Avg_Monthly_Value", "HSN2_WA_Share_Pct",
                ])
            else:
                # Which HSN2 sectors contain at least one flagged HS8 code?
                flagged_hsn2 = flagged["HSN2"].unique()

                # A) Count + sum of FLAGGED HS8 codes only
                flagged_agg = (
                    flagged.groupby("HSN2", as_index=False)
                           .agg(
                               Flagged_HS8_Count=("HS Code", "count"),
                               Flagged_HS8_Total_Value=("Total_Avg_Monthly_Value", "sum"),
                               Flagged_HS8_WA_Value=("WA_Avg_Monthly_Value", "sum"),
                           )
                )
                flagged_agg["Flagged_HS8_WA_Share_Pct"] = (
                    flagged_agg["Flagged_HS8_WA_Value"] /
                    flagged_agg["Flagged_HS8_Total_Value"].replace(0, np.nan) * 100
                ).round(2).fillna(0)

                # B) Full sector totals across ALL HS8 codes under qualifying HSN2s
                hsn2_total = (
                    hs8[hs8["HSN2"].isin(flagged_hsn2)]
                    .groupby("HSN2", as_index=False)
                    .agg(
                        HSN2_Total_Avg_Monthly_Value=("Total_Avg_Monthly_Value", "sum"),
                        HSN2_WA_Avg_Monthly_Value=("WA_Avg_Monthly_Value", "sum"),
                    )
                )
                hsn2_total["HSN2_WA_Share_Pct"] = (
                    hsn2_total["HSN2_WA_Avg_Monthly_Value"] /
                    hsn2_total["HSN2_Total_Avg_Monthly_Value"].replace(0, np.nan) * 100
                ).round(2).fillna(0)

                # Merge both sets of columns together
                rollup = flagged_agg.merge(hsn2_total, on="HSN2", how="left")
                rollup.sort_values("HSN2_Total_Avg_Monthly_Value", ascending=False, inplace=True)

            results[label] = {
                "hs8": hs8,
                "hs8_flagged": flagged,
                "rollup": rollup,
            }
        return results

    r1 = tab1_analyse(len(imp), len(exp), t1_abs, t1_share)

    # ── Output: 2-digit rollup ─────────────────────────────────────────────
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("##### 🔴 Import — High-Risk Sectors (HS2 Rollup)")
        render_hs2_rollup_table(r1["Import"]["rollup"], "Import")
    with col_b:
        st.markdown("##### 🔵 Export — High-Risk Sectors (HS2 Rollup)")
        render_hs2_rollup_table(r1["Export"]["rollup"], "Export")

    # ── Expander: full HS8 flagged list ───────────────────────────────────
    with st.expander("📋 Flagged HS8 codes detail (all flagged codes underlying the rollup)"):
        for label in ["Import", "Export"]:
            flagged_df = r1[label]["hs8_flagged"].copy()
            st.markdown(f"**{label} — {len(flagged_df):,} HIGH RISK HS8 codes**")
            if flagged_df.empty:
                st.info("No flagged codes at current thresholds.")
            else:
                flagged_df["Sector Description"] = flagged_df["HSN2"].map(HSN2_DESC).fillna("—")
                disp = flagged_df[[
                    "HS Code", "HSN2", "Sector Description", "Commodity",
                    "Total_Avg_Monthly_Value", "WA_Avg_Monthly_Value", "WA_Share_Pct"
                ]].copy().reset_index(drop=True)
                disp["Total_Avg_Monthly_Value"] = (disp["Total_Avg_Monthly_Value"] / 1e6).round(2)
                disp["WA_Avg_Monthly_Value"]     = (disp["WA_Avg_Monthly_Value"]     / 1e6).round(2)
                st.caption("📌 All values in USD Million (USD M)")
                st.dataframe(disp, use_container_width=True, height=360,
                    column_config={
                        "HS Code":                  st.column_config.TextColumn("HS8 Code"),
                        "HSN2":                     st.column_config.TextColumn("HSN2", width="small"),
                        "Sector Description":       st.column_config.TextColumn("Sector"),
                        "Commodity":                st.column_config.TextColumn("Commodity"),
                        "Total_Avg_Monthly_Value":  st.column_config.NumberColumn("Avg Monthly Value ($M)",    format="%.2f"),
                        "WA_Avg_Monthly_Value":     st.column_config.NumberColumn("WA Avg Monthly Value ($M)", format="%.2f"),
                        "WA_Share_Pct":             st.column_config.NumberColumn("WA Share (%)",              format="%.1f %%"),
                    })

    # ── Expander: full HS8 universe ────────────────────────────────────────
    with st.expander("📋 Full HS8 monthly average summary (all codes)"):
        for label in ["Import", "Export"]:
            hs8_all = r1[label]["hs8"].copy()
            st.markdown(f"**{label} — {len(hs8_all):,} HS8 codes**")
            hs8_all["Sector Description"] = hs8_all["HSN2"].map(HSN2_DESC).fillna("—")
            disp = hs8_all[[
                "HS Code", "HSN2", "Sector Description", "Commodity",
                "Total_Avg_Monthly_Value", "WA_Avg_Monthly_Value", "WA_Share_Pct", "Flag_High_Risk"
            ]].copy().reset_index(drop=True)
            disp["Total_Avg_Monthly_Value"] = (disp["Total_Avg_Monthly_Value"] / 1e6).round(2)
            disp["WA_Avg_Monthly_Value"]     = (disp["WA_Avg_Monthly_Value"]     / 1e6).round(2)
            st.caption("📌 All values in USD Million (USD M)")
            st.dataframe(disp, use_container_width=True, height=360,
                column_config={
                    "HS Code":                  st.column_config.TextColumn("HS8 Code"),
                    "HSN2":                     st.column_config.TextColumn("HSN2", width="small"),
                    "Sector Description":       st.column_config.TextColumn("Sector"),
                    "Commodity":                st.column_config.TextColumn("Commodity"),
                    "Total_Avg_Monthly_Value":  st.column_config.NumberColumn("Avg Monthly Value ($M)",    format="%.2f"),
                    "WA_Avg_Monthly_Value":     st.column_config.NumberColumn("WA Avg Monthly Value ($M)", format="%.2f"),
                    "WA_Share_Pct":             st.column_config.NumberColumn("WA Share (%)",              format="%.1f %%"),
                    "Flag_High_Risk":           st.column_config.CheckboxColumn("High Risk"),
                })


# ════════════════════════════════════════════════════════
# TAB 2 — ANNUAL HSN-2
# ════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-label">Annual Trade Exposure — 2-Digit HSN Sector Level</div>',
                unsafe_allow_html=True)
    st.caption(
        f"Sectors flagged where **annual trade > {fmt_usd(t2_annual)}** "
        f"AND **WA annual trade > {fmt_usd(t2_wa)}** (both required)."
    )

    @st.cache_data
    def tab2_analyse(imp_hash, exp_hash, annual_thresh, wa_thresh):
        results = {}
        for df, label in [(imp, "Import"), (exp, "Export")]:
            total_col = f"Annual_{label}_Value"
            wa_col    = f"WA_Annual_{label}_Value"
            share_col = f"WA_{label}_Share_Pct"
            annual_total = df.groupby("HSN2", as_index=False)["Value"].sum().rename(columns={"Value": total_col})
            wa_df        = df[df["Country of Destination"].isin(WA_UPPER)]
            annual_wa    = wa_df.groupby("HSN2", as_index=False)["Value"].sum().rename(columns={"Value": wa_col})
            summary = (pd.DataFrame({"HSN2": sorted(annual_total["HSN2"].unique())})
                         .merge(annual_total, on="HSN2", how="left")
                         .merge(annual_wa,    on="HSN2", how="left")
                         .fillna(0))
            summary[share_col]          = (summary[wa_col] / summary[total_col].replace(0, np.nan) * 100).round(2).fillna(0)
            summary["Flag_High_Annual"] = summary[total_col] > annual_thresh
            summary["Flag_High_WA"]     = summary[wa_col]    > wa_thresh
            summary["Flag_Combined"]    = summary["Flag_High_Annual"] & summary["Flag_High_WA"]
            summary.sort_values(total_col, ascending=False, inplace=True)
            results[label] = {
                "summary": summary,
                "high_risk": summary[summary["Flag_Combined"]].copy(),
                "total_col": total_col, "wa_col": wa_col, "share_col": share_col,
            }
        return results

    r2 = tab2_analyse(len(imp), len(exp), t2_annual, t2_wa)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("##### 🔴 Import — High-Risk Sectors")
        render_hs2_annual_table(r2["Import"]["high_risk"],
                                r2["Import"]["total_col"], r2["Import"]["wa_col"], r2["Import"]["share_col"], "Import")
    with col_b:
        st.markdown("##### 🔵 Export — High-Risk Sectors")
        render_hs2_annual_table(r2["Export"]["high_risk"],
                                r2["Export"]["total_col"], r2["Export"]["wa_col"], r2["Export"]["share_col"], "Export")

    with st.expander("📋 Full annual HSN-2 summary — all sectors"):
        for label in ["Import", "Export"]:
            st.markdown(f"**{label}**")
            full = add_desc(r2[label]["summary"])
            tc = r2[label]["total_col"]; wc = r2[label]["wa_col"]; sc = r2[label]["share_col"]
            disp = full[["HSN2", "Sector Description", tc, wc, sc, "Flag_Combined"]].copy().reset_index(drop=True)
            disp[tc] = (disp[tc] / 1e6).round(2)
            disp[wc] = (disp[wc] / 1e6).round(2)
            st.caption("📌 All values in USD Million (USD M)")
            st.dataframe(disp, use_container_width=True, height=340,
                column_config={
                    "HSN2":            st.column_config.TextColumn("HSN2", width="small"),
                    "Sector Description": st.column_config.TextColumn("Sector Description", width="large"),
                    tc:                st.column_config.NumberColumn("Annual Value ($M)",    format="%.2f"),
                    wc:                st.column_config.NumberColumn("WA Annual Value ($M)", format="%.2f"),
                    sc:                st.column_config.NumberColumn("WA Share (%)",         format="%.1f %%"),
                    "Flag_Combined":   st.column_config.CheckboxColumn("High Risk"),
                })


# ════════════════════════════════════════════════════════
# TAB 3 — ANNUAL HSN-8 → HSN-2 ROLLUP
# ════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-label">Annual HS8 Risk Identification → 2-Digit Sector Rollup</div>',
                unsafe_allow_html=True)
    st.caption(
        f"**Step 1:** Flag 8-digit codes where annual value > **{fmt_usd(t3_abs)}** "
        f"AND WA share > **{t3_share:.0f}%** (both required).  "
        f"**Step 2:** Sum flagged codes at 2-digit sector level."
    )

    @st.cache_data
    def tab3_analyse(imp_hash, exp_hash, abs_thresh, share_thresh):
        results = {}
        for df, label in [(imp, "Import"), (exp, "Export")]:
            total_col = f"Annual_{label}_Value"
            wa_col    = f"WA_Annual_{label}_Value"
            share_col = f"WA_{label}_Share_Pct"
            hs8_total = (df.groupby(["HS Code", "HSN2", "Commodity"], as_index=False)["Value"]
                           .sum().rename(columns={"Value": total_col}))
            wa_df = df[df["Country of Destination"].isin(WA_UPPER)]
            hs8_wa = (wa_df.groupby("HS Code", as_index=False)["Value"]
                          .sum().rename(columns={"Value": wa_col}))
            hs8 = hs8_total.merge(hs8_wa, on="HS Code", how="left").fillna(0)
            hs8[share_col]         = (hs8[wa_col] / hs8[total_col].replace(0, np.nan) * 100).round(2).fillna(0)
            hs8["Flag_High_Value"] = hs8[total_col] > abs_thresh
            hs8["Flag_High_Share"] = hs8[share_col] > share_thresh
            hs8["Flag_High_Risk"]  = hs8["Flag_High_Value"] & hs8["Flag_High_Share"]
            hs8.sort_values(total_col, ascending=False, inplace=True)
            flagged = hs8[hs8["Flag_High_Risk"]]
            if flagged.empty:
                rollup = pd.DataFrame(columns=["HSN2", "Flagged_HS8_Count",
                                                f"Sum_{total_col}", f"Sum_{wa_col}",
                                                f"WA_Rollup_{label}_Share_Pct"])
            else:
                flagged_codes = flagged["HS Code"].unique()
                wa_flagged = (wa_df[wa_df["HS Code"].isin(flagged_codes)]
                              .groupby(["HS Code", "HSN2"], as_index=False)["Value"]
                              .sum().rename(columns={"Value": wa_col}))
                merged = flagged[["HS Code", "HSN2", total_col]].merge(
                    wa_flagged[["HS Code", wa_col]], on="HS Code", how="left"
                ).fillna(0)
                rollup = (merged.groupby("HSN2")
                                .agg(Flagged_HS8_Count=(total_col, "count"),
                                     **{f"Sum_{total_col}": (total_col, "sum"),
                                        f"Sum_{wa_col}":    (wa_col,    "sum")})
                                .reset_index())
                rollup[f"WA_Rollup_{label}_Share_Pct"] = (
                    rollup[f"Sum_{wa_col}"] / rollup[f"Sum_{total_col}"].replace(0, np.nan) * 100
                ).round(2).fillna(0)
                rollup.sort_values(f"Sum_{total_col}", ascending=False, inplace=True)
            results[label] = {
                "hs8": hs8, "hs8_flagged": flagged, "rollup": rollup,
                "total_col": total_col, "wa_col": wa_col, "share_col": share_col,
                "rtc": f"Sum_{total_col}", "rwc": f"Sum_{wa_col}",
                "rsc": f"WA_Rollup_{label}_Share_Pct",
            }
        return results

    r3 = tab3_analyse(len(imp), len(exp), t3_abs, t3_share)

    col_a, col_b = st.columns(2)
    for col, label, color in [(col_a, "Import", "🔴"), (col_b, "Export", "🔵")]:
        with col:
            st.markdown(f"##### {color} {label} — 2-Digit Rollup of Flagged HS8 Codes")
            rollup = r3[label]["rollup"]
            rtc = r3[label]["rtc"]; rwc = r3[label]["rwc"]; rsc = r3[label]["rsc"]
            if rollup.empty:
                st.warning("No HIGH RISK HS8 codes at current thresholds.")
            else:
                disp = add_desc(rollup)
                out = disp[["HSN2", "Sector Description", "Flagged_HS8_Count", rtc, rwc, rsc]].copy().reset_index(drop=True)
                out[rtc] = (out[rtc] / 1e6).round(2)
                out[rwc] = (out[rwc] / 1e6).round(2)
                st.caption("📌 All values in USD Million (USD M)")
                st.dataframe(out, use_container_width=True, height=min(60 + len(out)*38, 520),
                    column_config={
                        "HSN2":                    st.column_config.TextColumn("HSN2", width="small"),
                        "Sector Description":      st.column_config.TextColumn("Sector Description", width="large"),
                        "Flagged_HS8_Count":       st.column_config.NumberColumn("# Flagged HS8", format="%d", width="small"),
                        rtc:                       st.column_config.NumberColumn("Sum Annual Value ($M)",    format="%.2f"),
                        rwc:                       st.column_config.NumberColumn("Sum WA Value ($M)",        format="%.2f"),
                        rsc:                       st.column_config.NumberColumn("WA Share (%)",             format="%.1f %%"),
                    })
                m1, m2, m3 = st.columns(3)
                m1.metric("Sectors affected",  len(rollup))
                m2.metric("Flagged HS8 codes", int(rollup["Flagged_HS8_Count"].sum()))
                m3.metric("Total WA exposure", fmt_usd(rollup[rwc].sum()))

    with st.expander("📋 Full HIGH RISK HS8 code list"):
        for label in ["Import", "Export"]:
            flagged_df = r3[label]["hs8_flagged"].copy()
            tc = r3[label]["total_col"]; wc = r3[label]["wa_col"]; sc = r3[label]["share_col"]
            st.markdown(f"**{label} — {len(flagged_df):,} HIGH RISK HS8 codes**")
            if flagged_df.empty:
                st.info("No flagged codes at current thresholds.")
            else:
                flagged_df["Sector Description"] = flagged_df["HSN2"].map(HSN2_DESC).fillna("—")
                disp = flagged_df[["HS Code", "HSN2", "Sector Description", "Commodity", tc, wc, sc]].copy().reset_index(drop=True)
                disp[tc] = (disp[tc] / 1e6).round(2)
                disp[wc] = (disp[wc] / 1e6).round(2)
                st.caption("📌 All values in USD Million (USD M)")
                st.dataframe(disp, use_container_width=True, height=360,
                    column_config={
                        "HS Code":            st.column_config.TextColumn("HS8 Code"),
                        "HSN2":               st.column_config.TextColumn("HSN2", width="small"),
                        "Sector Description": st.column_config.TextColumn("Sector"),
                        "Commodity":          st.column_config.TextColumn("Commodity"),
                        tc:                   st.column_config.NumberColumn("Annual Value ($M)", format="%.2f"),
                        wc:                   st.column_config.NumberColumn("WA Value ($M)",     format="%.2f"),
                        sc:                   st.column_config.NumberColumn("WA Share (%)",      format="%.1f %%"),
                    })