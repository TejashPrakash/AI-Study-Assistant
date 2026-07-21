import streamlit as st
from streamlit_option_menu import option_menu


def render_sidebar():

    with st.sidebar:

        # =====================================
        # Header
        # =====================================

        st.title("📚 AI Study Assistant")
        st.caption("Learn Smarter with AI")

        st.divider()

        # =====================================
        # PDF Upload
        # =====================================

        st.subheader("📄 Study Material")

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"],
            label_visibility="collapsed"
        )

        if uploaded_file:
            st.success(f"✅ {uploaded_file.name}")
        else:
            st.info("No PDF uploaded")

        st.divider()

        # =====================================
        # Navigation
        # =====================================

        st.subheader("🧭 Navigation")

        feature = option_menu(
            menu_title=None,
            options=[
                "Dashboard",
                "Chat",
                "Notes",
                "Flashcards",
                "Quiz",
                "Planner"
            ],
            icons=[
                "speedometer2",
                "chat-dots-fill",
                "journal-text",
                "layers-fill",
                "patch-question-fill",
                "calendar-week-fill"
            ],
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "#0E1117",
                },
                "icon": {
                    "color": "#4F8BF9",
                    "font-size": "18px",
                },
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "4px 0",
                    "padding": "10px",
                    "--hover-color": "#262730",
                    "border-radius": "8px",
                },
                "nav-link-selected": {
                    "background-color": "#4F8BF9",
                    "color": "white",
                    "border-radius": "8px",
                },
            }
        )

        st.divider()

        # =====================================
        # Session
        # =====================================

        st.subheader("⚙️ Session")

        if st.button(
            "🗑️ Clear Chat History",
            use_container_width=True
        ):
            st.session_state.messages = []

            if "quiz" in st.session_state:
                st.session_state.quiz = []

            st.rerun()

        st.divider()

        # =====================================
        # About
        # =====================================

        st.subheader("ℹ️ About")

        st.markdown("""
**📚 AI Study Assistant**

Version **2.0**

Developed by **Tejash Prakash**
""")

    return uploaded_file, feature