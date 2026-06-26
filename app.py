import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# ----------------------------------------
# Load Environment Variables
# ----------------------------------------
load_dotenv()

# Get API key (Streamlit Cloud or Local)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ Groq API Key not found.")
    st.info(
        "Local: Create a .env file with\n\n"
        "GROQ_API_KEY=your_api_key\n\n"
        "Streamlit Cloud: Add the key under Settings → Secrets."
    )
    st.stop()

# Initialize Groq Client
client = Groq(api_key=api_key)

# ----------------------------------------
# Page Configuration
# ----------------------------------------
st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🏥",
    layout="centered"
)

# ----------------------------------------
# Custom CSS
# ----------------------------------------
st.markdown("""
<style>

.stApp{
    background-color:#F5F9FF;
}

h1{
    text-align:center;
    color:#0B5394;
}

.stButton>button{
    width:100%;
    background:#28A745;
    color:white;
    font-size:18px;
    border-radius:10px;
    height:50px;
    border:none;
}

.stButton>button:hover{
    background:#218838;
}

.stTextInput>div>div>input{
    border-radius:10px;
    border:2px solid #B0C4DE;
}

.answer-box{
    background:white;
    color:black !important;
    padding:20px;
    border-radius:15px;
    border-left:8px solid #28A745;
    box-shadow:0px 4px 12px rgba(0,0,0,0.15);
    margin-top:20px;
    font-size:17px;
    line-height:1.8;
}

.answer-box *{
    color:black !important;
}

.footer{
    text-align:center;
    color:gray;
    font-size:13px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# Sidebar
# ----------------------------------------
st.sidebar.title("🏥 About")

st.sidebar.info("""
This chatbot provides **general health information only**.

✅ Explains common health topics.

❌ Does NOT diagnose diseases.

❌ Does NOT prescribe medicines.

Always consult a healthcare professional.
""")

st.sidebar.markdown("---")

st.sidebar.subheader("💡 Example Questions")

st.sidebar.write("""
• What causes a sore throat?

• Is paracetamol safe for children?

• What are flu symptoms?

• How much water should adults drink?

• How can I improve my sleep?

• What causes headaches?
""")

# ----------------------------------------
# Title
# ----------------------------------------
st.title("🏥 AI Health Assistant")

st.write(
    "Welcome! Ask any **general health-related question** "
    "and receive easy-to-understand educational information."
)

# ----------------------------------------
# Input
# ----------------------------------------
question = st.text_input(
    "💬 Ask your question",
    placeholder="Example: What causes a sore throat?"
)

# ----------------------------------------
# Safety Filter
# ----------------------------------------
unsafe_words = [
    "suicide",
    "kill",
    "murder",
    "overdose",
    "poison",
    "harm myself",
    "self harm",
    "how to die",
    "end my life"
]

# ----------------------------------------
# Button
# ----------------------------------------
if st.button("🔍 Get Answer"):

    if question.strip() == "":
        st.warning("⚠ Please enter a question.")
        st.stop()

    if any(word in question.lower() for word in unsafe_words):
        st.error(
            "⚠ I can't assist with dangerous or self-harm related requests.\n\n"
            "If this is an emergency, contact your local emergency services or a trusted healthcare professional."
        )
        st.stop()

    system_prompt = """
You are an AI Health Assistant.

Your role is to provide general health education.

Rules:

- Explain in simple English.
- Be friendly and supportive.
- Never diagnose illnesses.
- Never prescribe medicines.
- Never recommend dosages.
- Encourage users to consult a doctor for persistent, severe, or emergency symptoms.
- Politely refuse dangerous or harmful requests.
- Keep responses under 150 words.
- End every response with:

"This information is for educational purposes only and is not a substitute for professional medical advice."
"""

    try:

        with st.spinner("🤖 Generating response..."):

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

        st.success("✅ Answer")

        st.markdown(
            f"""
            <div class="answer-box">
            {answer}
            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:

        st.error("❌ Something went wrong while contacting the AI model.")

        st.code(str(e))

# ----------------------------------------
# Footer
# ----------------------------------------
st.markdown("---")

st.markdown(
    """
<div class="footer">
⚠ <b>Disclaimer:</b> This chatbot provides general health information only.
It is not intended to diagnose, treat, cure, or prevent any disease.
Always seek advice from a qualified healthcare professional.
</div>
""",
    unsafe_allow_html=True
)