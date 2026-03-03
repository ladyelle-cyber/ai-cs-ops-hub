import streamlit as st
import json
from anthropic import Anthropic

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="Elle Phillips | AI Revenue Operations for Health Tech",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def get_client():
    return Anthropic(api_key=st.secrets.get("ANTHROPIC_API_KEY", ""))

# ============================================================
# GAINSIGHT-INSPIRED CSS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --white: #ffffff;
        --off-white: #fafbfc;
        --gray-50: #f8f9fa;
        --gray-100: #f1f3f5;
        --gray-200: #e9ecef;
        --gray-300: #dee2e6;
        --gray-400: #adb5bd;
        --gray-500: #868e96;
        --gray-600: #495057;
        --gray-700: #343a40;
        --gray-800: #212529;
        --teal-50: #e6fcf5;
        --teal-100: #c3fae8;
        --teal-200: #96f2d7;
        --teal-400: #38d9a9;
        --teal-500: #20c997;
        --teal-600: #0ca678;
        --teal-700: #099268;
        --teal-800: #087f5b;
        --violet-50: #f3f0ff;
        --violet-100: #e5dbff;
        --violet-500: #7950f2;
        --violet-600: #6741d9;
        --coral: #ff6b6b;
        --coral-light: #ffc9c9;
        --amber: #fcc419;
        --amber-light: #fff3bf;
        --blue-50: #e7f5ff;
        --blue-500: #339af0;
    }

    .stApp { background: var(--white) !important; font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; }
    .block-container { padding-top: 0 !important; padding-bottom: 0 !important; max-width: 1200px !important; }
    #MainMenu, footer, header { visibility: hidden; }
    section[data-testid="stSidebar"] { display: none !important; }

    /* ---- NAV ---- */
    .top-nav { display:flex; align-items:center; justify-content:space-between; padding:16px 0; border-bottom:1px solid var(--gray-200); }
    .nav-brand { font-size:18px; font-weight:800; color:var(--gray-800); letter-spacing:-0.5px; }
    .nav-brand span { color:var(--teal-600); }

    /* ---- HERO ---- */
    .hero-section { padding:80px 0 48px; text-align:center; }
    .hero-badge { display:inline-block; background:var(--teal-50); color:var(--teal-700); border:1px solid var(--teal-200); border-radius:100px; padding:6px 18px; font-size:13px; font-weight:600; margin-bottom:24px; }
    .hero-title { font-size:52px; font-weight:800; color:var(--gray-800); line-height:1.1; letter-spacing:-1.5px; margin-bottom:20px; max-width:800px; margin-left:auto; margin-right:auto; }
    .hero-title .hl { background:linear-gradient(135deg,var(--teal-500),var(--violet-500)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
    .hero-sub { font-size:18px; color:var(--gray-500); line-height:1.6; max-width:600px; margin:0 auto 40px; }

    /* ---- FLOATING CARDS ---- */
    .float-row { display:flex; justify-content:center; gap:20px; flex-wrap:wrap; margin-bottom:48px; }
    .fcard { background:var(--white); border:1px solid var(--gray-200); border-radius:16px; padding:24px; box-shadow:0 4px 24px rgba(0,0,0,0.05); width:220px; text-align:left; transition:all 0.3s; }
    .fcard:hover { transform:translateY(-4px); box-shadow:0 8px 32px rgba(0,0,0,0.08); }
    .fcard .fi { font-size:28px; margin-bottom:10px; }
    .fcard .ft { font-size:14px; font-weight:700; color:var(--gray-800); margin-bottom:4px; }
    .fcard .fd { font-size:12px; color:var(--gray-500); line-height:1.5; }

    /* ---- SECTIONS ---- */
    .sec-eye { font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; color:var(--teal-600); margin-bottom:12px; }
    .sec-title { font-size:36px; font-weight:800; color:var(--gray-800); letter-spacing:-0.8px; line-height:1.2; margin-bottom:12px; }
    .sec-desc { font-size:16px; color:var(--gray-500); line-height:1.7; max-width:640px; margin-bottom:40px; }

    /* ---- FEATURE CARDS ---- */
    .feat-grid { display:grid; grid-template-columns:1fr 1fr; gap:20px; margin:32px 0; }
    .feat { background:var(--white); border:1px solid var(--gray-200); border-radius:16px; padding:32px; transition:all 0.3s; position:relative; overflow:hidden; }
    .feat:hover { border-color:var(--teal-400); box-shadow:0 8px 32px rgba(12,166,120,0.06); transform:translateY(-2px); }
    .feat::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; border-radius:16px 16px 0 0; }
    .feat.c1::before { background:linear-gradient(90deg,var(--teal-400),var(--teal-600)); }
    .feat.c2::before { background:linear-gradient(90deg,var(--violet-500),#9775fa); }
    .feat.c3::before { background:linear-gradient(90deg,var(--coral),#ffa8a8); }
    .feat.c4::before { background:linear-gradient(90deg,var(--amber),#ffe066); }
    .feat .fnum { display:inline-flex; align-items:center; justify-content:center; width:36px; height:36px; border-radius:10px; font-size:16px; font-weight:700; margin-bottom:16px; }
    .feat.c1 .fnum { background:var(--teal-50); color:var(--teal-700); }
    .feat.c2 .fnum { background:var(--violet-50); color:var(--violet-600); }
    .feat.c3 .fnum { background:#fff5f5; color:var(--coral); }
    .feat.c4 .fnum { background:var(--amber-light); color:#e67700; }
    .feat h3 { font-size:18px; font-weight:700; color:var(--gray-800); margin-bottom:8px; }
    .feat p { font-size:14px; color:var(--gray-500); line-height:1.6; }
    .ftag { display:inline-block; background:var(--gray-100); color:var(--gray-600); border-radius:100px; padding:3px 10px; font-size:11px; font-weight:600; margin:12px 4px 0 0; }

    /* ---- METRICS ---- */
    .met-row { display:grid; grid-template-columns:repeat(5,1fr); gap:16px; margin:40px 0; }
    .met { text-align:center; padding:24px 16px; background:var(--white); border:1px solid var(--gray-200); border-radius:16px; }
    .met .mv { font-size:28px; font-weight:800; color:var(--teal-700); font-family:'JetBrains Mono',monospace; }
    .met .ml { font-size:12px; color:var(--gray-500); margin-top:4px; font-weight:500; }

    /* ---- TIMELINE ---- */
    .tl-row { display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin:32px 0; }
    .tlc { background:var(--white); border:1px solid var(--gray-200); border-radius:16px; overflow:hidden; transition:all 0.3s; }
    .tlc:hover { box-shadow:0 8px 24px rgba(0,0,0,0.05); transform:translateY(-2px); }
    .tlh { padding:14px 20px; font-size:13px; font-weight:700; color:var(--white); letter-spacing:0.5px; }
    .tlh.bg1 { background:var(--teal-600); }
    .tlh.bg2 { background:var(--gray-800); }
    .tlb { padding:20px; }
    .tlb li { font-size:13px; color:var(--gray-600); line-height:1.7; margin-bottom:6px; list-style:none; padding-left:20px; position:relative; }
    .tlb li::before { content:'→'; position:absolute; left:0; color:var(--teal-500); font-weight:600; }
    .tlb .tld { color:var(--teal-700); font-weight:700; }

    /* ---- COMPARE TABLE ---- */
    .ctbl { width:100%; border-collapse:separate; border-spacing:0; border-radius:12px; overflow:hidden; border:1px solid var(--gray-200); margin:24px 0; }
    .ctbl th { background:var(--gray-800); color:white; padding:14px 20px; font-size:13px; font-weight:600; text-align:left; }
    .ctbl td { padding:12px 20px; font-size:13px; color:var(--gray-600); border-bottom:1px solid var(--gray-100); }
    .ctbl td.nw { color:var(--teal-700); font-weight:600; }
    .ctbl tr:last-child td { border-bottom:none; }
    .ctbl tr:nth-child(even) td { background:var(--gray-50); }

    /* ---- BIO CARDS ---- */
    .bio-grid { display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px; margin:32px 0; }
    .bio { border-radius:16px; padding:28px; border:1px solid var(--gray-200); }
    .bio.b1 { background:linear-gradient(135deg,var(--teal-50),var(--white)); border-color:var(--teal-200); }
    .bio.b2 { background:linear-gradient(135deg,var(--violet-50),var(--white)); border-color:var(--violet-100); }
    .bio.b3 { background:linear-gradient(135deg,var(--blue-50),var(--white)); border-color:#c5deff; }
    .bio .bl { font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px; }
    .bio.b1 .bl { color:var(--teal-700); }
    .bio.b2 .bl { color:var(--violet-600); }
    .bio.b3 .bl { color:var(--blue-500); }
    .bio .bt { font-size:13px; color:var(--gray-600); line-height:1.7; }

    /* ---- DEMO CONTAINER ---- */
    .demo-box { background:var(--white); border:1px solid var(--gray-200); border-radius:20px; padding:40px; box-shadow:0 4px 24px rgba(0,0,0,0.03); margin:20px 0; }
    .demo-hdr { display:flex; align-items:center; gap:8px; margin-bottom:24px; }
    .ddot { width:10px; height:10px; border-radius:50%; }
    .ddot.r { background:#ff6b6b; } .ddot.y { background:#fcc419; } .ddot.g { background:#51cf66; }
    .dtitle { font-size:14px; font-weight:600; color:var(--gray-500); margin-left:8px; }

    /* ---- AI OUTPUT ---- */
    .aout { background:var(--gray-50); border:1px solid var(--gray-200); border-radius:12px; padding:24px; margin:16px 0; }
    .aout .al { font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:var(--teal-600); margin-bottom:8px; }
    .aout .at { font-size:14px; color:var(--gray-700); line-height:1.7; }

    /* ---- SCORE ---- */
    .srow { display:flex; align-items:center; gap:24px; margin:20px 0; }
    .scirc { width:72px; height:72px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-family:'JetBrains Mono',monospace; font-size:22px; font-weight:700; }
    .sh { background:var(--teal-50); border:2px solid var(--teal-500); color:var(--teal-700); }
    .sm { background:var(--amber-light); border:2px solid var(--amber); color:#e67700; }
    .sl { background:#fff5f5; border:2px solid var(--coral); color:var(--coral); }
    .tpill { display:inline-block; padding:6px 16px; border-radius:100px; font-size:13px; font-weight:600; }
    .tp-s { background:var(--teal-50); color:var(--teal-700); border:1px solid var(--teal-200); }
    .tp-h { background:var(--violet-50); color:var(--violet-600); border:1px solid var(--violet-100); }
    .tp-sc { background:var(--amber-light); color:#e67700; border:1px solid #ffe066; }
    .tp-m { background:#fff5f5; color:var(--coral); border:1px solid var(--coral-light); }

    /* ---- FOOTER ---- */
    .sfooter { text-align:center; padding:48px 0; border-top:1px solid var(--gray-200); margin-top:64px; }
    .sfooter .fn { font-size:16px; font-weight:700; color:var(--gray-800); margin-bottom:4px; }
    .sfooter .fd { font-size:13px; color:var(--gray-400); }

    /* ---- STREAMLIT OVERRIDES ---- */
    .stButton > button { background:var(--teal-600)!important; color:white!important; border:none!important; border-radius:100px!important; padding:12px 32px!important; font-family:'Plus Jakarta Sans',sans-serif!important; font-size:14px!important; font-weight:600!important; box-shadow:0 4px 14px rgba(12,166,120,0.25)!important; transition:all 0.3s!important; }
    .stButton > button:hover { background:var(--teal-700)!important; transform:translateY(-2px)!important; box-shadow:0 6px 20px rgba(12,166,120,0.3)!important; }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea { border-radius:12px!important; border-color:var(--gray-200)!important; font-family:'Plus Jakarta Sans',sans-serif!important; }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus { border-color:var(--teal-500)!important; box-shadow:0 0 0 3px rgba(32,201,151,0.15)!important; }
    .stSelectbox label, .stTextInput label, .stTextArea label, .stMultiSelect label { font-family:'Plus Jakarta Sans',sans-serif!important; font-weight:600!important; font-size:13px!important; color:var(--gray-700)!important; }
    .stTabs [data-baseweb="tab-list"] { gap:0; border-bottom:2px solid var(--gray-200); }
    .stTabs [data-baseweb="tab"] { font-family:'Plus Jakarta Sans',sans-serif!important; font-weight:600!important; font-size:14px!important; padding:12px 24px!important; color:var(--gray-500)!important; }
    .stTabs [aria-selected="true"] { color:var(--teal-700)!important; border-bottom-color:var(--teal-600)!important; }
    div[data-testid="stExpander"] { border:1px solid var(--gray-200)!important; border-radius:12px!important; margin-bottom:8px; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SYSTEM PROMPTS
# ============================================================
ACCT_PROMPT = """You are an AI Account Intelligence Engine for health tech CS. Analyze account attributes and return strategic engagement recommendations grounded in VBC dynamics.

Return ONLY valid JSON: {"readiness_score": (0-100), "engagement_tier": "High Touch"|"Strategic"|"Scaled"|"Monitor", "risk_signals": [2-3], "expansion_signals": [2-3], "recommended_motion": "brief approach", "talk_track_angle": "clinical"|"administrative"|"financial", "stakeholder_target": "who and why", "90_day_priorities": [3 actions]}

Reference RAF accuracy, HEDIS, care gaps, provider burnout, MA Stars, risk adjustment. No markdown."""

ENABLE_PROMPT = """You are an AI Enablement Workflow Generator for health tech. Take product release info and generate enablement packages.

Return ONLY valid JSON: {"what_changed": "", "why_it_matters": "", "who_its_for": {"best_fit": [3], "walk_away": [3]}, "clinical_talk_track": "3-4 sentences", "admin_talk_track": "3-4 sentences", "when_not_to_sell": [3], "discovery_questions": [{"question":"","rationale":""}], "objection_responses": [{"objection":"","response":""}], "proof_points": [3-4]}

Healthcare/VBC specific. No markdown."""

DISC_PROMPT = """You are an AI Discovery & Objection Engine for health tech CSMs. Navigate complex customer conversations.

Return ONLY valid JSON: {"scenario_assessment": "2-3 sentences", "stakeholder_analysis": {"current_contact":"","ideal_contact":"","navigation_strategy":""}, "discovery_sequence": [{"question":"","intent":"","if_they_say_x":""}], "risk_flags": [2-3], "positioning_recommendation": {"lead_with":"","avoid":"","proof_point":""}, "objection_prep": [{"objection":"","response":"","underlying_concern":""}], "next_best_action": ""}

Healthcare specific. No markdown."""

FIELD_PROMPT = """You are an AI Field Intelligence Aggregator for health tech CS leadership. Analyze field patterns for strategic insights.

Return ONLY valid JSON: {"executive_summary": "3-4 sentences", "pattern_analysis": [{"pattern":"","frequency":"","impact":"","root_cause":""}], "product_intelligence": {"feature_requests":[],"competitive_threats":[],"positioning_gaps":[]}, "recommended_actions": [{"action":"","owner":"Product|CS|GTM|Engineering","priority":"P0|P1|P2","expected_impact":""}], "gtm_implications": "2-3 sentences", "metrics_to_watch": [3]}

Healthcare/VBC grounded. No markdown."""


# ============================================================
# HELPERS
# ============================================================
def call_claude(sys, msg):
    try:
        client = get_client()
        resp = client.messages.create(model="claude-sonnet-4-6", max_tokens=2000, system=sys, messages=[{"role":"user","content":msg}])
        txt = resp.content[0].text.strip()
        if txt.startswith("```"): txt = txt.split("\n",1)[1].rsplit("```",1)[0]
        return json.loads(txt)
    except json.JSONDecodeError:
        return {"error": "Parse failed: " + txt[:500]}
    except Exception as e:
        return {"error": f"API Error: {e}. Check ANTHROPIC_API_KEY."}

def sc(s):
    if s >= 70: return "sh"
    if s >= 40: return "sm"
    return "sl"

def tc(t):
    return {"High Touch":"tp-h","Strategic":"tp-s","Scaled":"tp-sc","Monitor":"tp-m"}.get(t,"tp-s")


# ============================================================
# NAV BAR
# ============================================================
st.markdown("""
<div class="top-nav">
    <div class="nav-brand">✦ Elle <span>Phillips</span></div>
    <div style="font-size:13px; color:#868e96;">AI Revenue Operations for Health Tech</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tabs = st.tabs(["Overview", "Live Demos", "Architecture", "About"])

# ============================================================
# OVERVIEW
# ============================================================
with tabs[0]:

    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">✦ Built from 14 years in the field</div>
        <h1 class="hero-title">I build the <span class="hl">AI systems</span> that make health tech CS actually work.</h1>
        <p class="hero-sub">Most CS orgs run on tribal knowledge, static playbooks, and heroics. I got tired of watching that fail. So I started building the operating systems that should exist instead.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="float-row">
        <div class="fcard"><div class="fi">🎯</div><div class="ft">Account Intelligence</div><div class="fd">Stop guessing which accounts are ready. Let the data tell you who to call and what to say.</div></div>
        <div class="fcard"><div class="fi">🔄</div><div class="ft">Enablement Automation</div><div class="fd">New release drops? Your team has talk tracks, objection responses, and discovery guides before lunch.</div></div>
        <div class="fcard"><div class="fi">💬</div><div class="ft">Conversation Intelligence</div><div class="fd">Your newest CSM walks into a call with the same strategic playbook as your best one.</div></div>
        <div class="fcard"><div class="fi">📊</div><div class="ft">Field Intelligence</div><div class="fd">What customers are actually saying — structured, prioritized, and routed to the people who can fix it.</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div class="sec-eye">THE PROBLEM</div>
    <div class="sec-title">Great products fail when CS can't keep up.</div>
    <div class="sec-desc">I've watched it happen at every company I've worked at. Product ships something great. CS scrambles to figure out how to position it. Half the team wings it. The other half waits for a training that comes three weeks too late. Meanwhile, customers churn — not because the product is bad, but because nobody translated the value for them. This system fixes that.</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feat-grid">
        <div class="feat c1"><div class="fnum">01</div><h3>Account Intelligence Engine</h3><p>Here's what usually happens: a CSM looks at an account, checks their gut, and decides how to engage. Problem is, your best CSM's gut is different from your newest hire's. This module takes account data — VBC maturity, payer mix, tech stack, known pain — and gives everyone the same quality read. Score, tier, talk track angle, and who to call first.</p><span class="ftag">Automated Scoring</span><span class="ftag">Risk Detection</span><span class="ftag">Expansion Signals</span></div>
        <div class="feat c2"><div class="fnum">02</div><h3>Enablement Workflow Generator</h3><p>Every product release needs talk tracks, discovery questions, objection responses, and a clear "don't sell this to these people" list. Building that manually takes weeks. This module does 80% of the work in minutes — you describe the release, it generates the full package. Your team spends time practicing, not waiting.</p><span class="ftag">Release-to-Revenue</span><span class="ftag">Talk Tracks</span><span class="ftag">Objection Library</span></div>
        <div class="feat c3"><div class="fnum">03</div><h3>Discovery & Objection Engine</h3><p>Your CSM is about to walk into a call with a skeptical practice manager who just had a failed EHR migration. What do they lead with? What do they avoid? Who should actually be in the room? This is the AI copilot that answers those questions in real time — before the call, not after the post-mortem.</p><span class="ftag">Stakeholder Navigation</span><span class="ftag">Real-Time Guidance</span><span class="ftag">Objection Handling</span></div>
        <div class="feat c4"><div class="fnum">04</div><h3>Field Intelligence Loop</h3><p>CSMs hear the most important things your company will ever learn — and most of it dies in a Slack thread. This module takes field observations and turns them into structured intelligence: what patterns are emerging, what competitors are doing, what Product needs to hear, and what GTM should change. No more "I think customers are saying..."</p><span class="ftag">Pattern Analysis</span><span class="ftag">Product Intel</span><span class="ftag">GTM Signals</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div class="sec-eye">HOW IT RUNS</div>
    <div class="sec-title">Same system, every release. 3 weeks.</div>
    <div class="sec-desc">The architecture stays the same — only the content changes. That's the whole point. You don't reinvent the wheel every time Product ships something. You run the motion.</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tl-row">
        <div class="tlc"><div class="tlh bg1">WEEK 1 — DIAGNOSE & ALIGN</div><div class="tlb"><li>Account Intelligence scores eligible accounts</li><li>Product delivers intent brief</li><li>CS surfaces top objections from field</li><li>RevOps provides baseline metrics</li><li class="tld">→ Scored account list + alignment doc</li></div></div>
        <div class="tlc"><div class="tlh bg2">WEEK 2 — BUILD & TEST</div><div class="tlb"><li>Enablement Generator creates full package</li><li>Pilot with 3-5 CSMs on real calls</li><li>Discovery Engine provides live support</li><li>Iterate based on field feedback</li><li class="tld">→ Field-tested enablement package</li></div></div>
        <div class="tlc"><div class="tlh bg1">WEEK 3 — ROLLOUT & REINFORCE</div><div class="tlb"><li>Live enablement session (90 min)</li><li>Manager coaching prompts distributed</li><li>Field Intelligence Loop activated</li><li>All CSMs get Discovery Engine access</li><li class="tld">→ Trained team + active feedback loop</li></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div class="sec-eye">WHAT GETS MEASURED</div>
    <div class="sec-title">If you're tracking calls and emails, you're tracking the wrong things.</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="met-row">
        <div class="met"><div class="mv">70%</div><div class="ml">Positioning Coverage</div></div>
        <div class="met"><div class="mv">60%</div><div class="ml">90-Day Adoption</div></div>
        <div class="met"><div class="mv">-40%</div><div class="ml">Confusion Tickets</div></div>
        <div class="met"><div class="mv">↑ QoQ</div><div class="ml">Commercial Influence</div></div>
        <div class="met"><div class="mv">↓ QoQ</div><div class="ml">Churn Risk</div></div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# LIVE DEMOS
# ============================================================
with tabs[1]:

    st.markdown("""
    <div style="padding:40px 0 20px;">
        <div class="sec-eye">TRY IT</div>
        <div class="sec-title">These aren't mockups. They're working.</div>
        <div class="sec-desc">Each module below is powered by Claude. Put in a real scenario — an account you're working, a release you're planning, a conversation you're prepping for — and see what comes back. The AI is grounded in VBC and health tech, not generic CS advice.</div>
    </div>
    """, unsafe_allow_html=True)

    dtabs = st.tabs(["🎯 Account Intelligence", "🔄 Enablement Generator", "💬 Discovery Engine", "📊 Field Intelligence"])

    # --- ACCOUNT INTELLIGENCE ---
    with dtabs[0]:
        st.markdown("""<div class="demo-box"><div class="demo-hdr"><div class="ddot r"></div><div class="ddot y"></div><div class="ddot g"></div><div class="dtitle">Account Intelligence Engine</div></div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            org = st.text_input("Organization", value="Heartland ACO Partners", key="a1")
            otype = st.selectbox("Type", ["ACO","MSO","Health System","Practice Group","Health Plan","IPA"], index=0, key="a2")
            vbc = st.selectbox("VBC Maturity", ["Pre-VBC (FFS dominant)","Early VBC (<20%)","Scaling VBC (20-50%)","Mature VBC (>50%)"], index=2, key="a3")
        with c2:
            payer = st.selectbox("Payer Mix", ["MA heavy (>40%)","Commercial dominant","Medicaid heavy","Balanced"], index=0, key="a4")
            size = st.select_slider("Providers", options=["<25","25-50","50-100","100-250","250-500","500+"], value="100-250", key="a5")
            stage = st.selectbox("Stage", ["Pre-sale","Implementation","Early adoption","Established","Renewal"], index=3, key="a6")
        pain = st.text_area("Pain Points", value="HCC coding completion at 64% against an 80% target — on par with national average but below shared savings threshold. MA Star rating holding at 3.5 (national median), missing the 4.0 cutoff for full bonus payments. HEDIS gap closure at 51%. RAF score variance running 18% against attributed population benchmarks. Platform login rate plateaued at 42% at month 10. 3 of 7 high-value quality measures below minimum performance levels for upcoming CMS reporting window. CFO questioning ROI ahead of annual contract review.", key="a7", height=100)

        if st.button("⚡ Generate Account Intelligence", type="primary", use_container_width=True, key="a8"):
            with st.spinner("Analyzing account..."):
                r = call_claude(ACCT_PROMPT, f"Org:{org or 'Unnamed'}, Type:{otype}, VBC:{vbc}, Payer:{payer}, Size:{size}, Stage:{stage}, Pain:{pain or 'None'}")
                if "error" in r:
                    st.error(r["error"])
                else:
                    s = r.get("readiness_score",0); t = r.get("engagement_tier","Strategic")
                    st.markdown(f'<div class="srow"><div class="scirc {sc(s)}">{s}</div><div><div style="font-size:14px;font-weight:700;color:#343a40;margin-bottom:4px;">Readiness: {s}/100</div><span class="tpill {tc(t)}">{t}</span></div></div>', unsafe_allow_html=True)
                    x1,x2 = st.columns(2)
                    with x1:
                        st.markdown("**🔴 Risk Signals**")
                        for i in r.get("risk_signals",[]): st.markdown(f"• {i}")
                    with x2:
                        st.markdown("**🟢 Expansion Signals**")
                        for i in r.get("expansion_signals",[]): st.markdown(f"• {i}")
                    st.markdown(f'<div class="aout"><div class="al">Recommended Motion</div><div class="at">{r.get("recommended_motion","")}</div></div>', unsafe_allow_html=True)
                    st.markdown(f"**Stakeholder Target:** {r.get('stakeholder_target','')}")
                    for i,p in enumerate(r.get("90_day_priorities",[]),1): st.markdown(f"**P{i-1}:** {p}")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ENABLEMENT GENERATOR ---
    with dtabs[1]:
        st.markdown("""<div class="demo-box"><div class="demo-hdr"><div class="ddot r"></div><div class="ddot y"></div><div class="ddot g"></div><div class="dtitle">Enablement Workflow Generator</div></div>""", unsafe_allow_html=True)
        rname = st.text_input("Release Name", value="AI-Powered Care Gap Prioritization", key="e1")
        rdesc = st.text_area("What changed?", value="New feature that surfaces real-time patient-level care gaps ranked by closure likelihood and revenue impact. Pulls from claims and EHR data to show providers exactly which patients need which interventions before the HEDIS measurement window closes. Designed for quality teams at MA-heavy ACOs and health plans managing Star ratings. Replaces manual gap lists that are 60-90 days stale by the time they reach the provider.", height=140, key="e2")
        persona = st.selectbox("Buyer", ["Clinical Leaders","Admin Leaders","IT/Informatics","Practice Managers"], index=0, key="e3")

        if st.button("⚡ Generate Enablement Package", type="primary", use_container_width=True, key="e4"):
            if not rdesc: st.warning("Describe the release.")
            else:
                with st.spinner("Building package..."):
                    r = call_claude(ENABLE_PROMPT, f"Release:{rname or 'Unnamed'}, Desc:{rdesc}, Persona:{persona}")
                    if "error" in r: st.error(r["error"])
                    else:
                        st.markdown(f'<div class="aout"><div class="al">What Changed</div><div class="at">{r.get("what_changed","")}</div></div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="aout"><div class="al">Why It Matters</div><div class="at">{r.get("why_it_matters","")}</div></div>', unsafe_allow_html=True)
                        f1,f2 = st.columns(2)
                        with f1:
                            st.markdown("**✅ Best Fit**")
                            for i in r.get("who_its_for",{}).get("best_fit",[]): st.markdown(f"• {i}")
                        with f2:
                            st.markdown("**🚫 Walk Away**")
                            for i in r.get("who_its_for",{}).get("walk_away",[]): st.markdown(f"• {i}")
                        t1,t2 = st.columns(2)
                        with t1: st.markdown(f'<div class="aout"><div class="al">Clinical Talk Track</div><div class="at">{r.get("clinical_talk_track","")}</div></div>', unsafe_allow_html=True)
                        with t2: st.markdown(f'<div class="aout"><div class="al">Admin Talk Track</div><div class="at">{r.get("admin_talk_track","")}</div></div>', unsafe_allow_html=True)
                        st.markdown("**🛑 When NOT to Sell**")
                        for i in r.get("when_not_to_sell",[]): st.markdown(f"• {i}")
                        st.markdown("**🔍 Discovery Questions**")
                        for q in r.get("discovery_questions",[]):
                            if isinstance(q,dict):
                                with st.expander(q.get("question","")): st.markdown(f"*{q.get('rationale','')}*")
                        st.markdown("**🛡️ Objections**")
                        for o in r.get("objection_responses",[]):
                            if isinstance(o,dict):
                                with st.expander(o.get("objection","")): st.markdown(o.get("response",""))
        st.markdown('</div>', unsafe_allow_html=True)

    # --- DISCOVERY ENGINE ---
    with dtabs[2]:
        st.markdown("""<div class="demo-box"><div class="demo-hdr"><div class="ddot r"></div><div class="ddot y"></div><div class="ddot g"></div><div class="dtitle">Discovery & Objection Engine</div></div>""", unsafe_allow_html=True)
        scen = st.text_area("Customer scenario", value="Meeting next Tuesday with VP of Quality at Lone Star IPA — 160-physician independent practice association in Dallas. 7 months post-implementation, platform adoption stuck at 28%. CMO just launched a vendor consolidation initiative and our tool is on the review list. They have a BlueCross shared savings contract renewal in Q3 where Star ratings directly affect their bonus pool — currently at 3.5 stars, need 4.0 to unlock the full payout. My champion is the VP of Quality but the CFO owns the final call and I've never met her.", height=140, key="d1")
        d1,d2 = st.columns(2)
        with d1: goal = st.selectbox("Goal", ["Initial discovery","Product positioning","Objection handling","Expansion","Renewal defense"], index=4, key="d2")
        with d2: urg = st.selectbox("Urgency", ["Standard","At-risk","Competitive threat","Escalation"], index=1, key="d3")

        if st.button("⚡ Generate Conversation Intelligence", type="primary", use_container_width=True, key="d4"):
            if not scen: st.warning("Describe the scenario.")
            else:
                with st.spinner("Analyzing..."):
                    r = call_claude(DISC_PROMPT, f"Scenario:{scen}, Goal:{goal}, Urgency:{urg}")
                    if "error" in r: st.error(r["error"])
                    else:
                        st.markdown(f'<div class="aout"><div class="al">Assessment</div><div class="at">{r.get("scenario_assessment","")}</div></div>', unsafe_allow_html=True)
                        sh = r.get("stakeholder_analysis",{})
                        s1,s2 = st.columns(2)
                        with s1:
                            st.markdown(f"**Current:** {sh.get('current_contact','')}")
                            st.markdown(f"**Ideal:** {sh.get('ideal_contact','')}")
                        with s2:
                            st.markdown(f'<div class="aout"><div class="al">Navigation</div><div class="at">{sh.get("navigation_strategy","")}</div></div>', unsafe_allow_html=True)
                        st.markdown("**🔍 Discovery Sequence**")
                        for i,q in enumerate(r.get("discovery_sequence",[]),1):
                            if isinstance(q,dict):
                                with st.expander(f"Q{i}: {q.get('question','')}"):
                                    st.markdown(f"**Intent:** {q.get('intent','')}")
                                    st.markdown(f"**Pivot:** {q.get('if_they_say_x','')}")
                        pos = r.get("positioning_recommendation",{})
                        st.markdown(f"**Lead with:** {pos.get('lead_with','')}")
                        st.markdown(f"**Avoid:** {pos.get('avoid','')}")
                        st.markdown("**🛡️ Objection Prep**")
                        for o in r.get("objection_prep",[]):
                            if isinstance(o,dict):
                                with st.expander(o.get("objection","")):
                                    st.markdown(f"**Response:** {o.get('response','')}")
                                    st.markdown(f"**Real concern:** {o.get('underlying_concern','')}")
                        st.markdown(f'<div class="aout"><div class="al">Next Best Action</div><div class="at">{r.get("next_best_action","")}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- FIELD INTELLIGENCE ---
    with dtabs[3]:
        st.markdown("""<div class="demo-box"><div class="demo-hdr"><div class="ddot r"></div><div class="ddot y"></div><div class="ddot g"></div><div class="dtitle">Field Intelligence Feedback Loop</div></div>""", unsafe_allow_html=True)
        obs = st.text_area("Field Observations", value="- 4 customers this month asked about ambient documentation integration — comparing us to Nuance DAX, saying physicians won't adopt any new platform without it\n- Lost a deal to Arcadia last week — they bundled risk adjustment + quality analytics + contract management at a flat PMPM, we quoted three separate line items\n- VP of Quality at two ACOs said their CMOs won't engage until they see a physician-facing view — the platform feels built for the quality team, not the providers closing gaps\n- Implementation flagged health system deployments averaging 4.5 months vs 6 weeks for independent practices — no documented root cause\n- Three customers going into payer contract renegotiations in Q3, asking for ROI documentation — they don't have it and need help building the case\n- CSM on Midwest account reported CMO said: 'I love what I see but my CFO thinks this is a reporting tool, not a revenue tool'", height=200, key="f1")
        per = st.selectbox("Period", ["This week","Last 2 weeks","This month","This quarter"], index=2, key="f2")

        if st.button("⚡ Generate Intelligence Brief", type="primary", use_container_width=True, key="f3"):
            if not obs: st.warning("Enter observations.")
            else:
                with st.spinner("Analyzing patterns..."):
                    r = call_claude(FIELD_PROMPT, f"Period:{per}\nObs:\n{obs}")
                    if "error" in r: st.error(r["error"])
                    else:
                        st.markdown(f'<div class="aout"><div class="al">Executive Summary</div><div class="at">{r.get("executive_summary","")}</div></div>', unsafe_allow_html=True)
                        st.markdown("**📊 Patterns**")
                        for p in r.get("pattern_analysis",[]):
                            if isinstance(p,dict):
                                with st.expander(p.get("pattern","")):
                                    st.markdown(f"**Frequency:** {p.get('frequency','')}")
                                    st.markdown(f"**Impact:** {p.get('impact','')}")
                                    st.markdown(f"**Root Cause:** {p.get('root_cause','')}")
                        pi = r.get("product_intelligence",{})
                        p1,p2,p3 = st.columns(3)
                        with p1:
                            st.markdown("**Features**")
                            for f in pi.get("feature_requests",[]): st.markdown(f"• {f}")
                        with p2:
                            st.markdown("**Threats**")
                            for f in pi.get("competitive_threats",[]): st.markdown(f"• {f}")
                        with p3:
                            st.markdown("**Gaps**")
                            for f in pi.get("positioning_gaps",[]): st.markdown(f"• {f}")
                        st.markdown("**✅ Actions**")
                        for a in r.get("recommended_actions",[]):
                            if isinstance(a,dict): st.markdown(f"**[{a.get('priority','P2')}]** {a.get('action','')} — *{a.get('owner','')}*")
                        st.markdown(f'<div class="aout"><div class="al">GTM Implications</div><div class="at">{r.get("gtm_implications","")}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# ARCHITECTURE
# ============================================================
with tabs[2]:
    st.markdown("""
    <div style="padding:40px 0 20px;">
        <div class="sec-eye">HOW I THINK ABOUT THIS</div>
        <div class="sec-title">The old way doesn't scale. Here's what does.</div>
        <div class="sec-desc">I've managed CS at every stage — 15-person teams, $25M accounts, 300+ practice rollouts. The bottleneck is never the people. It's that we keep asking humans to do things that systems should handle, and then wonder why quality varies.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <table class="ctbl">
        <thead><tr><th>Traditional CS Enablement</th><th>AI-Native Revenue Operations</th></tr></thead>
        <tbody>
            <tr><td>Manual account segmentation</td><td class="nw">Signal-based automated scoring</td></tr>
            <tr><td>Static playbooks updated quarterly</td><td class="nw">Dynamic enablement generated per release</td></tr>
            <tr><td>CSM judgment varies by experience</td><td class="nw">AI-augmented judgment, consistent quality</td></tr>
            <tr><td>Anecdotal feedback to Product</td><td class="nw">Structured intelligence pipelines</td></tr>
            <tr><td>Headcount-scaled coverage</td><td class="nw">System-scaled + human-led strategic overlay</td></tr>
            <tr><td>Activity metrics (calls, emails)</td><td class="nw">Revenue signals (adoption, expansion, churn)</td></tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("""
    This isn't about replacing CSMs — I've been one, I've managed them, I've built the teams. It's about making sure
    your day-one hire has access to the same strategic thinking that took your best performer five years to develop.
    That's what systems do. They make the floor higher.
    """)

    st.markdown("---")

    st.markdown("""
    <div class="sec-eye">SYSTEM FLOW</div>
    <div class="sec-title">Signal → Score → Workflow → Feedback</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ```
    ┌──────────────────────────────────────────┐
    │           📦 PRODUCT RELEASE              │
    └──────────────────────┬───────────────────┘
                           ↓
    ┌──────────────────────────────────────────┐
    │   🎯 Account Intelligence Engine         │
    │   Scoring → Tiers → Priority Targets     │
    └──────────────────────┬───────────────────┘
                           ↓
    ┌──────────────────────────────────────────┐
    │   🔄 Enablement Workflow Generator        │
    │   Talk Tracks → Discovery → Objections    │
    └──────────────────────┬───────────────────┘
                           ↓
    ┌──────────────────────────────────────────┐
    │   💬 Discovery & Objection Engine         │
    │   Real-Time CSM Copilot                   │
    └──────────────────────┬───────────────────┘
                           ↓
    ┌──────────────────────────────────────────┐
    │   📊 Field Intelligence Loop              │
    │   Patterns → Actions → Briefs             │
    └──────────────────────┬───────────────────┘
                           ↓
    ┌──────────────────────────────────────────┐
    │         💰 REVENUE IMPACT                 │
    │   Adoption → Retention → Expansion        │
    └──────────────────────────────────────────┘
    ```
    """)


# ============================================================
# ABOUT
# ============================================================
with tabs[3]:
    st.markdown("""
    <div style="padding:40px 0 20px;">
        <div class="sec-eye">WHO BUILT THIS</div>
        <div class="sec-title">I've sat in every chair at the VBC table.</div>
        <div class="sec-desc">Payer side, provider side, platform side. I've been the person on the other end of the QBR, the person running the QBR, and the person redesigning how QBRs work. Every module in this system solves a problem I've personally watched go wrong — more than once.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bio-grid">
        <div class="bio b1"><div class="bl">Payer</div><div class="bt">6 years inside Elevance Health. Built a 15-person account ops team from scratch for their VBC portfolio. Inherited a 60% satisfaction score on the largest account and got it to 92%. I know how payers think about risk, cost, and why they ghost your renewal call.</div></div>
        <div class="bio b2"><div class="bl">Provider</div><div class="bt">Privia Health, pre-IPO. Scaled practice transformation playbooks across 300+ practices. Transitioned physicians who'd been doing fee-for-service for 20 years into value-based workflows. I've sat with the crying doctor who hates the new system. I get it.</div></div>
        <div class="bio b3"><div class="bl">Platform</div><div class="bt">Cotiviti/Edifecs. Own a $25M health plan engagement — 22M members, 35+ stakeholders, 4 platforms, 6 internal teams all talking past each other. Built the enablement and operating infrastructure that drove 116% YoY adoption growth. This is where the system idea was born.</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### What I'm Building Toward")
    st.markdown("""
    I want to run operations at a health tech company where this kind of thinking matters.
    Not just using AI as a buzzword in a job description — actually designing the systems that connect
    product to customer to revenue, and making them repeatable enough that they work without me in the room.

    That's what a good operating system does. It works when you're not watching.
    """)

    st.markdown("---")

    st.markdown("### Connect")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/elle-phillips/) · elle.phillips@email.com")


# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="sfooter">
    <div class="fn">✦ Elle Phillips</div>
    <div class="fd">AI Revenue Operations for Health Tech</div>
</div>
""", unsafe_allow_html=True)
