import streamlit as st
from src.services.planner_service import generate_planner

def render_planner(uploaded_file, pdf_text):

    st.title("📅 AI Study Planner")

    if not uploaded_file:

        st.warning("Please upload a PDF first.")

    else:

        if "planner" not in st.session_state:
            st.session_state.planner = None

        st.subheader("Planner Settings")

        col1, col2 = st.columns(2)

        with col1:

            days = st.selectbox(
                "Study Duration",
                [3, 5, 7, 14, 30],
                index=2
            )

        with col2:

            hours = st.slider(
                "Hours per Day",
                1,
                8,
                2
            )

        if st.button("📅 Generate Planner"):

            with st.spinner("Creating Study Plan..."):

                st.session_state.planner = generate_planner(
                    pdf_text,
                    days=days,
                    hours_per_day=hours
                )

        if st.session_state.planner:

            planner = st.session_state.planner

            markdown_plan = "# 📅 Study Plan\n\n"

            for day in planner:

                st.markdown(f"## Day {day['day']}")

                markdown_plan += f"## Day {day['day']}\n"

                for topic in day["topics"]:

                    st.markdown(f"- {topic}")

                    markdown_plan += f"- {topic}\n"

                markdown_plan += "\n"

            st.download_button(
                "⬇ Download Planner",
                markdown_plan,
                file_name="study_plan.md",
                mime="text/markdown"
            )