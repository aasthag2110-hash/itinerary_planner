import uuid

import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from graph import app


st.set_page_config(
    page_title="Roamly — AI Travel Planner",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    :root {
        --ink: #1f2933;
        --muted: #66756f;
        --forest: #17483b;
        --mint: #dceee6;
        --cream: #f8f5ee;
        --coral: #ef7d61;
        --line: rgba(23, 72, 59, 0.13);
    }

    .stApp {
        background:
            radial-gradient(circle at 88% 3%, rgba(239, 125, 97, .12), transparent 24rem),
            linear-gradient(180deg, #fbfaf6 0%, #f5f7f3 100%);
        color: var(--ink);
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    h1, h2, h3 { letter-spacing: -0.02em; }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"], [data-testid="stAppDeployButton"],
    [data-testid="stMainMenu"], #MainMenu { display: none !important; }
    [data-testid="stSidebar"] {
        background: #123d33;
        border-right: 0;
    }
    [data-testid="stSidebar"] * { color: #f6f4ed; }
    [data-testid="stSidebar"] input {
        color: #172521 !important;
        background: rgba(255,255,255,.94) !important;
    }
    [data-testid="stSidebar"] .stButton button {
        border: 1px solid rgba(255,255,255,.25);
        background: rgba(255,255,255,.09);
        color: white;
    }
    .block-container { max-width: 1160px; padding-top: 2.2rem; padding-bottom: 5rem; }

    .brand { display:flex; align-items:center; gap:.7rem; margin-bottom:2.7rem; }
    .brand-mark {
        width: 2.35rem; height: 2.35rem; border-radius: 12px;
        display:grid; place-items:center; background:#f39a7f; color:#153e34;
        font-size:1.2rem; box-shadow:0 10px 30px rgba(0,0,0,.12);
    }
    .brand-name { font-size:1.22rem; font-weight:700; letter-spacing:-.03em; }
    .eyebrow {
        display:inline-flex; align-items:center; gap:.45rem; color:var(--forest);
        background:var(--mint); border:1px solid rgba(23,72,59,.08);
        border-radius:999px; padding:.4rem .75rem; font-size:.76rem;
        font-weight:700; letter-spacing:.08em; text-transform:uppercase;
    }
    .hero-title {
        font-family:'Playfair Display', serif; font-size:clamp(2.7rem, 5vw, 4.8rem);
        line-height:1.02; max-width:780px; color:#173c33; margin:.9rem 0 .8rem;
        letter-spacing:-.045em;
    }
    .hero-copy { max-width:650px; color:var(--muted); font-size:1.08rem; line-height:1.7; margin-bottom:1.8rem; }
    .section-label { color:var(--forest); font-size:.78rem; font-weight:700; letter-spacing:.09em; text-transform:uppercase; margin:2rem 0 .4rem; }
    .section-title { font-family:'Playfair Display', serif; color:#173c33; font-size:2rem; margin:0 0 .25rem; }
    .section-copy { color:var(--muted); margin:0 0 1.1rem; }
    .thread-pill {
        border:1px solid rgba(255,255,255,.16); border-radius:12px; padding:.7rem .8rem;
        color:rgba(255,255,255,.72); font-size:.72rem; line-height:1.45;
        overflow-wrap:anywhere; margin-top:.65rem;
    }
    .sidebar-note { color:rgba(255,255,255,.64); font-size:.82rem; line-height:1.55; margin:1.8rem 0 .5rem; }
    .status-card {
        display:flex; gap:.8rem; align-items:flex-start; background:white;
        border:1px solid var(--line); border-radius:16px; padding:1rem 1.1rem;
        box-shadow:0 8px 30px rgba(35,61,52,.05); margin:.5rem 0 1.2rem;
    }
    .status-dot { width:10px; height:10px; margin-top:.38rem; border-radius:50%; background:#54a985; box-shadow:0 0 0 5px #e5f5ed; }
    .status-title { color:var(--ink); font-weight:700; font-size:.92rem; }
    .status-copy { color:var(--muted); font-size:.84rem; margin-top:.15rem; }

    div[data-testid="stTextArea"] textarea {
        min-height:150px; border-radius:18px; border:1px solid var(--line);
        background:rgba(255,255,255,.9); font-size:1rem; line-height:1.6;
        padding:1rem; box-shadow:0 12px 35px rgba(35,61,52,.05);
    }
    div[data-testid="stTextArea"] textarea:focus { border-color:#4b9079; box-shadow:0 0 0 3px rgba(75,144,121,.12); }
    .stButton > button[kind="primary"] {
        min-height:3.15rem; border:0; border-radius:14px; background:#17483b;
        color:white; font-weight:700; box-shadow:0 10px 25px rgba(23,72,59,.18);
    }
    .stButton > button[kind="primary"]:hover { background:#225f4f; color:white; transform:translateY(-1px); }
    .stButton > button { border-radius:12px; font-weight:600; }
    [data-testid="stTabs"] [data-baseweb="tab-list"] { gap:.35rem; border-bottom:1px solid var(--line); }
    [data-testid="stTabs"] [data-baseweb="tab"] { border-radius:10px 10px 0 0; padding:.7rem 1rem; }
    [data-testid="stTabs"] [aria-selected="true"] { background:var(--mint); color:var(--forest); }
    [data-testid="stExpander"] { background:rgba(255,255,255,.75); border:1px solid var(--line); border-radius:14px; }
    hr { border-color:var(--line) !important; }
    .final-banner {
        border-radius:20px; padding:1.25rem 1.4rem; color:white;
        background:linear-gradient(120deg, #17483b, #296d59); margin:1rem 0;
    }
    .final-banner strong { font-family:'Playfair Display', serif; font-size:1.45rem; }
    .final-banner span { display:block; color:rgba(255,255,255,.72); margin-top:.2rem; font-size:.88rem; }
    @media (max-width: 700px) {
        .block-container { padding-top:1.25rem; }
        .hero-title { font-size:2.7rem; }
        .hero-copy { font-size:1rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.markdown(
        '<div class="brand"><div class="brand-mark">✦</div><div class="brand-name">Roamly</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Your planning space")
    st.caption("Keep each trip in its own thread.")
    user_id = st.text_input("Traveller ID", value="demo_user")
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = f"{user_id}_{uuid.uuid4().hex[:8]}"
    if "final_plan_ready" not in st.session_state:
        st.session_state.final_plan_ready = False
    if st.button("＋ Start a new trip", use_container_width=True):
        st.session_state.thread_id = f"{user_id}_{uuid.uuid4().hex[:8]}"
        st.session_state.pop("waiting_for_approval", None)
        st.session_state.pop("latest_result", None)
        st.session_state.final_plan_ready = False
        st.rerun()
    st.markdown(
        f'<div class="thread-pill">CURRENT TRIP<br>{st.session_state.thread_id}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sidebar-note">From flights and stays to weather and budgets, your specialist agents plan the details together.</div>',
        unsafe_allow_html=True,
    )


st.markdown('<span class="eyebrow">✦ AI-powered trip design</span>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Your next great story starts here.</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-copy">Tell us where you want to go, how you like to travel, and what you want to spend. Roamly turns it into one thoughtful, ready-to-review itinerary.</div>',
    unsafe_allow_html=True,
)

query = st.text_area(
    "Describe your dream trip",
    placeholder="Try: Plan a 7-day Japan trip under ₹2 lakh with boutique hotels, great food, and no overnight flights.",
    height=150,
    label_visibility="collapsed",
)

button_col, hint_col = st.columns([1, 2.2], vertical_alignment="center")
with button_col:
    create_plan = st.button("Plan my journey  →", type="primary", use_container_width=True)
with hint_col:
    st.caption("Include dates, budget, interests, and travel preferences for the best result.")

config = {"configurable": {"thread_id": st.session_state.thread_id}}

if create_plan:
    if not query.strip():
        st.warning("Tell us a little about your trip first.")
    else:
        st.session_state.final_plan_ready = False
        with st.spinner("Your travel team is researching the best options…"):
            result = app.invoke(
                {
                    "messages": [HumanMessage(content=query)],
                    "user_id": user_id,
                    "user_query": query,
                    "flight_results": "",
                    "hotel_results": "",
                    "weather_results": "",
                    "budget_results": "",
                    "itinerary": "",
                    "final_response": "",
                    "llm_calls": 0,
                },
                config=config,
            )
        st.session_state.latest_result = result
        st.session_state.waiting_for_approval = "__interrupt__" in result


result = st.session_state.get("latest_result")

if result:
    st.divider()
    st.markdown('<div class="section-label">Your trip workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">The first draft is ready</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Explore the research, then review the complete day-by-day plan.</div>', unsafe_allow_html=True)

    selected_agents = result.get("selected_agents", [])
    agent_names = ", ".join(name.replace("_agent", "").title() for name in selected_agents)
    st.markdown(
        f'<div class="status-card"><div class="status-dot"></div><div><div class="status-title">Planning complete</div><div class="status-copy">Specialists involved: {agent_names or "Itinerary"}</div></div></div>',
        unsafe_allow_html=True,
    )

    with st.expander("Why this approach was chosen"):
        st.write(result.get("supervisor_reasoning", "No planning notes available."))

    flight_tab, hotel_tab, weather_tab, budget_tab = st.tabs(
        ["✈  Flights", "⌂  Stays", "☀  Weather", "₹  Budget"]
    )
    with flight_tab:
        st.markdown(result.get("flight_results", "No flight research was needed."))
    with hotel_tab:
        st.markdown(result.get("hotel_results", "No stay research was needed."))
    with weather_tab:
        st.markdown(result.get("weather_results", "No weather research was needed."))
    with budget_tab:
        st.markdown(result.get("budget_results", "No budget analysis was needed."))

    st.markdown('<div class="section-label">Day by day</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Your draft itinerary</div>', unsafe_allow_html=True)
    if "__interrupt__" in result:
        draft = result["__interrupt__"][0].value.get("draft_itinerary", "")
    else:
        draft = result.get("itinerary", "")
    st.markdown(draft)


if st.session_state.get("waiting_for_approval"):
    st.divider()
    st.markdown('<div class="section-label">One last check</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Does this trip feel like you?</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Approve the draft or share what you would like changed.</div>', unsafe_allow_html=True)

    approved = st.radio(
        "Review decision",
        ["Yes, it looks great", "I’d like some changes"],
        horizontal=True,
        label_visibility="collapsed",
    )
    feedback = st.text_area(
        "What should we change?",
        placeholder="For example: swap the luxury hotel for something local and add a free afternoon…",
        disabled=approved == "Yes, it looks great",
        height=110,
    )

    approval_col, _ = st.columns([1, 2.2])
    with approval_col:
        submit_approval = st.button("Finish my plan  →", type="primary", use_container_width=True)
    if submit_approval:
        with st.spinner("Adding the finishing touches…"):
            final_result = app.invoke(
                Command(
                    resume={
                        "approved": approved == "Yes, it looks great",
                        "feedback": feedback,
                    }
                ),
                config=config,
            )
        st.session_state.latest_result = final_result
        st.session_state.waiting_for_approval = False
        st.session_state.final_plan_ready = True
        st.rerun()


final_result = st.session_state.get("latest_result")
if (
    st.session_state.get("final_plan_ready")
    and final_result
    and final_result.get("final_response")
):
    st.divider()
    st.markdown(
        '<div class="final-banner"><strong>Your journey is ready.</strong><span>A complete plan, shaped around the way you want to travel.</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(final_result["final_response"])
