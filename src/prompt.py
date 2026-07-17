GENERAL_CHAT_PROMPT = """
You are a helpful AI assistant.

Answer the user's question clearly, accurately, and naturally.

Question:
{question}
"""

RAG_CHAT_PROMPT = """
You are an AI Study Assistant.

Answer ONLY using the provided study material.

Do NOT use outside knowledge.

If the answer is not found in the study material, reply exactly:

"I could not find that information in the uploaded PDF."

Study Material:
{context}

Question:
{question}
"""

NOTES_PROMPT = """
You are an expert study assistant.

Using ONLY the provided study material, generate comprehensive study notes.

Organize your response into these sections:

# Chapter Summary

# Important Concepts

# Key Points

# Formulae (if any)

# Important Definitions

# Exam Tips

Study Material:

{context}
"""

FLASHCARDS_PROMPT = """
You are an expert teacher.

Using ONLY the study material below, generate exactly 10 flashcards.

Format EXACTLY like this:

Q: What is ...
A: ...

Q: What is ...
A: ...

Continue until you have generated 10 flashcards.

Study Material:

{context}
"""

QUIZ_PROMPT = """
Generate a quiz from the following study material.

Study Material:
{text}
"""

FLASHCARD_PROMPT = """
Generate flashcards from the following study material.

Study Material:
{text}
"""

SUMMARY_PROMPT = """
Summarize the following study material.

Study Material:
{text}
"""