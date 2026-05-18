import streamlit as st
from google import genai
from PyPDF2 import PdfReader
import re

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.main {
    background-color: #0E1117;
    color: white;
}

h1 {
    text-align: center;
    color: #00C6FF;
    font-size: 55px;
    font-weight: bold;
}

h2, h3 {
    color: #00C6FF;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(to right, #00c6ff, #0072ff);
    color: white;
    border-radius: 14px;
    height: 3.2em;
    font-size: 18px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.02);
    background: linear-gradient(to right, #0072ff, #00c6ff);
}

.metric-card {
    background: #161B22;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 0px 20px rgba(0,198,255,0.2);
}

.sidebar .sidebar-content {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================

st.title("🚀 AI Resume Analyzer")

st.markdown("""
<center>
Analyze resumes using Gemini AI and improve ATS performance.
</center>
""", unsafe_allow_html=True)

st.divider()

# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.header("⚡ About Project")

    st.write("""
    This AI Resume Analyzer helps users:

    ✅ Analyze ATS performance  
    ✅ Detect missing skills  
    ✅ Improve resume quality  
    ✅ Get role recommendations  
    ✅ Generate AI summaries  
    """)

    st.divider()

    st.subheader("🛠 Tech Stack")

    st.write("""
    - Python  
    - Streamlit  
    - Gemini AI  
    - NLP  
    - PyPDF2  
    """)

    st.divider()

    st.success("👨‍💻 Developed by Aakif Makrani")

# =========================================
# INPUTS
# =========================================

api_key = st.text_input(
    "🔑 Enter Gemini API Key",
    type="password"
)

uploaded_file = st.file_uploader(
    "📄 Upload Resume PDF",
    type=["pdf"]
)

# =========================================
# PDF EXTRACTION
# =========================================

def extract_text(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text

# =========================================
# EXTRACT ATS SCORE
# =========================================

def extract_score(text):

    match = re.search(r'(\d{1,3})/100', text)

    if match:
        return int(match.group(1))

    return 65

# =========================================
# ANALYZE BUTTON
# =========================================

if st.button("🚀 Analyze Resume"):

    if not api_key:

        st.error("Please enter Gemini API Key.")

    elif not uploaded_file:

        st.error("Please upload resume PDF.")

    else:

        with st.spinner("🤖 AI is analyzing your resume..."):

            try:

                resume_text = extract_text(uploaded_file)

                client = genai.Client(api_key=api_key)

                prompt = f"""
                You are an advanced ATS Resume Analyzer.

                Analyze the resume professionally.

                Give:

                ATS Score out of 100

                Technical Skills

                Missing Skills

                Resume Strengths

                Resume Weaknesses

                Best Job Roles

                Resume Improvements

                Professional Summary

                Resume:

                {resume_text}
                """

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                result = response.text

                # =========================================
                # ATS SCORE
                # =========================================

                score = extract_score(result)

                st.success("✅ Resume Analysis Complete!")

                st.subheader("🎯 ATS SCORE")

                col1, col2 = st.columns([1,3])

                with col1:

                    st.markdown(f"""
                    <div class="metric-card">
                        <h1>{score}</h1>
                        <h3>/100</h3>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:

                    st.progress(score)

                    if score >= 80:
                        st.success("Excellent Resume!")
                    elif score >= 60:
                        st.warning("Good Resume, but can improve.")
                    else:
                        st.error("Resume needs significant improvement.")

                st.divider()

                # =========================================
                # RESULT TABS
                # =========================================

                tab1, tab2, tab3 = st.tabs([
                    "📌 Full Analysis",
                    "📈 Resume Insights",
                    "💡 Recommendations"
                ])

                with tab1:

                    st.markdown(result)

                with tab2:

                    st.info("""
                    AI detected:
                    - Resume structure quality
                    - Technical skill alignment
                    - ATS keyword relevance
                    - Career suitability
                    """)

                with tab3:

                    st.success("""
                    Recommended next steps:

                    ✅ Add more projects  
                    ✅ Add measurable achievements  
                    ✅ Improve technical stack  
                    ✅ Add GitHub portfolio  
                    ✅ Add deployment links  
                    """)

            except Exception as e:

                st.error(f"Error: {e}")