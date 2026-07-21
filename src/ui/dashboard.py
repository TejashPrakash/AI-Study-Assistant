import streamlit as st


def render_dashboard(pdf_data):

    # ====================================
    # Header
    # ====================================

    st.title("📚 AI Study Assistant")

    st.caption("Your AI-powered learning companion for smarter learning.")

    st.divider()

    # ====================================
    # PDF Status
    # ====================================

    if pdf_data:

        if pdf_data["cached"]:

            st.success("📄 PDF Loaded Successfully (Already Indexed)")

        else:

            st.success("📄 PDF Uploaded & Indexed Successfully")

    else:

        st.info("📄 Upload a PDF from the sidebar to begin.")

    # ====================================
    # Statistics
    # ====================================

    pages = pdf_data["pages"] if pdf_data else 0
    chunks = pdf_data["chunks"] if pdf_data else 0

    chats = len(st.session_state.messages)
    flashcards = len(st.session_state.flashcards)
    quiz = len(st.session_state.quiz)
    notes = 1 if st.session_state.notes else 0

    st.subheader("📊 Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📄 Pages", pages)

    with col2:
        st.metric("🧩 Chunks", chunks)

    with col3:
        st.metric("💬 Chats", chats)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("🧠 Flashcards", flashcards)

    with col5:
        st.metric("❓ Quiz", quiz)

    with col6:
        st.metric("📝 Notes", notes)

    st.divider()

    # ====================================
    # Features
    # ====================================

    st.subheader("🚀 Available Features")

    c1, c2 = st.columns(2)

    with c1:

        st.info("💬 **AI Chat**\n\nAsk questions from your uploaded PDF.")

        st.info("📝 **AI Notes**\n\nGenerate structured study notes.")

        st.info("🧠 **Flashcards**\n\nRevise concepts using AI-generated flashcards.")

    with c2:

        st.info("❓ **Quiz**\n\nPractice MCQs generated from your study material.")

        st.info("📅 **Planner**\n\nCreate a personalized study timetable.")

        st.info("⚡ **Fast Retrieval**\n\nPowered by ChromaDB + Gemini.")

    st.divider()

    # ====================================
    # Recent Activity
    # ====================================

    st.subheader("📜 Recent Activity")

    activity = []

    if pdf_data:
        activity.append("✅ PDF Ready")

    if st.session_state.notes:
        activity.append("✅ Notes Generated")

    if st.session_state.flashcards:
        activity.append("✅ Flashcards Generated")

    if st.session_state.quiz:
        activity.append("✅ Quiz Generated")

    if st.session_state.messages:
        activity.append("✅ Chat Started")

    if activity:

        for item in activity:
            st.write(item)

    else:

        st.write("No activity yet.")

    st.divider()

    # ====================================
    # Tips
    # ====================================

    st.subheader("💡 Quick Tips")

    st.markdown("""
- 📄 Upload your study material.
- 💬 Ask questions naturally.
- 📝 Generate concise notes.
- 🧠 Revise with flashcards.
- ❓ Test yourself using quizzes.
- 📅 Plan your study schedule.
""")

    st.divider()

    st.caption("🚀 Version 2.0")
    st.caption("Made with ❤️ by **Tejash Prakash**")