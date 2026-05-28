import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from io import StringIO
import re
import os

USE_OPENAI = False

try:
    from openai import OpenAI

    if os.getenv("OPENAI_API_KEY"):
        client = OpenAI()
        USE_OPENAI = True

except Exception:
    USE_OPENAI = False

st.set_page_config(
    page_title="Smart Notes App",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.stTextArea textarea {
    font-size: 16px;
}

.note-card {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #ddd;
}

.ai-box {
    background-color: #eef7ff;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #3399ff;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 Smart Notes Learning App")
st.write("Create, organize, visualize, and simplify your notes using AI.")

st.sidebar.header("⚙️ Settings")

template = st.sidebar.selectbox(
    "Choose Notes Template",
    ["Listing", "Table", "Mind Map"]
)

theme = st.sidebar.selectbox(
    "Theme",
    ["Light", "Dark"]
)

st.header("📝 Your Notes")

uploaded_file = st.file_uploader(
    "Upload a text file (.txt)",
    type=["txt"]
)

default_text = """Python
Variables
Functions
Loops
Conditionals
Classes
Objects
Inheritance
Decorators
"""

notes = ""

if uploaded_file:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    notes = stringio.read()
else:
    notes = st.text_area(
        "Write your notes here:",
        value=default_text,
        height=300
    )

lines = [line.strip() for line in notes.split("\n") if line.strip()]

st.header("📚 Notes Visualization")

if template == "Listing":

    st.subheader("📌 Bullet Listing")

    st.markdown('<div class="note-card">', unsafe_allow_html=True)

    for item in lines:
        st.markdown(f"- {item}")

    st.markdown('</div>', unsafe_allow_html=True)

elif template == "Mind Map":

    st.subheader("🧠 Mind Map")

    if len(lines) > 0:

        G = nx.Graph()

        main_topic = lines[0]

        G.add_node(main_topic)

        for item in lines[1:]:
            G.add_node(item)
            G.add_edge(main_topic, item)

        fig, ax = plt.subplots(figsize=(10, 6))

        pos = nx.spring_layout(G, seed=42)

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="skyblue",
            node_size=3000,
            font_size=10,
            font_weight="bold",
            edge_color="gray",
            ax=ax
        )

        st.pyplot(fig)

st.header("🤖 AI Learning Assistant")

user_question = st.text_input(
    "Ask AI to simplify or explain your notes:"
)

def local_simplifier(text, question):
    """
    Basic fallback simplifier without OpenAI.
    """

    simplified = f"""
### Simplified Notes

Your notes mainly discuss:

{", ".join(lines[:10])}

### Simple Explanation

These topics are important programming concepts.

- Variables store information
- Functions organize reusable code
- Loops repeat tasks
- Classes help create objects

### Your Question

{question}

### Basic Answer

Try learning one concept at a time and practice with small examples.
"""

    return simplified


if st.button("✨ Simplify Notes"):

    if not notes.strip():
        st.warning("Please enter some notes first.")

    else:
        with st.spinner("AI is processing your notes..."):

st.markdown("---")
st.caption("Built with Streamlit ❤️")