import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Agro-Export Data Strategy",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── GLOBAL CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');

:root {
    --gd:   #1B4332;
    --gm:   #2D6A4F;
    --gl:   #52B788;
    --gold: #D4A017;
    --cream:#F8F4EC;
    --dark: #1C2B1E;
    --muted:#5A6E5C;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--cream);
    font-family: 'DM Sans', sans-serif;
    color: var(--dark);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--gd) !important;
    border-right: 4px solid var(--gold);
}
[data-testid="stSidebar"] * { color: #fff !important; }
[data-testid="stSidebar"] .stRadio > label { display: none; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px;
    padding: 6px 4px !important;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    display: block;
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15); }
header[data-testid="stHeader"] { display: none; }

/* Cards */
.card {
    background: #fff;
    border-radius: 14px;
    padding: 1.6rem 2rem;
    box-shadow: 0 3px 20px rgba(27,67,50,0.09);
    margin-bottom: 1rem;
    border-left: 5px solid var(--gl);
}
.card-gold  { border-left-color: var(--gold); }
.card-dark  { background: var(--gd); border-left-color: var(--gold); }
.card-dark p, .card-dark div, .card-dark strong, .card-dark li { color: #fff !important; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #0d2b1d 0%, var(--gd) 45%, var(--gm) 100%);
    border-radius: 18px;
    padding: 3.5rem 3rem;
    color: #fff;
    text-align: center;
    margin-bottom: 2rem;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    margin: 0 0 0.4rem;
    letter-spacing: -1.5px;
    line-height: 1.1;
}
.hero .sub { font-size: 1.1rem; font-weight: 300; opacity: 0.82; margin-bottom: 1.2rem; }
.hero .badge {
    display: inline-block;
    background: var(--gold);
    color: #1C2B1E;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 5px 16px;
    border-radius: 999px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin: 3px;
}

/* Section heading */
.sec-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.1rem;
    font-weight: 800;
    color: var(--gd);
    margin-bottom: 0.3rem;
    line-height: 1.15;
}
.sec-sub { color: var(--muted); font-size: 0.97rem; margin-bottom: 0.6rem; }
.gold-bar { width: 56px; height: 5px; background: var(--gold); border-radius: 4px; margin-bottom: 1.5rem; }

/* Big metric tiles */
.mtile {
    background: #fff;
    border-radius: 14px;
    padding: 1.8rem 1.2rem 1.4rem;
    text-align: center;
    box-shadow: 0 3px 18px rgba(27,67,50,0.09);
    border-top: 5px solid var(--gl);
}
.mtile.gold-top { border-top-color: var(--gold); }
.mtile .num {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    color: var(--gd);
    line-height: 1;
}
.mtile .lbl {
    font-size: 0.82rem;
    color: var(--muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    margin-top: 8px;
}
.mtile .change {
    font-size: 1rem;
    font-weight: 600;
    color: var(--gl);
    margin-top: 5px;
}

/* Dark data highlight boxes */
.dbox {
    background: var(--gd);
    color: #fff;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.dbox .dval {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    font-weight: 900;
    color: var(--gold);
    line-height: 1;
}
.dbox .dtitle { font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; opacity: 0.75; margin-bottom: 4px; }
.dbox .ddesc  { font-size: 0.9rem; opacity: 0.85; margin-top: 4px; line-height: 1.6; }

/* Progress bar */
.pbar-wrap { margin-bottom: 1.1rem; }
.pbar-label {
    display: flex; justify-content: space-between;
    font-size: 0.92rem; font-weight: 600; margin-bottom: 5px; color: var(--dark);
}
.pbar-track {
    background: rgba(27,67,50,0.1);
    border-radius: 999px;
    height: 20px;
    overflow: hidden;
}
.pbar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--gl) 0%, var(--gold) 100%);
}

/* Pill tags */
.pill {
    display: inline-block;
    background: rgba(82,183,136,0.13);
    color: var(--gm);
    border: 1.5px solid rgba(82,183,136,0.35);
    font-size: 0.85rem; font-weight: 600;
    padding: 6px 15px; border-radius: 999px; margin: 3px;
}
.pill-g {
    background: rgba(212,160,23,0.1);
    color: #7a5700;
    border-color: rgba(212,160,23,0.35);
}

/* Table overrides */
[data-testid="stDataFrame"] table { font-size: 1rem !important; }
[data-testid="stDataFrame"] thead th {
    background: var(--gd) !important;
    color: #fff !important;
    font-size: 0.97rem !important;
    font-weight: 700 !important;
    padding: 13px 18px !important;
}
[data-testid="stDataFrame"] tbody td {
    font-size: 1rem !important;
    padding: 11px 18px !important;
}
[data-testid="stDataFrame"] tbody tr:nth-child(even) td { background: rgba(82,183,136,0.06) !important; }

/* Footer */
.footer {
    background: var(--gd);
    color: rgba(255,255,255,0.65);
    padding: 1.1rem 2rem;
    border-radius: 12px;
    text-align: center;
    font-size: 0.84rem;
    margin-top: 2.5rem;
}

/* Tabs */
[data-testid="stTabs"] button {
    font-size: 1rem !important;
    font-weight: 600 !important;
    padding: 10px 22px !important;
}
</style>
""", unsafe_allow_html=True)


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1.2rem 0 0.6rem;'>
        <div style='font-size:2rem;'>🌿</div>
        <div style='font-family:Playfair Display,serif;font-size:1.1rem;font-weight:800;line-height:1.3;margin-top:6px;'>
            Agro-Export<br>Data Strategy
        </div>
        <div style='font-size:0.7rem;opacity:0.6;margin-top:5px;letter-spacing:1px;'>MAIN CAMPUS · GROUP 3</div>
    </div><hr/>
    """, unsafe_allow_html=True)

    sections = [
        "Overview",
        "Executive Summary",
        "Organizational Context",
        "Business Questions",
        "Analytics Maturity",
        "Target Data Vision",
        "Data Architecture",
        "Governance & Privacy",
        "Risks & Ethics",
        "KPIs & Impact",
        "Productivity, Quality & Traceability",
        "Thank You",
    ]
    selected = st.radio("nav", sections, label_visibility="collapsed")
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem;opacity:0.55;text-align:center;padding-bottom:1rem;line-height:1.8;'>
        18 March 2026<br>
        Abigail Ansah Amponsah · 11019225<br>
        Ekua Micah Abakah-Paintsil · 11012281<br>
        Nana Kane Bruce Eshun · 11117122
    </div>
    """, unsafe_allow_html=True)


def sec_title(text, sub=""):
    st.markdown(f"<div class='sec-title'>{text}</div>", unsafe_allow_html=True)
    if sub:
        st.markdown(f"<div class='sec-sub'>{sub}</div>", unsafe_allow_html=True)
    st.markdown("<div class='gold-bar'></div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if selected == "Overview":
    st.markdown("""
    <div class='hero'>
        <h1>Agro-Export Data Strategy</h1>
        <p class='sub'>Innovative Data Strategy for Sustainable Farming</p>
        <span class='badge'>Main Campus — Group 3</span>
        <span class='badge'>18 March 2026</span>
    </div>
    """, unsafe_allow_html=True)

    sec_title("Presented By")
    c1, c2, c3 = st.columns(3)
    for col, name, sid in zip([c1,c2,c3],
        ["Abigail Ansah Amponsah","Ekua Micah Abakah-Paintsil","Nana Kane Bruce Eshun"],
        ["11019225","11012281","11117122"]):
        col.markdown(f"""
        <div class='card' style='text-align:center;'>
            <div style='font-size:2.4rem;margin-bottom:8px;'>👤</div>
            <div style='font-family:Playfair Display,serif;font-size:1.15rem;font-weight:800;'>{name}</div>
            <div style='font-size:0.92rem;color:#5A6E5C;margin-top:6px;font-weight:600;'>{sid}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec_title("Strategy at a Glance", "Key numbers from the full 24-month data strategy")

    m1,m2,m3,m4 = st.columns(4)
    for col, num, lbl, change, gld in zip([m1,m2,m3,m4],
        ["3","18%→5%","28%→12%","15%→90%"],
        ["Export Crops","Export Rejection Rate","Post-Harvest Loss","Supply Chain Traceability"],
        ["Onions · Mangoes · Cashew","Target over 24 months","Target over 24 months","Target over 24 months"],
        [False, True, True, False]):
        cls = "mtile gold-top" if gld else "mtile"
        col.markdown(f"""
        <div class='{cls}'>
            <div class='num'>{num}</div>
            <div class='lbl'>{lbl}</div>
            <div class='change'>{change}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='card card-dark'>
        <div style='font-family:Playfair Display,serif;font-size:1.35rem;font-weight:800;color:#fff;margin-bottom:0.7rem;'>About This Strategy</div>
        <p style='font-size:1.05rem;line-height:1.9;color:#fff;'>
        This agro-export company competes in a demanding global market, supplying <strong>onions, mangoes,
        and cashew products</strong>. Challenges include yield variability, post-harvest losses, and export
        rejections driven by inconsistent quality and limited traceability. This strategy treats
        <strong>data as a core asset</strong> — boosting productivity, maintaining quality, strengthening
        farmer partnerships, and meeting international export regulations.
        </p>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 2 — EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "Executive Summary":
    sec_title("Executive Summary")

    st.markdown("""
    <div class='card' style='font-size:1.07rem;line-height:1.95;'>
    This agro-export company operates in a <strong>competitive global market</strong> supplying onions,
    mangoes, and cashew products. The company currently faces <strong>yield variability, post-harvest
    losses, and export rejections</strong> driven by inconsistent quality and limited traceability.<br><br>
    This strategy treats <strong>data as a valuable tool</strong> to boost productivity, maintain quality,
    strengthen farmer partnerships, and meet export regulations — focusing on
    <em>easy-to-use, flexible, and farmer-friendly</em> approaches that deliver clear results.
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec_title("Core Challenges — Current Numbers")

    c1,c2,c3 = st.columns(3)
    for col, val, lbl, desc in zip([c1,c2,c3],
        ["~18%","~28%","45%"],
        ["Shipments Rejected","Harvest Volume Lost","Farmer Compliance"],
        ["Of export shipments are currently rejected at their destination.",
         "Of total harvest volume is lost to post-harvest spoilage.",
         "Of farmers consistently meet export-grade quality standards."]):
        col.markdown(f"""
        <div class='dbox'>
            <div class='dtitle'>{lbl}</div>
            <div class='dval'>{val}</div>
            <div class='ddesc'>{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1b,c2b,c3b = st.columns(3)
    for col, ttl, desc in zip([c1b,c2b,c3b],
        ["Yield Variability","Post-Harvest Losses","Export Rejections"],
        ["Inconsistent crop output across farms due to climate, soil, and agronomic variance.",
         "Up to 28% of harvest volume is lost before reaching export markets.",
         "~18% of shipments are rejected due to quality gaps and poor traceability."]):
        col.markdown(f"""
        <div class='card' style='text-align:center;'>
            <div style='font-family:Playfair Display,serif;font-size:1.15rem;font-weight:800;color:#1B4332;margin-bottom:10px;'>{ttl}</div>
            <div style='font-size:0.97rem;color:#5A6E5C;line-height:1.75;'>{desc}</div>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 3 — ORGANIZATIONAL CONTEXT
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "Organizational Context":
    sec_title("Organizational Context & Strategic Objective")

    st.markdown("""
    <div class='card card-gold' style='font-size:1.05rem;line-height:1.88;'>
    <strong style='font-size:1.15rem;font-family:Playfair Display,serif;'>Industry & Competitive Landscape</strong><br><br>
    The agro-export industry is <strong>highly competitive</strong> and sensitive to climate variability,
    quality regulations, and global market demand. Exporters must meet <strong>strict international food
    safety, traceability, and quality standards</strong> while operating under tight profit margins.
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:1.35rem;font-weight:800;color:#1B4332;margin-bottom:1rem;'>Core Business Goals</div>", unsafe_allow_html=True)

    goals = [
        ("01","Yield Consistency","Improve crop yield consistency across onions, mangoes, and cashew farms."),
        ("02","Reduce Losses","Reduce post-harvest losses and storage spoilage."),
        ("03","Export Acceptance","Increase export acceptance rates by improving quality standards."),
        ("04","Traceability","Strengthen supply chain traceability and compliance with regulations."),
        ("05","Farmer Productivity","Improve farmer productivity and cost efficiency."),
    ]
    c1, c2 = st.columns(2)
    for i, (num, ttl, desc) in enumerate(goals):
        col = c1 if i % 2 == 0 else c2
        col.markdown(f"""
        <div class='card' style='display:flex;align-items:flex-start;gap:1.2rem;padding:1.2rem 1.5rem;'>
            <div style='font-family:Playfair Display,serif;font-size:2.2rem;font-weight:900;color:#D4A017;line-height:1;min-width:44px;'>{num}</div>
            <div>
                <div style='font-weight:700;font-size:1.07rem;margin-bottom:4px;'>{ttl}</div>
                <div style='font-size:0.95rem;color:#5A6E5C;line-height:1.65;'>{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='card card-dark'>
        <div style='font-family:Playfair Display,serif;font-size:1.3rem;font-weight:800;color:#fff;margin-bottom:0.7rem;'>Key Strategic Vision</div>
        <p style='font-size:1.07rem;line-height:1.95;color:#fff;'>
        To transform the company into a <strong>data-driven agro-export enterprise</strong> where data
        supports decision-making across production, quality control, logistics, and export operations —
        while maintaining strong farmer partnerships.
        </p>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 4 — BUSINESS QUESTIONS
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "Business Questions":
    sec_title("Business Questions the Strategy Must Answer")

    c1, c2 = st.columns(2)
    c1.markdown("<div style='font-family:Playfair Display,serif;font-size:1.25rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>Critical Decisions Currently Made Poorly</div>", unsafe_allow_html=True)
    for q in [
        "Which farms and regions produce the highest quality crops?",
        "When should farmers plant and harvest to maximize yield?",
        "Which farmer produce consistently meet export quality requirements?",
        "Which storage conditions reduce spoilage?",
    ]:
        c1.markdown(f"""
        <div class='card' style='padding:1.1rem 1.4rem;margin-bottom:0.7rem;font-size:1rem;font-weight:500;'>
            <span style='color:#D4A017;font-weight:900;margin-right:10px;font-size:1.2rem;'>?</span>{q}
        </div>""", unsafe_allow_html=True)

    c2.markdown("<div style='font-family:Playfair Display,serif;font-size:1.25rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>Strategic & Operational Questions</div>", unsafe_allow_html=True)
    for q in [
        "Which crops and markets provide the highest long-term profitability?",
        "How can supply be stabilized despite climate variability?",
        "Which farms require pest or irrigation intervention?",
        "Which storage facilities require monitoring?",
        "Which shipments risk export rejection?",
    ]:
        c2.markdown(f"""
        <div class='card card-gold' style='padding:1.1rem 1.4rem;margin-bottom:0.7rem;font-size:1rem;font-weight:500;'>
            <span style='color:#2D6A4F;font-weight:900;margin-right:10px;'>→</span>{q}
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:1.3rem;font-weight:800;color:#1B4332;margin-bottom:1rem;'>Short-Term vs Long-Term Information Needs</div>", unsafe_allow_html=True)
    d1, d2 = st.columns(2)
    d1.markdown("""
    <div class='card' style='border-top:5px solid #52B788;border-left:none;padding:1.5rem 1.8rem;'>
        <div style='font-family:Playfair Display,serif;font-weight:800;font-size:1.15rem;color:#2D6A4F;margin-bottom:0.9rem;'>Short-Term Needs</div>
        <ul style='font-size:1rem;line-height:2.2;margin:0;padding-left:1.3rem;color:#1C2B1E;'>
            <li>Which farms are currently experiencing pest or disease outbreaks?</li>
            <li>Which storage locations are at risk of spoilage?</li>
            <li>Does each shipment meet Ghanaian and international export standards?</li>
        </ul>
    </div>""", unsafe_allow_html=True)
    d2.markdown("""
    <div class='card card-gold' style='border-top:5px solid #D4A017;border-left:none;padding:1.5rem 1.8rem;'>
        <div style='font-family:Playfair Display,serif;font-weight:800;font-size:1.15rem;color:#7a5700;margin-bottom:0.9rem;'>Long-Term Needs</div>
        <ul style='font-size:1rem;line-height:2.2;margin:0;padding-left:1.3rem;color:#1C2B1E;'>
            <li>What yield levels can we expect next season?</li>
            <li>Which farming regions are most vulnerable to drought or excessive rainfall?</li>
            <li>Which farmers consistently produce high-quality crops?</li>
        </ul>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 5 — ANALYTICS MATURITY
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "Analytics Maturity":
    sec_title("Current Data & Analytics Maturity Assessment")

    levels = ["Descriptive","Diagnostic","Predictive","Prescriptive"]
    colors = ["#1B4332","rgba(45,106,79,0.5)","rgba(82,183,136,0.25)","rgba(82,183,136,0.1)"]
    labels = ["CURRENT LEVEL","Next Step","Goal","Ultimate Goal"]
    mcols = st.columns(4)
    for col, lvl, clr, lbl in zip(mcols, levels, colors, labels):
        border = "3px solid #D4A017" if lbl == "CURRENT LEVEL" else "2px solid rgba(82,183,136,0.3)"
        text_color = "#fff" if lbl == "CURRENT LEVEL" else "#1B4332"
        col.markdown(f"""
        <div style='background:{clr};border:{border};border-radius:12px;padding:1.5rem 1rem;text-align:center;margin-bottom:1rem;'>
            <div style='font-size:0.72rem;font-weight:700;letter-spacing:1px;color:#D4A017;margin-bottom:8px;'>{lbl}</div>
            <div style='font-family:Playfair Display,serif;font-size:1.4rem;font-weight:800;color:{text_color};'>{lvl}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class='dbox' style='font-size:1.05rem;'>
        <div class='dtitle'>Current Maturity Level</div>
        <div class='dval'>Descriptive Analytics</div>
        <div class='ddesc'>Can report historical results but <strong>lacks diagnostic and predictive capabilities</strong>.
        Target: progress through Diagnostic → Predictive → Prescriptive Analytics over 24 months.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    c1.markdown("<div style='font-family:Playfair Display,serif;font-size:1.25rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>Data Sources</div>", unsafe_allow_html=True)
    c1.markdown("""
    <div class='card'>
        <div style='font-weight:700;font-size:1rem;color:#2D6A4F;margin-bottom:10px;'>Internal Sources</div>
        <span class='pill'>Manual farm records</span>
        <span class='pill'>Export shipment data</span>
        <span class='pill'>Storage & inventory logs</span>
        <span class='pill'>Quality inspection reports</span>
        <div style='font-weight:700;font-size:1rem;color:#2D6A4F;margin:16px 0 10px;'>External Sources</div>
        <span class='pill pill-g'>Weather & climate data</span>
        <span class='pill pill-g'>Soil testing reports</span>
        <span class='pill pill-g'>Export regulatory standards</span>
        <span class='pill pill-g'>Market price trends</span>
    </div>""", unsafe_allow_html=True)

    c2.markdown("<div style='font-family:Playfair Display,serif;font-size:1.25rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>Data Quality Issues</div>", unsafe_allow_html=True)
    for issue in [
        "Incomplete and inconsistent farmer data",
        "Lack of standardised data collection",
        "Delayed reporting across the supply chain",
        "Limited traceability across the supply chain",
    ]:
        c2.markdown(f"""
        <div class='card' style='padding:1rem 1.4rem;margin-bottom:0.7rem;border-left-color:#e05252;font-size:1rem;font-weight:500;'>
            <span style='color:#e05252;font-weight:900;margin-right:10px;'>✕</span>{issue}
        </div>""", unsafe_allow_html=True)

    c2.markdown("<div style='font-family:Playfair Display,serif;font-size:1.15rem;font-weight:800;color:#1B4332;margin:1.2rem 0 0.7rem;'>Existing Tools & Skills</div>", unsafe_allow_html=True)
    for tool in ["Manual documentation","Basic operational reporting","Limited use of weather or soil data","Heavy reliance on farmer experience & intuition"]:
        c2.markdown(f"<span class='pill' style='font-size:0.88rem;margin:4px;'>{tool}</span>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 6 — TARGET DATA VISION
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "Target Data Vision":
    sec_title("Target Data Vision", "What the organisation looks like when fully data-driven")

    st.markdown("""
    <div class='card card-dark'>
        <div style='font-family:Playfair Display,serif;font-size:1.3rem;font-weight:800;color:#fff;margin-bottom:0.9rem;'>What "Data-Driven" Means for This Organisation</div>
        <div style='display:flex;flex-wrap:wrap;gap:0.8rem;'>
            <span style='background:rgba(255,255,255,0.14);color:#fff;padding:9px 20px;border-radius:999px;font-size:0.95rem;font-weight:500;'>Farmers use real-time insights</span>
            <span style='background:rgba(255,255,255,0.14);color:#fff;padding:9px 20px;border-radius:999px;font-size:0.95rem;font-weight:500;'>Risks predicted before losses occur</span>
            <span style='background:rgba(255,255,255,0.14);color:#fff;padding:9px 20px;border-radius:999px;font-size:0.95rem;font-weight:500;'>Automatic export compliance monitoring</span>
            <span style='background:rgba(255,255,255,0.14);color:#fff;padding:9px 20px;border-radius:999px;font-size:0.95rem;font-weight:500;'>Full farm-to-export traceability</span>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 6 prominent data boxes
    r1c1, r1c2, r1c3 = st.columns(3)
    r2c1, r2c2, r2c3 = st.columns(3)
    data_pairs = [
        (r1c1,"Export Rejection","18% → 5%","From 18% baseline to ≤5% within 24 months"),
        (r1c2,"Post-Harvest Loss","28% → 12%","From 28% baseline to ≤12% within 24 months"),
        (r1c3,"Traceability","15% → 90%","From 15% to 90% full farm-to-export traceability"),
        (r2c1,"Onion Yield","5 → 12 MT/ha","From 5 MT/ha to 12 MT/ha over 24 months"),
        (r2c2,"Farmer Compliance","45% → 86%","From 45% to 86% meeting export-grade standards"),
        (r2c3,"Mango Yield","4.5 → 9 MT/ha","From 4.5 MT/ha to 9 MT/ha over 24 months"),
    ]
    for col, lbl, val, desc in data_pairs:
        col.markdown(f"""
        <div class='dbox'>
            <div class='dtitle'>{lbl}</div>
            <div class='dval'>{val}</div>
            <div class='ddesc'>{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:1.3rem;font-weight:800;color:#1B4332;margin-bottom:1rem;'>Full Success Metrics Table</div>", unsafe_allow_html=True)
    df_t = pd.DataFrame({
        "Metric": [
            "Export Rejection Rate",
            "Post-Harvest Loss (% of volume)",
            "Onion Yield (MT/ha)",
            "Mango Yield (MT/ha)",
            "Cashew Yield (MT/ha)",
            "Farmer Quality Compliance",
            "Supply Chain Traceability",
        ],
        "Current Baseline": ["~18%","~28%","5 MT/ha","4.5 MT/ha","0.60 MT/ha","45%","15%"],
        "12-Month Target":  ["≤10%","≤20%","9.5 MT/ha","5.5 MT/ha","0.72 MT/ha","65%","55%"],
        "24-Month Target":  ["≤5%","≤12%","12 MT/ha","9 MT/ha","2 MT/ha","86%","90%"],
    })
    st.dataframe(df_t, use_container_width=True, hide_index=True, height=320)

    st.markdown("<br>", unsafe_allow_html=True)
    fig = go.Figure()
    crops = ["Onions","Mangoes","Cashew"]
    for vals, name, color in zip(
        [[5,4.5,0.60],[9.5,5.5,0.72],[12,9,2.0]],
        ["Baseline","12-Month Target","24-Month Target"],
        ["#5A6E5C","#52B788","#D4A017"]
    ):
        fig.add_trace(go.Bar(name=name, x=crops, y=vals, marker_color=color,
                             text=[f"{v} MT/ha" for v in vals], textposition="outside",
                             textfont=dict(size=14, family="DM Sans")))
    fig.update_layout(
        barmode="group",
        title=dict(text="Crop Yield Targets (MT/ha) — Baseline vs 12 & 24-Month",
                   font=dict(size=18, family="Playfair Display")),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=1.12, font=dict(size=13)),
        height=400, margin=dict(t=65,b=20,l=20,r=20),
        font=dict(family="DM Sans", size=13),
        yaxis=dict(gridcolor="rgba(0,0,0,0.05)", title=dict(text="MT / Hectare", font=dict(size=13))),
        xaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 7 — DATA ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "Data Architecture":
    sec_title("Data Architecture & Technology Stack (Conceptual)")

    c1, c2 = st.columns(2)
    c1.markdown("<div style='font-family:Playfair Display,serif;font-size:1.25rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>Data Ingestion Sources</div>", unsafe_allow_html=True)
    for num, tool, desc in [
        ("01","Open Data Kit / Kobo Toolbox","Mobile farm data collection apps"),
        ("02","Farmonaut","Weather & satellite crop monitoring"),
        ("03","AgriXP","Farm management / data collection platform"),
        ("04","Odoo Inventory","Export and logistics systems"),
    ]:
        c1.markdown(f"""
        <div class='card' style='display:flex;align-items:flex-start;gap:1rem;padding:1.2rem 1.5rem;margin-bottom:0.7rem;'>
            <div style='font-family:Playfair Display,serif;font-size:1.8rem;font-weight:900;color:#D4A017;line-height:1;min-width:38px;'>{num}</div>
            <div>
                <div style='font-weight:700;font-size:1.05rem;margin-bottom:3px;'>{tool}</div>
                <div style='font-size:0.92rem;color:#5A6E5C;'>{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    c2.markdown("<div style='font-family:Playfair Display,serif;font-size:1.25rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>Storage Solutions</div>", unsafe_allow_html=True)
    for ltr, tool, desc in [
        ("A","Computer & External Devices","Backup and secure local storage"),
        ("B","MySQL / PostgreSQL","Cloud-based relational database"),
        ("C","Google Sheets & Google Drive","Lightweight collaborative storage & backup"),
    ]:
        c2.markdown(f"""
        <div class='card card-gold' style='display:flex;align-items:flex-start;gap:1rem;padding:1.2rem 1.5rem;margin-bottom:0.7rem;'>
            <div style='font-family:Playfair Display,serif;font-size:1.8rem;font-weight:900;color:#D4A017;line-height:1;min-width:28px;'>{ltr}</div>
            <div>
                <div style='font-weight:700;font-size:1.05rem;margin-bottom:3px;'>{tool}</div>
                <div style='font-size:0.92rem;color:#5A6E5C;'>{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    c2.markdown("<div style='font-family:Playfair Display,serif;font-size:1.15rem;font-weight:800;color:#1B4332;margin:1rem 0 0.7rem;'>Integration Considerations</div>", unsafe_allow_html=True)
    for pt in [
        "Integration between farm operations, quality inspection, and logistics data.",
        "Real-time synchronisation between farmer mobile apps and central systems.",
        "Compatibility with export certification systems.",
    ]:
        c2.markdown(f"""
        <div class='card' style='padding:0.9rem 1.3rem;margin-bottom:0.5rem;font-size:0.97rem;font-weight:500;border-left-color:#D4A017;'>
            <span style='color:#D4A017;font-weight:900;margin-right:8px;'>→</span>{pt}
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:1.25rem;font-weight:800;color:#1B4332;margin-bottom:1rem;'>Data Flow — Conceptual Architecture</div>", unsafe_allow_html=True)
    fig = go.Figure()
    for name, sub, y, color in [
        ("Ingestion Layer","Mobile Apps · Satellite · Farm Platforms · Logistics",0.88,"#1B4332"),
        ("Integration Layer","API Connectors · Real-Time Sync · Data Validation",0.64,"#2D6A4F"),
        ("Storage Layer","MySQL/PostgreSQL · Google Drive · Local Backup",0.42,"#52B788"),
        ("Analytics Layer","Dashboards · Reports · Predictive Models",0.20,"#D4A017"),
    ]:
        fig.add_shape(type="rect",x0=0.05,y0=y-0.09,x1=0.95,y1=y+0.09,
                      fillcolor=color,line_color=color,opacity=0.95)
        fig.add_annotation(x=0.5,y=y+0.025,text=f"<b>{name}</b>",showarrow=False,
                           font=dict(color="white",size=16,family="DM Sans"))
        fig.add_annotation(x=0.5,y=y-0.038,text=sub,showarrow=False,
                           font=dict(color="rgba(255,255,255,0.78)",size=12,family="DM Sans"))
    for y in [0.79,0.55,0.31]:
        fig.add_annotation(x=0.5,y=y,text="▼",showarrow=False,
                           font=dict(color="#D4A017",size=24))
    fig.update_layout(
        height=430,margin=dict(t=10,b=10,l=10,r=10),
        xaxis=dict(visible=False,range=[0,1]),
        yaxis=dict(visible=False,range=[0,1]),
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig,use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 8 — GOVERNANCE & PRIVACY
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "Governance & Privacy":
    sec_title("Data Governance & Privacy Regulations")

    c1, c2 = st.columns(2)
    c1.markdown("<div style='font-family:Playfair Display,serif;font-size:1.25rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>Data Ownership & Stewardship</div>", unsafe_allow_html=True)
    for num, owner, data in [
        ("01","Farmers","Own all farm production data"),
        ("02","Operations Team","Owns logistics and shipment data"),
        ("03","Quality Control Team","Owns inspection and grading data"),
        ("04","Management","Oversees governance policy and data strategy"),
    ]:
        c1.markdown(f"""
        <div class='card' style='display:flex;align-items:flex-start;gap:1.2rem;padding:1.2rem 1.5rem;margin-bottom:0.7rem;'>
            <div style='font-family:Playfair Display,serif;font-size:2rem;font-weight:900;color:#D4A017;line-height:1;min-width:40px;'>{num}</div>
            <div>
                <div style='font-weight:800;font-size:1.08rem;margin-bottom:3px;'>{owner}</div>
                <div style='font-size:0.95rem;color:#5A6E5C;'>{data}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    c2.markdown("<div style='font-family:Playfair Display,serif;font-size:1.25rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>Privacy & Regulatory Concerns</div>", unsafe_allow_html=True)
    for concern in [
        "Protection of farmer personal data",
        "Compliance with international food safety standards",
        "Secure handling of export documentation",
    ]:
        c2.markdown(f"""
        <div class='dbox' style='padding:1.3rem 1.5rem;margin-bottom:0.8rem;'>
            <div style='font-size:1.05rem;font-weight:600;color:#fff;'>{concern}</div>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 9 — RISKS & ETHICS
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "Risks & Ethics":
    sec_title("Risks & Ethics")

    c1, c2 = st.columns(2)
    c1.markdown("<div style='font-family:Playfair Display,serif;font-size:1.25rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>Ethical Considerations</div>", unsafe_allow_html=True)
    for eth_title, eth_desc in [
        ("Fair use of farmer data","Data collected from farmers must never be exploited or used against their interests."),
        ("Transparency in evaluations","All performance evaluations must be open, explainable, and accessible to those evaluated."),
        ("Support, not penalise","Analytics should empower and support farmers — not be used as a punitive measure."),
    ]:
        c1.markdown(f"""
        <div class='card card-gold' style='padding:1.2rem 1.5rem;margin-bottom:0.8rem;'>
            <div style='font-weight:800;font-size:1.05rem;margin-bottom:5px;'>{eth_title}</div>
            <div style='font-size:0.95rem;color:#5A6E5C;line-height:1.65;'>{eth_desc}</div>
        </div>""", unsafe_allow_html=True)

    c2.markdown("<div style='font-family:Playfair Display,serif;font-size:1.25rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>Risk Mitigation Strategies</div>", unsafe_allow_html=True)
    for r_title, r_desc in [
        ("Training","Training farmers and staff in digital data collection."),
        ("Validation","Standardised data validation — correct format, realistic limits, no missing values, no duplicates."),
        ("3-2-1 Backup","3 copies of data · 2 different media types · 1 off-site copy (Google Drive)."),
        ("Cybersecurity","Strong passwords, access controls, and secure system architecture."),
        ("Offline Tools","Offline data capture tools for rural and low-connectivity areas."),
    ]:
        c2.markdown(f"""
        <div class='card' style='padding:1rem 1.4rem;margin-bottom:0.6rem;'>
            <div style='font-weight:800;font-size:1.05rem;color:#1B4332;margin-bottom:3px;'>{r_title}</div>
            <div style='font-size:0.93rem;color:#5A6E5C;line-height:1.65;'>{r_desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Playfair Display,serif;font-size:1.3rem;font-weight:800;color:#1B4332;margin-bottom:1rem;'>The 3-2-1 Backup Rule</div>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    for col, num, lbl, desc in zip([b1,b2,b3],
        ["3","2","1"],
        ["Copies of Your Data","Different Media Types","Off-Site Copy"],
        ["Always maintain at least 3 separate copies of all data.",
         "Store on 2 different media (e.g. computer + external drive).",
         "Keep 1 copy off-site — cloud storage such as Google Drive."]):
        col.markdown(f"""
        <div class='dbox' style='text-align:center;'>
            <div class='dval' style='font-size:4.5rem;'>{num}</div>
            <div class='dtitle' style='font-size:0.92rem;margin-top:8px;'>{lbl}</div>
            <div class='ddesc' style='font-size:0.92rem;margin-top:6px;'>{desc}</div>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 10 — KPIs & IMPACT
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "KPIs & Impact":
    sec_title("Measuring Success & Strategic Impact")

    tab1, tab2, tab3 = st.tabs(["  Data Maturity KPIs  ","  Business Impact Metrics  ","  Review Mechanisms  "])

    with tab1:
        df_kpi = pd.DataFrame({
            "KPI": [
                "% Farm Operations Digitised",
                "Data Accuracy & Completeness Rate",
                "Farmers Actively Using Data Tools",
                "Dashboards / Reports Deployed",
                "Time to Generate Operational Report",
            ],
            "Current Baseline": ["12%","38%","0 farmers","0 dashboards","3–5 days (manual)"],
            "12-Month Target":  ["60%","75%","120 farmers","4 dashboards","< 4 hours"],
            "24-Month Target":  ["95%","92%","350+ farmers","10+ dashboards","Near real-time"],
        })
        st.dataframe(df_kpi, use_container_width=True, hide_index=True, height=260)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div style='font-family:Playfair Display,serif;font-size:1.25rem;font-weight:800;color:#1B4332;margin-bottom:1rem;'>Progress Towards Key Targets</div>", unsafe_allow_html=True)
        for lbl, base, t12, t24 in [
            ("Farm Operations Digitised", 12, 60, 95),
            ("Data Accuracy & Completeness", 38, 75, 92),
            ("Farmer Adoption (% of 350 target)", 0, 34, 100),
        ]:
            st.markdown(f"<div style='font-weight:700;font-size:1.05rem;margin-bottom:5px;'>{lbl} <span style=\"color:#5A6E5C;font-weight:400;font-size:0.9rem;\">— Baseline: {base}%</span></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='pbar-wrap'>
                <div class='pbar-label'><span>12-Month Target</span><span>{t12}%</span></div>
                <div class='pbar-track'><div class='pbar-fill' style='width:{t12}%;'></div></div>
                <div class='pbar-label' style='margin-top:8px;'><span>24-Month Target</span><span>{t24}%</span></div>
                <div class='pbar-track'><div class='pbar-fill' style='width:{t24}%;'></div></div>
            </div><br>""", unsafe_allow_html=True)

    with tab2:
        df_biz = pd.DataFrame({
            "Business Metric": [
                "Post-Harvest Loss (% of harvest)",
                "Export Acceptance Rate",
                "Crop Yield Consistency (variation)",
                "Operational Cost per MT Exported",
                "Farmer Average Income Increase",
            ],
            "Current Baseline": ["28%","82%","34% variation","GHS 1,850/MT","Baseline (N/A)"],
            "12-Month Target":  ["20% (save ~GHS 90K/season)","90%","22% variation","GHS 1,600/MT","+8% vs baseline"],
            "24-Month Target":  ["12% (save ~GHS 180K/season)","95%","12% variation","GHS 1,350/MT","+18% vs baseline"],
        })
        st.dataframe(df_biz, use_container_width=True, hide_index=True, height=250)

        st.markdown("<br>", unsafe_allow_html=True)
        h1,h2,h3,h4 = st.columns(4)
        for col, val, lbl, desc in zip([h1,h2,h3,h4],
            ["GHS 90K","GHS 180K","82%→95%","GHS 500/MT"],
            ["Savings at 12 Months","Savings at 24 Months","Export Acceptance","Cost Reduction / MT"],
            ["Per season at 20% loss","Per season at 12% loss","Shipment acceptance rate","GHS 1,850 → GHS 1,350"]):
            col.markdown(f"""
            <div class='dbox' style='text-align:center;'>
                <div class='dtitle'>{lbl}</div>
                <div class='dval' style='font-size:2rem;'>{val}</div>
                <div class='ddesc'>{desc}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        fc1, fc2 = st.columns(2)
        with fc1:
            fig = go.Figure(go.Bar(
                x=["Baseline\n(28% loss)","12-Month\n(20% loss)","24-Month\n(12% loss)"],
                y=[0,90000,180000],
                marker_color=["#5A6E5C","#52B788","#D4A017"],
                text=["GHS 0","GHS 90,000","GHS 180,000"],
                textposition="outside",
                textfont=dict(size=13,family="DM Sans"),
                width=0.5
            ))
            fig.update_layout(
                title=dict(text="Post-Harvest Savings (GHS/Season)",font=dict(size=15,family="Playfair Display")),
                paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                height=380,margin=dict(t=55,b=20,l=20,r=20),
                font=dict(family="DM Sans",size=12),
                yaxis=dict(gridcolor="rgba(0,0,0,0.05)",title="GHS",tickformat=","),
                xaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig,use_container_width=True)

        with fc2:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=["Baseline","12-Month","24-Month"],
                y=[82,90,95],
                mode="lines+markers+text",
                line=dict(color="#52B788",width=4),
                marker=dict(size=16,color="#1B4332",line=dict(color="#D4A017",width=3)),
                text=["82%","90%","95%"],
                textposition="top center",
                textfont=dict(size=15,family="DM Sans",color="#1C2B1E"),
            ))
            fig2.update_layout(
                title=dict(text="Export Acceptance Rate (%)",font=dict(size=15,family="Playfair Display")),
                paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                height=380,margin=dict(t=55,b=20,l=20,r=20),
                font=dict(family="DM Sans",size=12),
                yaxis=dict(range=[75,100],gridcolor="rgba(0,0,0,0.05)",title="%"),
                xaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig2,use_container_width=True)

    with tab3:
        st.markdown("<div style='font-family:Playfair Display,serif;font-size:1.25rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>Review & Feedback Mechanisms</div>", unsafe_allow_html=True)
        for num, mech, desc in [
            ("01","Quarterly Strategy Review Meetings","Senior leadership reviews progress against all KPIs every quarter."),
            ("02","Farmer Feedback Sessions","Regular sessions to gather on-the-ground input from farmers on data tools."),
            ("03","Performance Monitoring Dashboards","Live dashboards tracking yield, quality, and traceability metrics."),
            ("04","Continuous Improvement Programs","Ongoing cycles to refine data collection, tools, and processes."),
        ]:
            st.markdown(f"""
            <div class='card' style='display:flex;align-items:flex-start;gap:1.2rem;padding:1.3rem 1.7rem;margin-bottom:0.8rem;'>
                <div style='font-family:Playfair Display,serif;font-size:2rem;font-weight:900;color:#D4A017;line-height:1;min-width:40px;'>{num}</div>
                <div>
                    <div style='font-weight:800;font-size:1.08rem;margin-bottom:4px;'>{mech}</div>
                    <div style='font-size:0.95rem;color:#5A6E5C;line-height:1.65;'>{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 11 — PRODUCTIVITY, QUALITY & TRACEABILITY
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "Productivity, Quality & Traceability":
    sec_title("How the Data Strategy Drives Results")

    tab1, tab2, tab3 = st.tabs(["  Productivity  ","  Quality  ","  Traceability  "])

    with tab1:
        st.markdown("""
        <div class='dbox' style='font-size:1.07rem;margin-bottom:1.3rem;'>
            <div class='dtitle'>Definition</div>
            <div style='font-size:1.07rem;color:#fff;line-height:1.75;'>
            Productivity = <strong>yield per hectare</strong> + <strong>farmer efficiency</strong>
            + <strong>input optimisation</strong> (fertilizer, water, labor)
            </div>
        </div>""", unsafe_allow_html=True)

        c1,c2 = st.columns(2)
        c1.markdown("<div style='font-family:Playfair Display,serif;font-size:1.15rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>How the Strategy Improves Productivity</div>", unsafe_allow_html=True)
        for item in ["Data-driven farming decisions","Farmer benchmarking across regions","Training and farmer inclusion in digital tools"]:
            c1.markdown(f"""
            <div class='card' style='padding:1.1rem 1.4rem;margin-bottom:0.7rem;font-size:1rem;font-weight:600;'>
                <span style='color:#52B788;margin-right:10px;font-size:1.15rem;font-weight:900;'>✓</span>{item}
            </div>""", unsafe_allow_html=True)

        c2.markdown("<div style='font-family:Playfair Display,serif;font-size:1.15rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>Productivity Metrics Tracked</div>", unsafe_allow_html=True)
        for item in ["Average yield per hectare","Yield variability across regions","Input efficiency (output per unit of input)"]:
            c2.markdown(f"""
            <div class='card card-gold' style='padding:1.1rem 1.4rem;margin-bottom:0.7rem;font-size:1rem;font-weight:600;'>
                <span style='color:#D4A017;margin-right:10px;'>→</span>{item}
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class='card card-dark' style='margin-top:0.6rem;font-size:1.07rem;'>
            <strong>Impact:</strong> More consistent yields, lower costs, and higher farmer incomes.
        </div>""", unsafe_allow_html=True)

        fig = go.Figure()
        for vals, name, color in zip(
            [[5,4.5,0.60],[9.5,5.5,0.72],[12,9,2.0]],
            ["Baseline","12-Month","24-Month"],["#5A6E5C","#52B788","#D4A017"]
        ):
            fig.add_trace(go.Bar(name=name,x=["Onions","Mangoes","Cashew"],y=vals,
                                 marker_color=color,text=[f"{v}" for v in vals],
                                 textposition="outside",textfont=dict(size=14)))
        fig.update_layout(
            barmode="group",
            title=dict(text="Yield per Hectare (MT/ha) — Baseline vs Targets",font=dict(size=16,family="Playfair Display")),
            paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h",y=1.12,font=dict(size=13)),
            height=380,margin=dict(t=65,b=20,l=20,r=20),
            font=dict(family="DM Sans",size=13),
            yaxis=dict(gridcolor="rgba(0,0,0,0.05)",title="MT/ha"),
            xaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig,use_container_width=True)

    with tab2:
        st.markdown("""
        <div class='dbox' style='font-size:1.07rem;margin-bottom:1.3rem;'>
            <div class='dtitle'>Definition</div>
            <div style='font-size:1.07rem;color:#fff;line-height:1.75;'>
            Quality = meeting <strong>export standards</strong> + consistency in
            <strong>size, appearance, condition</strong> + reduced spoilage and contamination
            </div>
        </div>""", unsafe_allow_html=True)

        c1,c2 = st.columns(2)
        c1.markdown("<div style='font-family:Playfair Display,serif;font-size:1.15rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>How the Strategy Improves Quality</div>", unsafe_allow_html=True)
        for item in ["Standardised digital quality inspection data","Storage & post-harvest monitoring","Predictive and prescriptive analytics"]:
            c1.markdown(f"""
            <div class='card' style='padding:1.1rem 1.4rem;margin-bottom:0.7rem;font-size:1rem;font-weight:600;'>
                <span style='color:#52B788;margin-right:10px;font-size:1.15rem;font-weight:900;'>✓</span>{item}
            </div>""", unsafe_allow_html=True)

        c2.markdown("<div style='font-family:Playfair Display,serif;font-size:1.15rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>Quality Metrics Tracked</div>", unsafe_allow_html=True)
        for item in ["Export rejection rate","% of produce meeting export standards","Post-harvest loss percentage"]:
            c2.markdown(f"""
            <div class='card card-gold' style='padding:1.1rem 1.4rem;margin-bottom:0.7rem;font-size:1rem;font-weight:600;'>
                <span style='color:#D4A017;margin-right:10px;'>→</span>{item}
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class='card card-dark' style='margin-top:0.6rem;font-size:1.07rem;'>
            <strong>Impact:</strong> Higher export acceptance, reduced losses, and stronger market reputation.
        </div>""", unsafe_allow_html=True)

        fig = go.Figure()
        cats = ["Rejection Rate (%)","Post-Harvest Loss (%)","Farmer Compliance (%)"]
        for vals, name, color in zip(
            [[18,28,45],[10,20,65],[5,12,86]],
            ["Baseline","12-Month","24-Month"],["#5A6E5C","#52B788","#D4A017"]
        ):
            fig.add_trace(go.Bar(name=name,x=cats,y=vals,marker_color=color,
                                 text=[f"{v}%" for v in vals],textposition="outside",textfont=dict(size=14)))
        fig.update_layout(
            barmode="group",
            title=dict(text="Quality KPIs — Baseline vs Targets",font=dict(size=16,family="Playfair Display")),
            paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h",y=1.12,font=dict(size=13)),
            height=380,margin=dict(t=65,b=20,l=20,r=20),
            font=dict(family="DM Sans",size=13),
            yaxis=dict(gridcolor="rgba(0,0,0,0.05)",title="%"),
            xaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig,use_container_width=True)

    with tab3:
        st.markdown("""
        <div class='dbox' style='font-size:1.07rem;margin-bottom:1.3rem;'>
            <div class='dtitle'>Definition</div>
            <div style='font-size:1.07rem;color:#fff;line-height:1.75;'>
            Traceability = tracking produce from <strong>Farm → Storage → Shipment → Export Market</strong>
            with verifiable records at every stage of the supply chain.
            </div>
        </div>""", unsafe_allow_html=True)

        c1,c2 = st.columns(2)
        c1.markdown("<div style='font-family:Playfair Display,serif;font-size:1.15rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>How the Strategy Improves Traceability</div>", unsafe_allow_html=True)
        for item in ["End-to-end data capture at every supply chain stage","Integration across the full value chain"]:
            c1.markdown(f"""
            <div class='card' style='padding:1.1rem 1.4rem;margin-bottom:0.7rem;font-size:1rem;font-weight:600;'>
                <span style='color:#52B788;margin-right:10px;font-size:1.15rem;font-weight:900;'>✓</span>{item}
            </div>""", unsafe_allow_html=True)

        c2.markdown("<div style='font-family:Playfair Display,serif;font-size:1.15rem;font-weight:800;color:#1B4332;margin-bottom:0.9rem;'>Traceability Metrics Tracked</div>", unsafe_allow_html=True)
        for item in ["% produce with full farm-to-export trace","Export compliance rate","Time to trace back a rejected shipment","Traceability gaps in the supply chain"]:
            c2.markdown(f"""
            <div class='card card-gold' style='padding:0.95rem 1.3rem;margin-bottom:0.6rem;font-size:1rem;font-weight:600;'>
                <span style='color:#D4A017;margin-right:10px;'>→</span>{item}
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class='card card-dark' style='margin-top:0.6rem;font-size:1.07rem;'>
            <strong>Impact:</strong> Stronger buyer trust, regulatory compliance, and access to premium export markets.
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div style='font-family:Playfair Display,serif;font-size:1.2rem;font-weight:800;color:#1B4332;margin-bottom:0.8rem;'>% of Shipments Fully Traceable (Farm to Export)</div>", unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=["Current Baseline","12-Month Target","24-Month Target"],
            y=[15,55,90],
            marker_color=["#5A6E5C","#52B788","#D4A017"],
            text=["15%","55%","90%"],
            textposition="outside",
            textfont=dict(size=17,family="DM Sans",color="#1C2B1E"),
            width=0.45
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
            height=360,margin=dict(t=30,b=20,l=20,r=20),
            font=dict(family="DM Sans",size=14),
            yaxis=dict(range=[0,110],gridcolor="rgba(0,0,0,0.05)",title="% Shipments Traceable"),
            xaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig,use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 12 — THANK YOU
# ═══════════════════════════════════════════════════════════════════════════════
elif selected == "Thank You":
    st.markdown("""
    <div class='hero' style='padding:5rem 3rem;'>
        <div style='font-size:0.85rem;letter-spacing:3px;opacity:0.6;text-transform:uppercase;margin-bottom:0.7rem;'>
        Agro-Export Data Strategy · Main Campus Group 3
        </div>
        <h1 style='font-size:4rem;'>Thank You</h1>
        <p class='sub' style='font-size:1.25rem;'>For Your Attention</p>
        <hr style='border:1px solid rgba(255,255,255,0.18);width:55%;margin:2rem auto;'/>
        <div style='font-size:0.95rem;opacity:0.75;margin-bottom:0.9rem;'>Presented by:</div>
        <div style='display:flex;flex-wrap:wrap;justify-content:center;gap:0.7rem;'>
            <span class='badge'>Abigail Ansah Amponsah — 11019225</span>
            <span class='badge'>Ekua Micah Abakah-Paintsil — 11012281</span>
            <span class='badge'>Nana Kane Bruce Eshun — 11117122</span>
        </div>
        <div style='margin-top:1.4rem;font-size:0.88rem;opacity:0.6;'>18 March 2026</div>
    </div>""", unsafe_allow_html=True)

    sec_title("24-Month Strategy Impact — Final Summary")

    s1,s2,s3,s4 = st.columns(4)
    for col, val, lbl, chg in zip([s1,s2,s3,s4],
        ["GHS 180K","95%","90%","+18%"],
        ["Annual Savings (Year 2)","Export Acceptance","Supply Traceability","Farmer Income Growth"],
        ["At ≤12% post-harvest loss","Shipment acceptance rate","Full farm-to-export trace","vs. pre-strategy baseline"]):
        col.markdown(f"""
        <div class='mtile gold-top'>
            <div class='num'>{val}</div>
            <div class='lbl'>{lbl}</div>
            <div class='change'>{chg}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cats = ["Productivity","Quality","Traceability","Governance","Analytics Maturity"]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=[2,2,1,2,1],theta=cats,fill="toself",name="Baseline",
                                  line=dict(color="#5A6E5C",width=2.5),fillcolor="rgba(90,110,92,0.12)"))
    fig.add_trace(go.Scatterpolar(r=[4.5,4.5,4.5,4,4],theta=cats,fill="toself",name="24-Month Target",
                                  line=dict(color="#52B788",width=3),fillcolor="rgba(82,183,136,0.18)"))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True,range=[0,5],tickfont=dict(size=12),gridcolor="rgba(27,67,50,0.12)"),
            angularaxis=dict(tickfont=dict(size=15,family="DM Sans",color="#1B4332"))
        ),
        legend=dict(orientation="h",y=-0.1,font=dict(size=15)),
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        height=480,margin=dict(t=20,b=60,l=30,r=30),
        font=dict(family="DM Sans")
    )
    st.plotly_chart(fig,use_container_width=True)


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    Agro-Export Data Strategy &nbsp;·&nbsp; Main Campus Group 3 &nbsp;·&nbsp; March 2026
</div>""", unsafe_allow_html=True)