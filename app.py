import streamlit as st
from chains import run_research
from report import generate_pdf

st.set_page_config(
    page_title="Deep Research AI",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Deep Research AI Agent")
st.caption("Built with LangChain + Groq (Llama 3) + DuckDuckGo · 100% Free")

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    
    breadth = st.slider(
        "Breadth — sub-queries",
        min_value=1, max_value=5, value=3,
        help="How many different angles of the topic to research"
    )
    depth = st.slider(
        "Depth — search rounds per query",
        min_value=1, max_value=3, value=2,
        help="How many times each sub-query searches the web"
    )

    st.divider()
    st.markdown("**Stack**")
    st.markdown("- 🧠 LLM: Groq / Llama 3.3 70B")
    st.markdown("- 🔍 Search: DuckDuckGo")
    st.markdown("- 🔗 Framework: LangChain")
    st.markdown("- 🖥️ UI: Streamlit")
    st.markdown("- 📄 PDF: ReportLab")
    st.divider()
    st.success("✅ Total cost: ₹0")

# ── Main input ───────────────────────────────────────────────────────────────
topic = st.text_input(
    "🔍 Enter your research topic:",
    placeholder="e.g. Impact of AI on healthcare in 2025"
)

col1, col2 = st.columns([1, 3])
with col1:
    start = st.button("🚀 Start Research", type="primary", use_container_width=True)
with col2:
    st.caption(f"Will run {breadth} sub-queries × {depth} search rounds = up to {breadth * depth * 2} web searches")

# ── Run pipeline ─────────────────────────────────────────────────────────────
if start:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        progress = st.progress(0, text="Starting research agents...")

        with st.status("🤖 Running research pipeline...", expanded=True) as status:
            st.write("🔍 Agent 1 — Researcher searching the web...")
            progress.progress(10, "Researcher working...")

            try:
                report = run_research(topic, breadth=breadth, depth=depth)

                progress.progress(80, "Summarizing findings...")
                st.write("📝 Agent 2 — Summarizer organizing findings...")

                progress.progress(95, "Writing report...")
                st.write("✍️ Agent 3 — Presenter writing the report...")

                st.session_state["report"] = report
                st.session_state["topic"] = topic
                progress.progress(100, "Done!")
                status.update(label="✅ Research complete!", state="complete")

            except Exception as e:
                progress.empty()
                status.update(label="❌ Error occurred", state="error")
                st.error(f"Something went wrong: {e}")
                st.info("Tip: Check your GROQ_API_KEY in the .env file")

# ── Display report ───────────────────────────────────────────────────────────
if "report" in st.session_state:
    st.divider()

    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.subheader(f"📄 Report: {st.session_state['topic']}")
    with col_b:
        pdf_bytes = generate_pdf(
            st.session_state["topic"],
            st.session_state["report"]
        )
        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_bytes,
            file_name=f"{st.session_state['topic'][:40].replace(' ', '_')}_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    with st.expander("📖 Full Report", expanded=True):
        st.markdown(st.session_state["report"])