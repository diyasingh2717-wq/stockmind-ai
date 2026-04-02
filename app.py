import streamlit as st
from src.predict import predict
from supabase import create_client

# ── 1. PAGE SETUP ─────────────────────────────────
st.set_page_config(page_title="StockAI", page_icon="📈", layout="wide")

# ── 2. SESSION STATE (TRIALS & PRO) ───────────────
if 'is_pro' not in st.session_state:
    st.session_state.is_pro = False
if 'trial_count' not in st.session_state:
    st.session_state.trial_count = 0

FREE_LIMIT = 10

# ── 3. DATABASE CONFIGURATION ──────────────────────
SUPABASE_URL = "https://kxqandvimqemiqxzhane.supabase.co"
# IMPORTANT: You MUST paste the long key starting with 'eyJ' here for it to work
SUPABASE_KEY = "kxqandvimqemiqxzhane"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception:
    st.error("Database connection failed. Please check your Supabase API Key.")

# ── 4. CUSTOM CSS (PREMIUM DARK THEME) ─────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, .stApp { background: #05080f !important; font-family: 'DM Sans', sans-serif; color: #e2e8f0; }
#MainMenu, footer, header { display: none !important; }
.block-container { padding: 1rem 1.5rem !important; }

.topnav {
    display: flex; align-items: center; background: linear-gradient(135deg, #0d1117, #0f1a2e);
    border: 1px solid #1e3a5f; border-radius: 14px; padding: 0.85rem 1.5rem; margin-bottom: 1rem;
}
.logo {
    font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.3rem;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.main-card {
    background: linear-gradient(135deg, #0d1117, #0f1a2e);
    border: 1px solid #1e3a5f; border-radius: 16px; padding: 1.6rem; margin-bottom: 1rem;
}
.section-title {
    font-family: 'Syne', sans-serif; font-size: 0.72rem; font-weight: 700;
    color: #334e68; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.8rem;
}
.stButton > button {
    background: linear-gradient(135deg, #38bdf8, #818cf8) !important;
    color: #05080f !important; font-weight: 700 !important; width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# ── 5. TOP NAV ────────────────────────────────────
st.markdown('<div class="topnav"><span class="logo">◈ StockAI</span></div>', unsafe_allow_html=True)

# ── 6. MAIN CONTENT (TWO COLUMNS) ─────────────────
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚡ AI Prediction Engine</div>', unsafe_allow_html=True)

    trials_left = FREE_LIMIT - st.session_state.trial_count
    can_use = st.session_state.is_pro or (trials_left > 0)

    if can_use:
        if not st.session_state.is_pro:
            st.info(f"🎁 Free Trial: {trials_left} attempts remaining.")
        
        stock = st.text_input("Enter Stock Symbol", placeholder="e.g., TSLA or RELIANCE.NS")
        
        if st.button("Generate AI Forecast →"):
            if stock:
                with st.spinner("Analyzing Market Data..."):
                    try:
                        trend, prob, target = predict(stock.upper().strip())
                        st.success(f"Signal: {trend} | Confidence: {prob*100:.1f}%")
                        st.metric("Target Price", f"{target:.2f}")
                        
                        if not st.session_state.is_pro:
                            st.session_state.trial_count += 1
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
    else:
        st.error("❌ Free Trial Expired! Please activate Pro in the sidebar.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 Project Feedback</div>', unsafe_allow_html=True)
    f_url = "https://docs.google.com/forms/d/e/1FAIpQLSepT-SWxjzAayz39w3bF-MM77GDiCas9oFmexh2H5rdNAqf3A/viewform?embedded=true"
    st.components.v1.iframe(f_url, height=500, scrolling=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── 7. SIDEBAR (UPI TRANSACTION ID ACTIVATION) ───
st.sidebar.title("🚀 StockAI Pro")

if not st.session_state.is_pro:
    upi_id = "2007diyasingh@okicici"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa={upi_id}&am=99&cu=INR"
    st.sidebar.image(qr_url, caption="Scan to Pay ₹99 & Unlock Pro")
    
    with st.sidebar.form("activate_pro"):
        email = st.text_input("Registered Email")
        upi_tid = st.text_input("UPI Transaction ID (12-Digits)")
        
        if st.form_submit_button("Activate Unlimited Access"):
            if "@" in email and len(upi_tid) >= 12:
                try:
                    data = {
                        "email": email, 
                        "transaction_id": upi_tid, 
                        "utr_number": upi_tid, 
                        "verified": False
                    }
                    # FIXED INDENTATION AND CALL
                    supabase.table("premium_users").insert(data).execute()
                    
                    st.session_state.is_pro = True
                    st.sidebar.success("✅ Pro Activated!")
                    st.rerun()
                except Exception as e:
                    st.sidebar.error(f"Database error: {e}")
            else:
                st.sidebar.warning("Enter valid email and 12-digit Transaction ID.")
else:
    st.sidebar.success("✨ PRO STATUS: ACTIVE")
    if st.sidebar.button("Logout / Reset Trials"):
        st.session_state.is_pro = False
        st.session_state.trial_count = 0
        st.rerun()
