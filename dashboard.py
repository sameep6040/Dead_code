import streamlit as st
import os
from Main import run_secure_optimization

st.set_page_config(
    page_title="Secure Dead Code Optimization Engine",
    page_icon="⚙️",
    layout="wide"
)

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

h1, h2, h3 {
    color: white;
}

.stTextArea textarea {
    font-family: 'Courier New', monospace;
    background-color: #1a1c23 !important;
    color: #00ff88 !important;
    border-radius: 10px;
}

.stCodeBlock {
    background-color: #1a1c23 !important;
    border-radius: 10px;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.metric-box {
    background: #161b22;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #2d3748;
}

</style>
""", unsafe_allow_html=True)


st.sidebar.title("⚙️ Navigation")

page = st.sidebar.radio(
    "Choose Section",
    [
        "Compiler Dashboard",
        "Project Source Code"
    ]
)

st.sidebar.markdown("---")

st.sidebar.subheader("📌 Project Summary")

st.sidebar.info("""
This project performs:

- Dead Code Elimination
- CFG Generation
- Unreachable Code Removal
- Dead Branch Removal
- Overwritten Assignment Removal
- Unused Function Detection
- Break/Continue Dead Code Removal
""")

st.sidebar.markdown("---")

st.sidebar.subheader("🧠 Core Concepts")

st.sidebar.write("""
- Intermediate Representation (IR)
- Control Flow Graph (CFG)
- Control Flow Analysis
- Local Data Flow Optimization
""")

st.sidebar.markdown("---")
st.sidebar.caption("v2.0 | Compiler Design Project")


if page == "Project Source Code":

    st.title("📂 Internal Logic Explorer")
    st.write("Explore the internal implementation of the optimization engine.")

    files = [
        "Parser.py",
        "Optimizer.py",
        "instractions.py",
        "Main.py",
        "CFG.py",
        "dashboard.py"
    ]

    selected_file = st.selectbox(
        "Select File",
        files
    )

    try:
        with open(selected_file, "r") as f:
            code = f.read()
            st.code(code, language="python")

    except Exception as e:
        st.error(f"Could not open file: {e}")


else:

    st.title("⚙️ Secure Dead Code Optimization Engine")
    st.caption("Control Flow + Data Flow Based Compiler Optimization Dashboard")

    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📥 Source Code Input")

        language = st.selectbox(
            "Choose Programming Language",
            ["C", "Python"]
        )

        input_code = st.text_area(
            "Paste your C code here",
            height=500,
            placeholder="Paste your C code here..."
        )

        run_button = st.button(
            "🚀 Run Optimization",
            type="primary"
        )

    with col2:
        st.subheader("📤 Optimized Output")

        if run_button and input_code:

            with st.spinner("Analyzing program structure and generating CFG..."):

                optimized_code, logs, removed_lines, ir_list, before_cfg, after_cfg = run_secure_optimization(
                    input_code, 
                    language
                )

                st.session_state["optimized_code"] = optimized_code
                st.session_state["logs"] = logs
                st.session_state["removed_lines"] = removed_lines
                st.session_state["ir_list"] = ir_list
                st.session_state["before_cfg"] = before_cfg
                st.session_state["after_cfg"] = after_cfg

        if "optimized_code" in st.session_state:

            st.text_area(
                "Optimized C Code",
                value=st.session_state["optimized_code"],
                height=500
            )

        else:
            st.info("Run optimization to view results.")

    st.markdown("---")

    st.subheader("📊 Optimization Summary")

    m1, m2, m3 = st.columns(3)

    if "optimized_code" in st.session_state:

        with m1:
            st.metric(
                "Lines Removed",
                st.session_state["removed_lines"]
            )

        with m2:
            st.metric(
                "CFG Status",
                "Generated"
            )

        with m3:
            st.metric(
                "Optimization Status",
                "Success"
            )

    else:
        with m1:
            st.metric("Lines Removed", "0")

        with m2:
            st.metric("CFG Status", "Waiting")

        with m3:
            st.metric("Optimization Status", "Idle")

    st.markdown("---")

    st.subheader("🧭 Control Flow Graph Comparison")

    if "before_cfg" in st.session_state:

        cfg1, cfg2 = st.columns(2)

        with cfg1:
            st.markdown("### Before Optimization")
            before_path = f"static/{st.session_state['before_cfg']}"

            if os.path.exists(before_path):
                st.image(before_path, width="stretch")
            else:
                st.warning("Before CFG image not found.")

        with cfg2:
            st.markdown("### After Optimization")
            after_path = f"static/{st.session_state['after_cfg']}"

            if os.path.exists(after_path):
                st.image(after_path, width="stretch")
            else:
                st.warning("After CFG image not found.")

    else:
        st.info("Run optimization to generate CFG comparison.")

    st.markdown("---")

    with st.expander("🔍 Intermediate Representation (IR)"):

        if "ir_list" in st.session_state:

            st.write("Instruction stream used by the optimizer:")

            for instr in st.session_state["ir_list"]:
                st.text(str(instr))

        else:
            st.info("IR will appear after optimization.")

    st.markdown("---")

    st.subheader("📝 Optimization Audit Trail")

    if "logs" in st.session_state:

        for log in st.session_state["logs"]:
            st.success(log)

    else:
        st.info("Audit logs will appear here after execution.")