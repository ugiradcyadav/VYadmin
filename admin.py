"""
V.Y. Tech — Admin Panel (Light Theme)
Run with: streamlit run admin.py
Keep this file PRIVATE — only for your use.
"""

import streamlit as st
import json
import os
import secrets
import string
from datetime import datetime, timedelta
import pandas as pd

# ── File paths (same folder as the bot) ──────────────────────
LICENSE_FILE = "vy_licenses.json"
CLIENTS_FILE = "vy_clients.json"

# ── MASTER ADMIN PASSWORD ─────────────────────────────────────
# CHANGE THIS to something only you know!
ADMIN_PASSWORD = "VYTech@2025#Admin"

# ── IB Vantage partner link (your referral link) ──────────────
IB_VANTAGE_LINK = "https://www.vantagemarkets.com/open-live-account/?affid=MjMxNDgzOTU=&invitecode=u0vkGliE"
IB_DISCOUNT_PERCENT = 15   # % discount for IB clients

# ── Pricing plans ─────────────────────────────────────────────
PLANS = {
    "Trial":      {"price": 0,    "days": 1,   "label": "1-day Free Trial"},
    "Weekly":      {"price": 10,    "days": 7,   "label": "7-day — $10"},
    "Monthly":    {"price": 49,   "days": 30,  "label": "Monthly — $49"},
    "Quarterly":  {"price": 129,  "days": 90,  "label": "Quarterly — $129"},
    "Annual":     {"price": 399,  "days": 365, "label": "Annual — $399"},
    "Lifetime":   {"price": 999,  "days": 36500, "label": "Lifetime — $999"},
}

# ─────────────────────────────────────────────────────────────
# DATA HELPERS
# ─────────────────────────────────────────────────────────────

def load_licenses():
    if not os.path.exists(LICENSE_FILE):
        save_licenses({})
        return {}
    with open(LICENSE_FILE, "r") as f:
        return json.load(f)

def save_licenses(data):
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_clients():
    if not os.path.exists(CLIENTS_FILE):
        save_clients([])
        return []
    with open(CLIENTS_FILE, "r") as f:
        return json.load(f)

def save_clients(data):
    with open(CLIENTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def generate_key(plan="Pro"):
    """Generate a unique V.Y. Tech license key"""
    chars = string.ascii_uppercase + string.digits
    part1 = "VYTECH"
    part2 = plan.upper()[:3]
    part3 = "".join(secrets.choice(chars) for _ in range(4))
    part4 = "".join(secrets.choice(chars) for _ in range(4))
    return f"{part1}-{part2}-{part3}-{part4}"

def get_stats():
    licenses = load_licenses()
    clients  = load_clients()
    now      = datetime.now()

    total        = len(licenses)
    active       = sum(1 for v in licenses.values() if v.get("active") and datetime.strptime(v["expiry"], "%Y-%m-%d") >= now)
    expired      = sum(1 for v in licenses.values() if datetime.strptime(v["expiry"], "%Y-%m-%d") < now)
    revenue      = sum(v.get("paid_amount", 0) for v in licenses.values())
    ib_clients   = sum(1 for v in licenses.values() if v.get("ib_partner"))
    pending      = sum(1 for c in clients if c.get("status") == "pending")

    return {
        "total":       total,
        "active":      active,
        "expired":     expired,
        "revenue":     revenue,
        "ib_clients":  ib_clients,
        "pending":     pending,
    }

# ─────────────────────────────────────────────────────────────
# CSS - PURE WHITE UI UPDATE
# ─────────────────────────────────────────────────────────────

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    *, html, body, .stApp, .main { font-family: 'Inter', sans-serif !important; }
    
    /* Main Background & Text (PURE WHITE) */
    html, body, .stApp, .main    { background-color: #ffffff !important; color: #111827 !important; }
    .block-container             { padding-top: 1rem !important; }
    
    /* Sidebar */
    [data-testid="stSidebar"]      { background: #f8fafc !important; border-right: 1px solid #e2e8f0 !important; }
    [data-testid="stSidebar"] * { color: #334155 !important; }

    /* Buttons */
    .stButton > button             { background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%) !important;
                                     color: #ffffff !important; border: none !important; border-radius: 8px !important;
                                     font-weight: 600 !important; transition: all .2s !important; 
                                     box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important; }
    .stButton > button:hover       { filter: brightness(1.1) !important; box-shadow: 0 4px 6px rgba(0,0,0,0.15) !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { background: #f1f5f9 !important; border-radius: 10px !important; padding: 4px; gap: 4px; }
    .stTabs [data-baseweb="tab"]  { color: #64748b !important; border-radius: 7px !important; font-weight: 600 !important; }
    .stTabs [aria-selected="true"]{ background: linear-gradient(135deg, #2563eb, #7c3aed) !important; color: #ffffff !important; }

    /* Top Metrics Boxes */
    [data-testid="stMetric"]      { background: #ffffff !important; border: 1px solid #e2e8f0 !important;
                                    border-radius: 10px !important; padding: 14px 16px !important; 
                                    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important; }
    [data-testid="stMetricValue"] { color: #0f172a !important; font-size: 26px !important; font-weight: 800 !important; }
    [data-testid="stMetricLabel"] { color: #64748b !important; font-size: 12px !important; letter-spacing: .5px; text-transform: uppercase; font-weight: 700 !important; }

    /* --- LIGHT MODE INPUT FIELDS --- */
    
    /* 1. Labels */
    label p, .stCheckbox p { color: #334155 !important; font-weight: 600 !important; } 
    
    /* 2. Text Input Boxes Background & Typed Text */
    .stTextInput input, .stNumberInput input, .stTextArea textarea, .stDateInput input {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        color: #0f172a !important; 
        border-radius: 8px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
    }
    
    /* Focus state for inputs */
    .stTextInput input:focus, .stNumberInput input:focus { border-color: #2563eb !important; box-shadow: 0 0 0 1px #2563eb !important; }
    
    /* 3. Dropdowns (Selectbox) */
    .stSelectbox [data-baseweb="select"] > div { background-color: #ffffff !important; border-color: #cbd5e1 !important; }
    .stSelectbox [data-baseweb="select"] span { color: #0f172a !important; font-weight: 500 !important; } 

    /* 4. Placeholders Visibility */
    ::placeholder { color: #94a3b8 !important; opacity: 1 !important; }
    input::placeholder, textarea::placeholder { color: #94a3b8 !important; }

    /* Tables and Cards */
    .stDataFrame { border: 1px solid #e2e8f0 !important; border-radius: 8px !important; }
    ::-webkit-scrollbar { width: 6px; } ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
    .vy-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    
    /* Badges */
    .vy-badge-active   { background: #dcfce7; color: #166534; border: 1px solid #86efac; padding: 2px 8px; border-radius: 20px; font-size: 11px; font-weight: 600; }
    .vy-badge-expired  { background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; padding: 2px 8px; border-radius: 20px; font-size: 11px; font-weight: 600; }
    .vy-badge-inactive { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; padding: 2px 8px; border-radius: 20px; font-size: 11px; font-weight: 600; }
    
    /* Footer */
    .vy-footer { text-align: center; margin-top: 30px; padding: 16px 0; border-top: 1px solid #e2e8f0; font-size: 11px; color: #64748b; font-weight: 500;}
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────

st.set_page_config(page_title="V.Y. Tech — Admin Panel", page_icon="🔐", layout="wide")
inject_css()

# ─────────────────────────────────────────────────────────────
# PASSWORD GATE
# ─────────────────────────────────────────────────────────────

if "admin_auth" not in st.session_state:
    st.session_state.admin_auth = False

if not st.session_state.admin_auth:
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:80vh;text-align:center;">
        <div style="font-size:42px;font-weight:900;letter-spacing:7px;
                    background:linear-gradient(135deg,#2563eb 0%,#7c3aed 100%);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            V.Y. TECH
        </div>
        <div style="color:#64748b;font-size:11px;letter-spacing:4px;margin-top:4px;font-weight:600;">ADMIN CONTROL PANEL</div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1.5, 2, 1.5])
    with col:
        st.markdown("""
        <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:16px;padding:32px;text-align:center;box-shadow:0 4px 6px -1px rgba(0,0,0,0.1);">
            <div style="color:#334155;font-size:15px;font-weight:700;margin-bottom:20px;">🔐 Admin Login</div>
        </div>
        """, unsafe_allow_html=True)
        pw = st.text_input("Admin Password", type="password", placeholder="Enter admin password")
        if st.button("Enter Admin Panel", use_container_width=True, type="primary"):
            if pw == ADMIN_PASSWORD:
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("❌ Wrong password.")
    st.stop()

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────

stats = get_stats()
now_str = datetime.now().strftime("%d %b %Y  %H:%M:%S")

st.markdown(f"""
<div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;
            padding:16px 28px;margin-bottom:18px;box-shadow:0 1px 3px rgba(0,0,0,0.05);
            display:flex;align-items:center;justify-content:space-between;">
    <div>
        <div style="font-size:24px;font-weight:900;letter-spacing:5px;
                    background:linear-gradient(135deg,#2563eb 0%,#7c3aed 100%);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            V.Y. TECH
        </div>
        <div style="color:#64748b;font-size:9px;letter-spacing:3px;text-transform:uppercase;margin-top:2px;font-weight:700;">
            Admin Control Panel
        </div>
    </div>
    <div style="display:flex;gap:24px;align-items:center;font-size:12px;">
        <div style="text-align:center;">
            <div style="color:#64748b;font-size:9px;text-transform:uppercase;letter-spacing:2px;font-weight:600;">Pending</div>
            <div style="color:#ea580c;font-weight:800;">{stats['pending']} requests</div>
        </div>
        <div style="text-align:center;">
            <div style="color:#64748b;font-size:9px;text-transform:uppercase;letter-spacing:2px;font-weight:600;">Active</div>
            <div style="color:#16a34a;font-weight:800;">{stats['active']} licenses</div>
        </div>
        <div style="text-align:center;">
            <div style="color:#64748b;font-size:9px;text-transform:uppercase;letter-spacing:2px;font-weight:600;">Time</div>
            <div style="color:#334155;font-weight:700;">{now_str}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TOP METRICS
# ─────────────────────────────────────────────────────────────

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("📋 Total Licenses",  stats["total"])
c2.metric("✅ Active",          stats["active"])
c3.metric("❌ Expired",         stats["expired"])
c4.metric("💰 Total Revenue",   f"${stats['revenue']:,}")
c5.metric("🤝 IB Clients",      stats["ib_clients"])
c6.metric("⏳ Pending Approvals", stats["pending"])

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────

tab_gen, tab_manage, tab_clients, tab_pending, tab_ib, tab_settings = st.tabs([
    "➕  Generate License",
    "📋  Manage Licenses",
    "👥  All Clients",
    "⏳  Pending Approvals",
    "🤝  IB Partner Tracker",
    "⚙️  Settings",
])

# ════════════════════════════════════════════════════════════
# TAB 1 — GENERATE LICENSE
# ════════════════════════════════════════════════════════════

with tab_gen:
    st.markdown("#### ➕ Create a New License Key")
    st.markdown("""
    <div class="vy-card">
        <div style="color:#475569;font-size:13px;margin-bottom:16px;font-weight:500;">
            Fill in the client details and select a plan. The key will be generated automatically.
            You can then copy it and send via WhatsApp / Email to the client.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        g_name    = st.text_input("Client Full Name *",    placeholder="e.g. Ahmed Khan")
        g_email   = st.text_input("Client Email *",        placeholder="ahmed@email.com")
        g_phone   = st.text_input("WhatsApp Number",       placeholder="+92-300-1234567")
        g_broker  = st.text_input("Broker Name",           placeholder="e.g. Vantage, XM, ICMarkets")
        g_acc_id  = st.text_input("MT5 Account ID",        placeholder="Broker account number")

    with col2:
        g_plan    = st.selectbox("Subscription Plan", list(PLANS.keys()),
                                 format_func=lambda x: PLANS[x]["label"])
        g_ib      = st.checkbox("IB Vantage Partner (15% discount applies)", value=False)
        g_paid    = st.number_input("Amount Paid ($)", min_value=0.0, value=float(PLANS[g_plan]["price"]), step=1.0)
        g_notes   = st.text_area("Notes (optional)", placeholder="Any special instructions...")

        # Auto-calculate expiry
        days      = PLANS[g_plan]["days"]
        expiry_dt = datetime.now() + timedelta(days=days)
        g_expiry  = st.date_input("Expiry Date", value=expiry_dt)

        if g_ib:
            discount = g_paid * (IB_DISCOUNT_PERCENT / 100)
            st.info(f"🤝 IB Discount Applied: -${discount:.2f} → Final: **${g_paid - discount:.2f}**")

    st.markdown("---")
    col_btn1, col_btn2, col_sp = st.columns([1, 1, 3])

    with col_btn1:
        if st.button("🔑  Generate & Save License", type="primary", use_container_width=True):
            if not g_name or not g_email:
                st.error("Name and Email are required.")
            else:
                key = generate_key(g_plan)
                lics = load_licenses()

                # Make sure key is unique
                while key in lics:
                    key = generate_key(g_plan)

                paid_final = g_paid * (1 - IB_DISCOUNT_PERCENT / 100) if g_ib else g_paid

                lics[key] = {
                    "user":        g_name,
                    "email":       g_email,
                    "phone":       g_phone,
                    "broker":      g_broker,
                    "account_id":  g_acc_id,
                    "plan":        g_plan,
                    "expiry":      g_expiry.strftime("%Y-%m-%d"),
                    "active":      True,
                    "ib_partner":  g_ib,
                    "paid_amount": round(paid_final, 2),
                    "notes":       g_notes,
                    "created_at":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                save_licenses(lics)

                st.success(f"✅ License created successfully!")
                st.markdown(f"""
                <div style="background:#f0fdf4;border:2px solid #22c55e;border-radius:12px;padding:20px;text-align:center;margin-top:12px;">
                    <div style="color:#166534;font-size:11px;letter-spacing:2px;text-transform:uppercase;font-weight:700;">License Key</div>
                    <div style="font-size:24px;font-weight:900;color:#15803d;letter-spacing:4px;margin:10px 0;
                                font-family:'JetBrains Mono',monospace;">
                        {key}
                    </div>
                    <div style="color:#166534;font-size:12px;font-weight:600;">
                        Client: {g_name} &nbsp;|&nbsp; Plan: {g_plan} &nbsp;|&nbsp; Expires: {g_expiry.strftime('%d %b %Y')}
                    </div>
                    <div style="color:#166534;font-size:11px;margin-top:6px;">
                        📋 Copy this key and send to client via WhatsApp or Email.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # WhatsApp message template
                wa_msg = (
                    f"🎉 *V.Y. Tech — Omega AI Platform*%0A%0A"
                    f"Hello {g_name}!%0AYour license has been activated.%0A%0A"
                    f"🔑 *License Key:*%0A`{key}`%0A%0A"
                    f"📅 Plan: {g_plan}%0A"
                    f"⏰ Valid until: {g_expiry.strftime('%d %b %Y')}%0A%0A"
                    f"Enter this key when you start the V.Y. Tech trading platform.%0A%0A"
                    f"For support: Contact V.Y. Tech team."
                )
                phone_clean = g_phone.replace("+", "").replace("-", "").replace(" ", "") if g_phone else ""
                wa_url = f"https://wa.me/{phone_clean}?text={wa_msg}" if phone_clean else ""

                if wa_url:
                    st.markdown(f"""
                    <div style="margin-top:12px;text-align:center;">
                        <a href="{wa_url}" target="_blank"
                           style="background:#25d366;color:#fff;
                                  text-decoration:none;padding:10px 28px;border-radius:8px;
                                  font-weight:600;font-size:13px;display:inline-block;box-shadow:0 2px 4px rgba(0,0,0,0.1);">
                            📱 Send via WhatsApp
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

    with col_btn2:
        if st.button("🔄  Preview Key Only", use_container_width=True):
            preview_key = generate_key(g_plan)
            st.code(preview_key, language=None)
            st.caption("This is a preview only. Click Generate & Save to actually create the license.")

# ════════════════════════════════════════════════════════════
# TAB 2 — MANAGE LICENSES
# ════════════════════════════════════════════════════════════

with tab_manage:
    st.markdown("#### 📋 All Licenses")

    lics = load_licenses()
    now = datetime.now()

    # Search & filter
    col_search, col_filter, col_status = st.columns([2, 1, 1])
    with col_search:
        search_q = st.text_input("🔍 Search by name, email or key", placeholder="Type to filter...")
    with col_filter:
        plan_filter = st.selectbox("Filter by Plan", ["All"] + list(PLANS.keys()))
    with col_status:
        status_filter = st.selectbox("Filter by Status", ["All", "Active", "Expired", "Inactive"])

    # Build dataframe
    rows = []
    for key, v in lics.items():
        expiry    = datetime.strptime(v["expiry"], "%Y-%m-%d")
        days_left = (expiry - now).days
        status    = "Active" if v.get("active") and days_left >= 0 else ("Expired" if days_left < 0 else "Inactive")

        # Apply filters
        if search_q and search_q.lower() not in (v.get("user","") + v.get("email","") + key).lower():
            continue
        if plan_filter != "All" and v.get("plan") != plan_filter:
            continue
        if status_filter != "All" and status != status_filter:
            continue

        rows.append({
            "Key":          key,
            "Client":       v.get("user", "—"),
            "Email":        v.get("email", "—"),
            "Broker":       v.get("broker", "—"),
            "Plan":         v.get("plan", "—"),
            "Expiry":       v["expiry"],
            "Days Left":    days_left,
            "Status":       status,
            "IB Partner":   "🤝 Yes" if v.get("ib_partner") else "—",
            "Paid ($)":     v.get("paid_amount", 0),
        })

    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, hide_index=True, use_container_width=True, height=380)
        st.caption(f"Showing {len(rows)} licenses")
    else:
        st.info("No licenses found matching the filters.")

    st.markdown("---")
    st.markdown("#### 🛠️ Quick Actions on a License")

    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    with col_a1:
        action_key = st.text_input("License Key", placeholder="VYTECH-XXX-XXXX-XXXX", key="action_key_input")
    with col_a2:
        if st.button("✅  Activate", use_container_width=True):
            lics = load_licenses()
            if action_key in lics:
                lics[action_key]["active"] = True
                save_licenses(lics)
                st.success(f"✅ {action_key} activated.")
            else:
                st.error("Key not found.")
    with col_a3:
        if st.button("🚫  Deactivate", use_container_width=True):
            lics = load_licenses()
            if action_key in lics:
                lics[action_key]["active"] = False
                save_licenses(lics)
                st.warning(f"⛔ {action_key} deactivated.")
            else:
                st.error("Key not found.")
    with col_a4:
        extend_days = st.number_input("Extend by (days)", value=30, min_value=1, key="extend_days")

    col_e1, col_e2 = st.columns([1, 3])
    with col_e1:
        if st.button("🗓️  Extend Expiry", use_container_width=True):
            lics = load_licenses()
            if action_key in lics:
                old_exp = datetime.strptime(lics[action_key]["expiry"], "%Y-%m-%d")
                base    = max(old_exp, datetime.now())
                new_exp = base + timedelta(days=extend_days)
                lics[action_key]["expiry"] = new_exp.strftime("%Y-%m-%d")
                save_licenses(lics)
                st.success(f"🗓️ Extended to {new_exp.strftime('%d %b %Y')}")
            else:
                st.error("Key not found.")

    if st.button("🗑️  Delete License (permanent)", type="secondary"):
        lics = load_licenses()
        if action_key in lics:
            del lics[action_key]
            save_licenses(lics)
            st.success(f"🗑️ {action_key} deleted.")
        else:
            st.error("Key not found.")

# ════════════════════════════════════════════════════════════
# TAB 3 — ALL CLIENTS
# ════════════════════════════════════════════════════════════

with tab_clients:
    st.markdown("#### 👥 Registered Clients")
    lics = load_licenses()
    now  = datetime.now()

    if not lics:
        st.info("No clients yet. Create licenses in the Generate tab.")
    else:
        rows = []
        for key, v in lics.items():
            expiry    = datetime.strptime(v["expiry"], "%Y-%m-%d")
            days_left = (expiry - now).days
            rows.append({
                "Client":       v.get("user", "—"),
                "Email":        v.get("email", "—"),
                "WhatsApp":     v.get("phone", "—"),
                "Broker":       v.get("broker", "—"),
                "Account ID":   v.get("account_id", "—"),
                "Plan":         v.get("plan", "—"),
                "Expiry":       v["expiry"],
                "Days Left":    days_left,
                "IB Partner":   "🤝" if v.get("ib_partner") else "—",
                "Paid ($)":     v.get("paid_amount", 0),
                "Key":          key,
                "Joined":       v.get("created_at", "—")[:10],
            })

        df_clients = pd.DataFrame(rows)
        st.dataframe(df_clients, hide_index=True, use_container_width=True, height=420)

        # Revenue by plan
        if rows:
            st.markdown("#### 💰 Revenue Breakdown by Plan")
            rev_data = {}
            for r in rows:
                plan = r["Plan"]
                rev_data[plan] = rev_data.get(plan, 0) + r["Paid ($)"]

            rc1, rc2, rc3, rc4, rc5 = st.columns(5)
            cols_rev = [rc1, rc2, rc3, rc4, rc5]
            for i, (plan, rev) in enumerate(rev_data.items()):
                if i < 5:
                    cols_rev[i].metric(plan, f"${rev:,.2f}")

# ════════════════════════════════════════════════════════════
# TAB 4 — PENDING APPROVALS (from client self-registration)
# ════════════════════════════════════════════════════════════

with tab_pending:
    st.markdown("#### ⏳ Pending Client Registrations")
    st.markdown("""
    <div class="vy-card">
        <div style="color:#475569;font-size:13px;font-weight:500;">
            These are clients who registered via the <b>Client Registration Portal</b> 
            and are waiting for your approval. Review each request and either approve (generate a key and send)
            or reject it.
        </div>
    </div>
    """, unsafe_allow_html=True)

    clients   = load_clients()
    pending   = [c for c in clients if c.get("status") == "pending"]
    approved  = [c for c in clients if c.get("status") == "approved"]
    rejected  = [c for c in clients if c.get("status") == "rejected"]

    pa1, pa2, pa3 = st.columns(3)
    pa1.metric("⏳ Pending",  len(pending))
    pa2.metric("✅ Approved", len(approved))
    pa3.metric("❌ Rejected", len(rejected))

    st.markdown("---")
    if not pending:
        st.success("✅ No pending registrations. You're all caught up!")
    else:
        for i, client in enumerate(pending):
            ib_flag = client.get("ib_partner", False)
            with st.expander(
                f"{'🤝 [IB] ' if ib_flag else ''}📩 {client.get('name','?')} — {client.get('email','?')} — {client.get('plan','?')} plan",
                expanded=(i == 0)
            ):
                d1, d2 = st.columns(2)
                with d1:
                    st.markdown(f"""
                    **Name:** {client.get('name', '—')}<br>
                    **Email:** {client.get('email', '—')}<br>
                    **WhatsApp:** {client.get('phone', '—')}<br>
                    **Broker:** {client.get('broker', '—')}<br>
                    **MT5 Account:** {client.get('account_id', '—')}
                    """, unsafe_allow_html=True)
                with d2:
                    st.markdown(f"""
                    **Plan Requested:** {client.get('plan', '—')}<br>
                    **IB Vantage Partner:** {'🤝 YES — Discount eligible' if ib_flag else 'No'}<br>
                    **Submitted:** {client.get('submitted_at', '—')}<br>
                    **Notes:** {client.get('notes', '—') or '—'}
                    """, unsafe_allow_html=True)

                btn_approve, btn_reject, btn_sp = st.columns([1, 1, 2])
                with btn_approve:
                    if st.button(f"✅ Approve & Generate Key", key=f"approve_{i}", type="primary"):
                        # Generate key
                        plan    = client.get("plan", "Monthly")
                        key     = generate_key(plan)
                        lics    = load_licenses()
                        while key in lics:
                            key = generate_key(plan)

                        days      = PLANS.get(plan, {}).get("days", 30)
                        expiry_dt = datetime.now() + timedelta(days=days)
                        price     = PLANS.get(plan, {}).get("price", 49)
                        if ib_flag:
                            price = round(price * (1 - IB_DISCOUNT_PERCENT / 100), 2)

                        lics[key] = {
                            "user":        client["name"],
                            "email":       client["email"],
                            "phone":       client.get("phone", ""),
                            "broker":      client.get("broker", ""),
                            "account_id":  client.get("account_id", ""),
                            "plan":        plan,
                            "expiry":      expiry_dt.strftime("%Y-%m-%d"),
                            "active":      True,
                            "ib_partner":  ib_flag,
                            "paid_amount": price,
                            "notes":       f"Self-registered via portal.",
                            "created_at":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        }
                        save_licenses(lics)

                        # Mark as approved in clients file
                        for c in clients:
                            if c.get("email") == client["email"]:
                                c["status"]   = "approved"
                                c["key"]      = key
                                c["approved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        save_clients(clients)

                        st.success(f"✅ Approved! Key: **{key}**")

                        phone_clean = client.get("phone", "").replace("+", "").replace("-", "").replace(" ", "")
                        wa_msg = (
                            f"🎉 *V.Y. Tech — Omega AI Platform*%0A%0A"
                            f"Hello {client['name']}!%0AYour subscription is approved.%0A%0A"
                            f"🔑 *License Key:*%0A`{key}`%0A%0A"
                            f"📅 Plan: {plan} | Valid until: {expiry_dt.strftime('%d %b %Y')}%0A%0A"
                            f"Enter this key in the trading platform to unlock it."
                        )
                        if phone_clean:
                            st.markdown(f"""
                            <a href="https://wa.me/{phone_clean}?text={wa_msg}" target="_blank"
                               style="background:#25d366;color:#fff;padding:8px 20px;border-radius:8px;
                                      font-size:12px;font-weight:600;text-decoration:none;display:inline-block;margin-top:8px;">
                               📱 Send Key via WhatsApp
                            </a>
                            """, unsafe_allow_html=True)

                        st.rerun()

                with btn_reject:
                    if st.button(f"❌ Reject", key=f"reject_{i}"):
                        for c in clients:
                            if c.get("email") == client["email"]:
                                c["status"] = "rejected"
                        save_clients(clients)
                        st.warning("Request rejected.")
                        st.rerun()

# ════════════════════════════════════════════════════════════
# TAB 5 — IB PARTNER TRACKER
# ════════════════════════════════════════════════════════════

with tab_ib:
    st.markdown("#### 🤝 IB Vantage Partner Tracking")
    st.markdown(f"""
    <div class="vy-card">
        <div style="display:flex;justify-content:space-between;align-items:start;">
            <div>
                <div style="color:#475569;font-size:14px;font-weight:700;margin-bottom:8px;">Your IB Referral Link</div>
                <div style="font-family:monospace;color:#0369a1;font-size:13px;background:#f8fafc;
                            padding:10px 16px;border-radius:8px;border:1px solid #cbd5e1;">
                    {IB_VANTAGE_LINK}
                </div>
                <div style="color:#64748b;font-size:12px;margin-top:8px;font-weight:500;">
                    Share this link with potential clients. When they register via this link,
                    they'll tick the IB checkbox in the registration form for their discount.
                </div>
            </div>
            <div style="text-align:center;background:#f0f9ff;border:1px solid #bae6fd;
                        border-radius:10px;padding:16px 24px;min-width:140px;">
                <div style="color:#0369a1;font-size:10px;text-transform:uppercase;letter-spacing:2px;font-weight:700;">IB Discount</div>
                <div style="font-size:32px;font-weight:900;color:#0284c7;">{IB_DISCOUNT_PERCENT}%</div>
                <div style="color:#0369a1;font-size:11px;font-weight:600;">off any plan</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # IB clients list
    lics     = load_licenses()
    ib_rows  = []
    ib_rev   = 0.0
    now      = datetime.now()
    for key, v in lics.items():
        if v.get("ib_partner"):
            expiry    = datetime.strptime(v["expiry"], "%Y-%m-%d")
            days_left = (expiry - now).days
            ib_rev   += v.get("paid_amount", 0)
            ib_rows.append({
                "Client":     v.get("user", "—"),
                "Broker":     v.get("broker", "—"),
                "Account ID": v.get("account_id", "—"),
                "Plan":       v.get("plan", "—"),
                "Paid ($)":   v.get("paid_amount", 0),
                "Expiry":     v["expiry"],
                "Days Left":  days_left,
                "Key":        key,
            })

    ib1, ib2, ib3 = st.columns(3)
    ib1.metric("🤝 Total IB Clients", len(ib_rows))
    ib2.metric("💰 IB Revenue",       f"${ib_rev:,.2f}")
    ib3.metric("🔖 Discount Applied", f"{IB_DISCOUNT_PERCENT}% per client")

    if ib_rows:
        st.dataframe(pd.DataFrame(ib_rows), hide_index=True, use_container_width=True)
    else:
        st.info("No IB partner clients yet. Share your Vantage IB link to start earning referral commissions.")

    st.markdown("---")
    st.markdown("#### 📋 How IB System Works (Step by Step)")
    st.markdown("""
    <div class="vy-card">
        <ol style="color:#475569;font-size:14px;line-height:2;font-weight:500;">
            <li>Share your <b style="color:#0284c7;">Vantage IB referral link</b> with potential traders.</li>
            <li>They open a Vantage account through your link (you earn commission from Vantage).</li>
            <li>They come to you for V.Y. Tech bot subscription.</li>
            <li>They fill the <b style="color:#0284c7;">Client Registration Portal</b> and tick "IB Vantage Partner".</li>
            <li>You approve their request — they get <b style="color:#15803d;">{discount}% discount</b> automatically.</li>
            <li>Their account is tracked here in the IB Tracker tab.</li>
            <li>You earn from both: <b style="color:#15803d;">Vantage IB commission + bot subscription</b>.</li>
        </ol>
    </div>
    """.format(discount=IB_DISCOUNT_PERCENT), unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# TAB 6 — SETTINGS
# ════════════════════════════════════════════════════════════

with tab_settings:
    st.markdown("#### ⚙️ Platform Settings")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("##### 💰 Edit Plan Prices")
        for plan_name, plan_data in PLANS.items():
            st.text(f"{plan_name}: {plan_data['label']} ({plan_data['days']} days)")
        st.caption("To change prices, edit the PLANS dict at the top of admin.py")

    with col_s2:
        st.markdown("##### 🛡️ Admin Password")
        st.caption("To change the admin password, edit ADMIN_PASSWORD at the top of admin.py and restart.")
        new_pw = st.text_input("New Password (preview)", type="password")
        if new_pw:
            st.code(f'ADMIN_PASSWORD = "{new_pw}"', language="python")
            st.caption("Copy the line above and replace in admin.py")

    st.markdown("---")
    st.markdown("##### 🗄️ Data Export")
    lics = load_licenses()
    if lics:
        rows = []
        for key, v in lics.items():
            rows.append({"Key": key, **{k: str(val) for k, val in v.items()}})
        df_export = pd.DataFrame(rows)
        csv = df_export.to_csv(index=False)
        st.download_button("⬇️  Export All Licenses (CSV)", data=csv, file_name="vy_licenses_export.csv", mime="text/csv")

    if st.button("🚪  Logout Admin", type="secondary"):
        st.session_state.admin_auth = False
        st.rerun()

# FOOTER
st.markdown("""
<div class="vy-footer">
    © 2026 &nbsp;<span style="color:#334155;font-weight:800;letter-spacing:2px;">V.Y. TECH</span>&nbsp; — Admin Panel &nbsp;|&nbsp; Keep this panel private.
</div>
""", unsafe_allow_html=True)