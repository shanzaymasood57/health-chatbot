import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

# -----------------------------
# Load API Key
# -----------------------------
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ GROQ_API_KEY not found!")
    st.info("Create a .env file and add:\n\nGROQ_API_KEY=your_api_key")
    st.stop()

client = Groq(api_key=api_key)

# -----------------------------
# Streamlit Page
# -----------------------------
st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🏥",
    layout="centered"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main{
    background-color:#f5f9ff;
}

.stButton>button{
    width:100%;
    border-radius:10px;
    background-color:#4CAF50;
    color:white;
    font-size:18px;
    height:50px;
}

.stTextInput>div>div>input{
    border-radius:10px;
}

.answer{
    background-color:#E8F5E9;
    color:#000000;          /* Black text */
    padding:20px;
    border-radius:10px;
    border-left:7px solid #28a745;
    font-size:17px;
    line-height:1.7;
    font-weight:500;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🏥 About")

st.sidebar.info("""
This chatbot provides **general health information** only.

It does NOT diagnose diseases.

It does NOT prescribe medicines.

Always consult a qualified doctor.
""")

st.sidebar.markdown("---")

st.sidebar.subheader("Example Questions")

st.sidebar.write("""
• What causes a sore throat?

• Is paracetamol safe for children?

• What are flu symptoms?

• How much water should adults drink?

• How can I improve my sleep?
""")

# -----------------------------
# Title
# -----------------------------
st.title("🏥 AI Health Assistant")

st.write(
    "Ask your health-related questions below. "
    "I will provide simple and easy-to-understand information."
)

# -----------------------------
# User Input
# -----------------------------
question = st.text_input(
    "💬 Enter your question",
    placeholder="Example: What causes a sore throat?"
)

# -----------------------------
# Ask Button
# -----------------------------
if st.button("🔍 Get Answer"):

    # Empty input
    if question.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    # -----------------------------
    # Safety Filter
    # -----------------------------
    unsafe_words = [
        "suicide",
        "kill",
        "murder",
        "overdose",
        "poison",
        "harm myself",
        "self harm"
    ]

    if any(word in question.lower() for word in unsafe_words):

        st.error(
            "⚠ Sorry, I cannot provide assistance with dangerous medical requests.\n\n"
            "If this is an emergency, please contact your local emergency services or a healthcare professional immediately."
        )

        st.stop()

    # -----------------------------
    # Prompt Engineering
    # -----------------------------
    system_prompt = """
You are a helpful AI medical assistant.

Your job is only to provide general health education.

Rules:

1. Explain in simple English.

2. Be friendly.

3. Never diagnose diseases.

4. Never prescribe medicines.

5. Never tell users exactly what treatment they need.

6. Recommend consulting a doctor when symptoms are severe.

7. Politely refuse dangerous or harmful requests.

8. Keep answers under 150 words.

9. End every response with:

"This information is for educational purposes only and is not a substitute for professional medical advice."
"""

    try:

        with st.spinner("Generating answer..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

        answer = response.choices[0].message.content

        st.success("Answer")

        st.markdown(
            f'<div class="answer">{answer}</div>',
            unsafe_allow_html=True
        )

    except Exception as e:

        st.error("Something went wrong!")

        st.code(str(e))

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")

st.caption(
    "⚠ Disclaimer: This chatbot provides general health information only. "
    "It should not be used as a substitute for professional medical advice, diagnosis, or treatment."
)