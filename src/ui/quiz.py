import streamlit as st

from src.services.quiz_service import generate_quiz

def render_quiz(uploaded_file, pdf_text):

    st.title("❓ AI Quiz Generator")

    if not uploaded_file:

        st.warning("Please upload a PDF first.")

    else:

        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"],
            index=1
        )

        num_questions = st.selectbox(
            "Number of Questions",
            [5, 10, 15],
            index=1
        )

        if st.button("🚀 Generate Quiz"):

            with st.spinner("Generating Quiz..."):

                st.session_state.quiz = generate_quiz(
                    pdf_text,
                    difficulty=difficulty,
                    num_questions=num_questions
                )

                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_submitted = False
                st.session_state.selected_option = None
                st.session_state.quiz_finished = False

        if st.session_state.quiz and not st.session_state.quiz_finished:

            quiz = st.session_state.quiz

            question = quiz[st.session_state.quiz_index]

            st.progress(
                (st.session_state.quiz_index + 1) / len(quiz)
            )

            st.subheader(
                f"Question {st.session_state.quiz_index + 1} / {len(quiz)}"
            )

            st.markdown(question["question"])

            option = st.radio(
                "Choose an answer:",
                ["A", "B", "C", "D"],
                format_func=lambda x: f"{x}. {question['options'][ord(x)-65]}",
                key=f"quiz_option_{st.session_state.quiz_index}"
            )

            if not st.session_state.quiz_submitted:

                if st.button("✅ Submit Answer"):

                    st.session_state.selected_option = option
                    st.session_state.quiz_submitted = True

                    if option == question["answer"]:

                        st.session_state.quiz_score += 1

                    st.rerun()

            else:

                if st.session_state.selected_option == question["answer"]:

                    st.success("✅ Correct!")

                else:

                    st.error(
                        f"❌ Incorrect! Correct Answer: {question['answer']}"
                    )

                st.info(question["explanation"])

                if st.button("➡ Next Question"):

                    st.session_state.quiz_index += 1

                    st.session_state.quiz_submitted = False
                    st.session_state.selected_option = None

                    if st.session_state.quiz_index >= len(quiz):

                        st.session_state.quiz_finished = True

                    st.rerun()

        elif st.session_state.quiz_finished:

            total = len(st.session_state.quiz)

            score = st.session_state.quiz_score

            percentage = score / total * 100

            st.success("🎉 Quiz Completed!")

            col1, col2 = st.columns(2)

            with col1:

                st.metric("Score", f"{score}/{total}")

            with col2:

                st.metric("Percentage", f"{percentage:.1f}%")

            if st.button("🔄 Retry Quiz"):

                st.session_state.quiz = []
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_submitted = False
                st.session_state.selected_option = None
                st.session_state.quiz_finished = False

                st.rerun()