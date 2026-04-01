import streamlit as st
from src.predict import predict
from supabase import create_client
import datetime

# ── 1. PAGE SETUP ─────────────────────────────────
st.set_page_config(page_title="StockAI", page_icon="📈", layout="wide")

# ── 2. DATABASE CONFIGURATION ──────────────────────
# Using your specific Supabase credentials
SUPABASE_URL = "https://kxqandvimqemiqxzhane.supabase.co"
# IMPORTANT: Replace the string below with your actual 'anon public' key from Supabase settings
SUPABASE_KEY = "PASTE_YOUR_LONG_ANON_KEY_HERE" 

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("Database connection failed. Please check your Supabase API Key.")

# ── 3. CUSTOM CSS ──────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, .stApp { background: #05080f !important; font-family: 'DM Sans', sans-serif; color: #e2e8f0; }
#MainMenu, footer, header { display: none !important; }
.block-container { padding: 1rem 1.5rem !important; max-width: 100% !important; }

.topnav {
    display: flex; align-items: center; gap: 1rem;
    background: linear-gradient(135deg, #0d1117, #0f1a2e);
    border: 1px solid #1e3a5f; border-radius: 14px;
    padding: 0.85rem 1.5rem; margin-bottom: 1rem;
    box-shadow: 0 4px 24px #0008;
}
.logo {
    font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.3rem;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.nav-badge {
    background: #0f2744; color: #38bdf8; font-size: 0.62rem;
    padding: 3px 10px; border-radius: 20px; letter-spacing: 1.5px;
    text-transform: uppercase; border: 1px solid #1e3a5f;
}
.nav-right { margin-left: auto; display: flex; align-items: center; gap: 0.5rem; }
.nav-dot { width: 7px; height: 7px; border-radius: 50%; background: #22c55e; box-shadow: 0 0 8px #22c55e; }
.nav-status { color: #64748b; font-size: 0.78rem; }

.stats-row { display: grid; grid-template-columns: repeat(3,1fr); gap: 1rem; margin-bottom: 1rem; }
.stat-card {
    background: linear-gradient(135deg, #0d1117, #0f1a2e);
    border: 1px solid #1e3a5f; border-radius: 14px; padding: 1.1rem 1.3rem;
    box-shadow: 0 2px 12px #0006;
}
.stat-label { color: #334e68; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 1.5px; }
.stat-value { font-family: 'Syne', sans-serif; font-size: 1.6rem; font-weight: 700; margin-top: 4px; color: #38bdf8; }
.stat-sub { color: #334e68; font-size: 0.7rem; margin-top: 3px; }

.main-card {
    background: linear-gradient(135deg, #0d1117, #0f1a2e);
    border: 1px solid #1e3a5f; border-radius: 16px;
    padding: 1.6rem; box-shadow: 0 4px 32px #00000040;
}
.result-card {
    background: #080c14; border: 1px solid #1e3a5f;
    border-radius: 10px; padding: 1rem;
    box-shadow: inset 0 1px 0 #ffffff08;
    margin-bottom: 1rem;
}
.rc-label { color: #334e68; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 1px; }
.rc-value { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; color: #f1f5f9; margin-top: 3px; }
.divider { height: 1px; background: #1e3a5f; margin: 0.65rem 0; }
.section-title {
    font-family: 'Syne', sans-serif; font-size: 0.72rem; font-weight: 700;
    color: #334e68; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.8rem;
}

.stTextInput > div > div > input,
.stTextArea textarea {
    background: #080c14 !important; color: #e2e8f0 !important;
    border: 1px solid #1e3a5f !important; border-radius: 8px !important;
    font-size: 0.88rem !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label {
    color: #334e68 !important; font-size: 0.72rem !important;
    text-transform: uppercase !important; letter-spacing: 1px !important;
}
div[data-baseweb="select"] > div {
    background: #080c14 !important; border: 1px solid #1e3a5f !important;
    border-radius: 8px !important; color: #e2e8f0 !important;
}
.stButton > button {
    background: linear-gradient(135deg, #38bdf8, #818cf8) !important;
    color: #05080f !important; border: none !important; border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    font-size: 0.85rem !important; width: 100% !important; padding: 0.6rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── 4. TOP NAV ──────────────────────────────
st.markdown("""
<div class="topnav">
  <span class="logo">◈ StockAI</span>
  <span class="nav-badge">Beta v2.0</span>
  <div class="nav-right">
    <div class="nav-dot"></div>
    <span class="nav-status">Live Market Data</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── 5. STATS ─────────────────────────────────
st.markdown("""
<div class="stats-row">
  <div class="stat-card">
    <div class="stat-label">Confidence</div>
    <div class="stat-value">Dynamic</div>
    <div class="stat-sub">Calculated per stock</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Stocks Analyzed</div>
    <div class="stat-value">1,240+</div>
    <div class="stat-sub">NSE · NYSE · NASDAQ</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Data Source</div>
    <div class="stat-value" style="font-size:1rem;padding-top:6px;">yFinance API</div>
    <div class="stat-sub">30-day rolling window</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── 6. MAIN CONTENT (TWO COLUMNS) ──────────
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚡ Stock Prediction</div>', unsafe_allow_html=True)

    stock = st.text_input("Stock Symbol", placeholder="AAPL · TSLA · HDFCBANK.NS")

    if st.button("Run Prediction →"):
        if not stock.strip():
            st.warning("Enter a symbol first.")
        else:
            with st.spinner(f"Analyzing {stock.upper()}..."):
                try:
                    trend, prob, target = predict(stock.upper().strip())
                    color = "#22c55e" if trend == "UP" else "#ef4444"
                    arrow = "▲ UP" if trend == "UP" else "▼ DOWN"
                    currency = "₹" if (".NS" in stock.upper() or ".BO" in stock.upper()) else "$"
                    st.markdown(f"""
                    <div class="result-card">
                      <div class="rc-label">Symbol</div>
                      <div class="rc-value">{stock.upper()}</div>
                      <div class="divider"></div>
                      <div class="rc-label">Trend</div>
                      <div class="rc-value" style="color:{color}; font-size:1.3rem;">{arrow}</div>
                      <div class="divider"></div>
                      <div class="rc-label">Confidence</div>
                      <div class="rc-value" style="color:{color};">{prob*100:.1f}%</div>
                      <div class="divider"></div>
                      <div class="rc-label">Target Price</div>
                      <div class="rc-value" style="color:{color};">{currency}{target:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ {e}")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 Feedback</div>', unsafe_allow_html=True)
    with st.form("fb_form"):
        st.text_input("Your Name", placeholder="e.g. Rahul")
        st.selectbox("Type", ["Bug Report", "UI Suggestion", "Feature Request", "General"])
        st.select_slider("Rating ⭐", [1, 2, 3, 4, 5], value=4)
        st.text_area("Message", placeholder="What can we improve?", height=100)
        if st.form_submit_button("Submit Feedback →"):
            st.success("✅ Thanks! Feedback received.")
    st.markdown('</div>', unsafe_allow_html=True)

# ── 7. SIDEBAR: PAYMENT & DATABASE TRACKING ──────
st.sidebar.title("💎 StockAI Pro")
st.sidebar.info("Get access to 99% accurate signals.")

# UPI & QR Config
upi_id = "2007diyasingh@okicici"
upi_link = f"upi://pay?pa={upi_id}&pn=StockAI&am=99&cu=INR"
qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={upi_link}"

st.sidebar.image(qr_url, caption="Scan to Pay ₹99")
st.sidebar.markdown("---")
st.sidebar.write("**Step 2: Confirm Payment**")

# THE DATABASE FORM
with st.sidebar.form("payment_form"):
    cust_email = st.text_input("Your Email")
    utr_no = st.text_input("UPI transaction id")
    
    if st.form_submit_button("Activate My Pro Access"):
        if "@" in cust_email and len(upi_id) >= 12:
            try:
                # SENDS DATA TO YOUR 'payments' TABLE
                db_entry = {
                    "email": cust_email,
                    "transaction_id": upi_id,
                    "verified": False
                }
                supabase.table("payments").insert(db_entry).execute()
                st.sidebar.success("✅ Logged! Pro unlocks after verification.")
            except Exception as e:
                st.sidebar.error("Database error. Ensure table 'payments' exists.")
        else:
            st.sidebar.warning("Enter a valid Email and 12-digit UPI transaction.")

st.sidebar.markdown("---")
st.sidebar.write("📩 Contact: 2024ca56f@sigce.edu.in")
with col_right:
    # ── FEEDBACK SECTION ───────────────────────────
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 Share Your Feedback</div>', unsafe_allow_html=True)
    
    st.write("Help us improve StockAI by filling out our quick feedback form.")
    
    # YOUR EXACT GOOGLE FORM LINK AS A BUTTON
    st.link_button("📝 Open Google Feedback Form", 
                   "https://docs.google.com/forms/d/e/1FAIpQLSepT-SWxjzAayz39w3bF-MM77GDiCas9oFmexh2H5rdNAqf3A/viewform?usp=header")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # ── PREMIUM & FOOTER ──────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Your Payment Link
    st.link_button("💎 Go Premium — ₹99/month", 
                   "https://rzp.io/l/rzp_test_SYG6sG4tSY0LC7")
    
    st.markdown("### StockAI - AI Based Stock Prediction Platform")
    st.write("This project is live and running.") add in this
