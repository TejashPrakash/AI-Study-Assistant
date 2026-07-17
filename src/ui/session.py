import streamlit as st


def initialize_session():

    defaults = {

        "messages": [],

        "notes": None,

        "flashcards": [],

        "current_card": 0,

        "show_answer": False,

        "quiz": [],

        "quiz_index": 0,

        "quiz_score": 0,

        "quiz_submitted": False,

        "selected_option": None,

        "quiz_finished": False,

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value