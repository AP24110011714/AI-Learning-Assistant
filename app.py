import streamlit as st
import pandas as pd
import plotly.express as px

from utils.prompt_builder import build_prompt
from utils.gemini_helper import get_response
from utils.gemini_api import generate_ai_response
from utils.emotion_engine import get_emotion_and_confidence

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="AI Learning Assistant",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Learning Assistant")
st.info("Enter your learning problem and get AI-powered emotional support.")

st.divider()

# ===============================
# SESSION STATE
# ===============================
if "history" not in st.session_state:
    st.session_state.history = []

# ===============================
# AI TOGGLE
# ===============================
use_ai = st.checkbox("🤖 Use Gemini AI Response", value=True)

# ===============================
# INPUT
# ===============================
field = st.selectbox(
    "Select Your Academic Field",
    ["Computer Science", "Mathematics", "Physics", "Chemistry",
     "Biology", "Electronics", "Mechanical", "Civil",
     "English", "Economics", "Other"]
)

problem = st.text_area(
    "Describe your learning problem",
    height=200,
    placeholder="Example: I'm confused about recursion."
)

# ===============================
# ANALYZE BUTTON
# ===============================
if st.button("Analyze Emotion"):

    # VALIDATION
    if problem.strip() == "":
        st.error("Please enter a learning problem before analyzing.")
        st.stop()

    # TEMP VALUES (Epic 3 pending)
    emotion, confidence = get_emotion_and_confidence(problem)

    prompt = build_prompt(field, problem, emotion, confidence)

    # AI GENERATION
    with st.spinner("🔍 Generating response..."):
        try:
            if use_ai:
                ai_response = generate_ai_response(prompt)

                if ai_response is None:
                    response = get_response(emotion)
                    final_response = response["emoji"] + "\n\n" + response["response"]
                else:
                    final_response = ai_response
            else:
                response = get_response(emotion)
                final_response = response["emoji"] + "\n\n" + response["response"]

        except Exception:
            st.error("AI failed. Using fallback.")
            response = get_response(emotion)
            final_response = response["emoji"] + "\n\n" + response["response"]

    # ===============================
    # OUTPUT (FINAL POLISHED UI)
    # ===============================
    st.success("Analysis Completed")

    # Layout (Story 4)
    col1, col2 = st.columns(2)

    with col1:
        st.write("### 📚 Field")
        st.write(field)

    with col2:
        st.write("### 📝 Problem")
        st.write(problem)

    # Emotion badge
    st.write("### 😊 Emotion")
    if emotion == "Confused":
        st.error(f"🔴 {emotion}")
    elif emotion == "Confident":
        st.success(f"🟢 {emotion}")
    elif emotion == "Frustrated":
        st.warning(f"🟠 {emotion}")
    else:
        st.info(f"🔵 {emotion}")

    # Confidence bar
    st.write("### 📊 Confidence")
    st.progress(confidence / 100)
    st.write(f"{confidence}%")

    # Prompt
    st.write("### 🤖 Gemini Prompt")
    st.code(prompt)

    # AI Response Card
    st.write("### 💡 AI Response")
    st.markdown(
        f"""
        <div style="
            padding:15px;
            border-radius:10px;
            background-color:#1e1e1e;
            color:white;
            border:1px solid #444;">
            {final_response}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Save history
    st.session_state.history.append({
        "field": field,
        "problem": problem,
        "emotion": emotion,
        "confidence": confidence
    })

# ===============================
# SIDEBAR
# ===============================
st.sidebar.title("📊 Dashboard")
st.sidebar.write(f"Total Interactions: {len(st.session_state.history)}")

if st.sidebar.button("🗑 Clear History"):
    st.session_state.history = []
    st.rerun()

st.sidebar.subheader("Recent")

for item in reversed(st.session_state.history[-3:]):
    st.sidebar.write(f"📚 {item['field']}")
    st.sidebar.write(f"😊 {item['emotion']} ({item['confidence']}%)")
    st.sidebar.write("---")

# ===============================
# ANALYTICS DASHBOARD
# ===============================
if len(st.session_state.history) > 0:

    st.divider()
    st.title("📊 Analytics Dashboard")

    df = pd.DataFrame(st.session_state.history)

    tab1, tab2, tab3 = st.tabs(["😊 Emotions", "📚 Fields", "📌 Summary"])

    with tab1:
        emotion_counts = df["emotion"].value_counts().reset_index()
        emotion_counts.columns = ["emotion", "count"]

        fig = px.pie(emotion_counts, names="emotion", values="count")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.line(df, y="confidence", markers=True)
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        field_counts = df.groupby(["field", "emotion"]).size().reset_index(name="count")

        fig3 = px.bar(field_counts, x="field", y="count", color="emotion", barmode="group")
        st.plotly_chart(fig3, use_container_width=True)

    with tab3:
        st.write("Total:", len(df))
        st.write("Most Emotion:", df["emotion"].mode()[0] if not df.empty else "N/A")
        st.write("Avg Confidence:", round(df["confidence"].mean(), 2) if not df.empty else 0)
        st.dataframe(df)