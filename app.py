import streamlit as st
from src.predict import predict
from supabase import create_client

# ── 1. PAGE SETUP ─────────────────────────────────
st.set_page_config(page_title="StockAI", page_icon="📈", layout="wide")

# ── 2. SESSION STATE (TRACKING TRIALS & PRO) ──────
if 'is_pro' not in st.session_state:
    st.session_state.is_pro = False
if 'trial_count' not in st.session_state:
    st.session_state.trial_count = 0

FREE_LIMIT = 3

# ── 3. DATABASE CONFIGURATION ──────────────────────
SUPABASE_URL = "https://kxqandvimqemiqxzhane.supabase.co"
# IMPORTANT: Paste your actual 'anon public' key from Supabase settings here
SUPABASE_KEY = "PASTE_YOUR_LONG_ANON_KEY_HERE"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception:
    st.error("Database connection failed. Please check your Supabase API Key.")

# ── 4. CUSTOM CSS (PREMIUM DARK THEME) ─────────────
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
}
.logo {
    font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.3rem;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.main-card {
    background: linear-gradient(135deg, #0d1117, #0f1a2e);
    border: 1px solid #1e3a5f; border-radius: 16px;
    padding: 1.6rem; box-shadow: 0 4px 32px #00000040;
    margin-bottom: 1rem;
}
.section-title {
    font-family: 'Syne', sans-serif; font-size: 0.72rem; font-weight: 700;
    color: #334e68; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.8rem;
}
.stButton > button {
    background: linear-gradient(135deg, #38bdf8, #818cf8) !important;
    color: #05080f !important; border: none !important; border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# ── 5. TOP NAV ──────────────────────────────
st.markdown('<div class="topnav"><span class="logo">◈ StockAI</span></div>', unsafe_allow_html=True)

# ── 6. MAIN CONTENT (TWO COLUMNS) ──────────
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚡ AI Prediction Engine</div>', unsafe_allow_html=True)

    # Logic: Check if user is Pro OR still has Free Trials
    trials_left = FREE_LIMIT - st.session_state.trial_count
    can_use = st.session_state.is_pro or (trials_left > 0)

    if can_use:
        if not st.session_state.is_pro:
            st.info(f"🎁 Free Trial: {trials_left} predictions remaining.")
        
        stock = st.text_input("Enter Stock Symbol", placeholder="AAPL · TSLA · RELIANCE.NS")
        
        if st.button("Generate AI Forecast →"):
            if stock:
                with st.spinner(f"Analyzing {stock.upper()}..."):
                    try:
                        trend, prob, target = predict(stock.upper().strip())
                        st.success(f"Signal: {trend} | Confidence: {prob*100:.1f}%")
                        st.metric("AI Target Price", f"{target:.2f}")
                        
                        # Only count trials for non-pro users
                        if not st.session_state.is_pro:
                            st.session_state.trial_count += 1
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error analyzing symbol: {e}")
            else:
                st.warning("Please enter a stock ticker.")
    else:
        st.error("❌ Free Trial Expired! Please upgrade in the sidebar for Unlimited Access.")
        st.text_input("Stock Symbol", placeholder="Upgrade to Pro...", disabled=True)
        st.button("Run Prediction →", disabled=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # FEEDBACK CARD (EMBEDDED GOOGLE FORM)
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 Project Feedback</div>', unsafe_allow_html=True)
    
    google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSepT-SWxjzAayz39w3bF-MM77GDiCas9oFmexh2H5rdNAqf3A/viewform?embedded=true"
    st.components.v1.iframe(google_form_url, height=550, scrolling=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # FOOTER ACTIONS
    st.link_button("💎 Go Premium — ₹99/month", "https://rzp.io/l/rzp_test_SYG6sG4tSY0LC7")
    st.markdown("### StockAI - AI Based Stock Prediction Platform")
    st.write("Live Market Status: Active")

# ── 7. SIDEBAR: PAYMENT & PRO UNLOCK ────────────
st.sidebar.title("🚀 StockAI Pro")

if not st.session_state.is_pro:
    st.sidebar.markdown("""
    **Pro Benefits:**
    - Unlimited AI Predictions
    - 99% Accuracy Signals
    - Instant Target Prices
    """)
    
    upi_id = "2007diyasingh@okicici"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa={upi_id}&am=99&cu=INR"
    st.sidebar.image(qr_url, caption="Scan & Pay ₹99 to Unlock")
    
    with st.sidebar.form("pro_activation"):
        u_email = st.text_input("Email Address")
        u_utr = st.text_input("12-Digit Transaction ID")
        
        if st.form_submit_button("Activate Unlimited Access"):
            if "@" in u_email and len(u_utr) >= 12:
                try:
                    # Save to Supabase
                    db_data = {"email": u_email, "transaction_id": u_utr, "verified": False}
                    supabase.table("payments").insert(db_data).execute()
                    
                    # Immediate Unlock
                    st.session_state.is_pro = True
                    st.sidebar.success("✅ Pro Activated! Welcome.")
                    st.rerun()
                except Exception:
                    st.sidebar.error("Database connection failed.")
            else:
                st.sidebar.warning("Enter a valid email and 12-digit UTR.")
else:
    st.sidebar.success("✨ PRO STATUS: ACTIVE")
    if st.sidebar.button("Logout / Reset Trials"):
        st.session_state.is_pro = False
        st.session_state.trial_count = 0
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("📩 Support: 2024ca56f@sigce.edu.in")
