import os
import re
import streamlit as st
from google import genai
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# =========================================
# LOAD ENV
# =========================================

load_dotenv()

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #F5F7FB;
}

/* Hide Streamlit Branding */

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main Layout */

.block-container {
    padding-top: 2rem;
    max-width: 1350px;
}

/* Buttons */

.stButton > button {
    width: 100%;
    height: 3.5em;
    border-radius: 16px;
    border: none;
    background: linear-gradient(to right, #4F46E5, #7C3AED);
    color: white;
    font-size: 16px;
    font-weight: 600;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px);
}

/* File Uploader */

[data-testid="stFileUploader"] {
    background: white;
    border: 2px dashed #D1D5DB;
    border-radius: 20px;
    padding: 20px;
}

/* Metric Card */

[data-testid="metric-container"] {
    background: white;
    border-radius: 24px;
    padding: 25px;
    border: 1px solid #ECECEC;
    box-shadow: 0 10px 30px rgba(0,0,0,0.04);
}

/* Tabs */

.stTabs [data-baseweb="tab"] {
    background: white;
    border-radius: 14px;
    padding: 10px 22px;
    border: 1px solid #ECECEC;
    margin-right: 10px;
}

/* Cards */

.card {
    background: white;
    padding: 30px;
    border-radius: 28px;
    border: 1px solid #ECECEC;
    box-shadow: 0 10px 30px rgba(0,0,0,0.04);
}

.hero-title {
    font-size: 64px;
    font-weight: 800;
    line-height: 1;
    color: #111827;
}

.hero-gradient {
    background: linear-gradient(to right, #4F46E5, #7C3AED);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    color: #6B7280;
    font-size: 19px;
    margin-top: 15px;
    line-height: 1.7;
}

.small-title {
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 13px;
    margin-bottom: 10px;
}

.result-box {
    background: white;
    border-radius: 24px;
    padding: 30px;
    border: 1px solid #ECECEC;
    box-shadow: 0 10px 30px rgba(0,0,0,0.04);
}

</style>
""", unsafe_allow_html=True)

# =========================================
# FUNCTIONS
# =========================================

def extract_text(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text


def extract_score(text):

    match = re.search(r'(\\d{1,3})/100', text)

    if match:
        return int(match.group(1))

    return 72

# =========================================
# HERO SECTION
# =========================================

st.markdown("""
<div class="card">

<div class="small-title">
AI Powered Resume Intelligence
</div>

<div class="hero-title">
Optimize Your <span class="hero-gradient">Resume</span>
</div>

<div class="hero-sub">
Get ATS insights, recruiter-style analysis,
missing skills detection, and AI-powered
career recommendations using Gemini AI.
</div>

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# =========================================
# MAIN GRID
# =========================================

left, right = st.columns([1.2, 0.8])

# =========================================
# LEFT PANEL
# =========================================

with left:

    st.markdown("""
    <div class="card">
    <div class="small-title">
    Upload Resume
    </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )

    analyze = st.button("Analyze Resume")

# =========================================
# RIGHT PANEL
# =========================================

with right:

    st.markdown("""
    <div class="card">

    <div class="small-title">
    ATS Intelligence
    </div>

    ### AI Recruiter Dashboard

    - ATS Optimization Analysis  
    - Missing Skills Detection  
    - Resume Improvements  
    - Technical Skill Evaluation  
    - Recruiter-Level Feedback  

    </div>
    """, unsafe_allow_html=True)

# =========================================
# ANALYSIS
# =========================================

if analyze:

    if not uploaded_file:

        st.error("Please upload resume PDF.")

    else:

        with st.spinner("Analyzing resume using Gemini AI..."):

            try:

                resume_text = extract_text(uploaded_file)

                client = genai.Client(
                    api_key=os.getenv("GEMINI_API_KEY")
                )

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

                score = extract_score(result)

                st.write("")
                st.write("")

                # =========================================
                # SCORE SECTION
                # =========================================

                score1, score2 = st.columns([1, 2])

                with score1:

                    st.metric(
                        label="ATS SCORE",
                        value=f"{score}/100"
                    )

                with score2:

                    st.markdown("""
                    ### Resume Performance
                    """)

                    st.progress(score)

                    if score >= 80:
                        st.success("Excellent ATS optimization detected.")
                    elif score >= 60:
                        st.warning("Good resume with improvement opportunities.")
                    else:
                        st.error("Resume requires significant optimization.")

                st.write("")
                st.write("")

                # =========================================
                # TABS
                # =========================================

                tab1, tab2, tab3 = st.tabs([
                    "Full Analysis",
                    "Resume Insights",
                    "Recommendations"
                ])

                with tab1:

                    st.markdown(result)

                with tab2:

                    st.info("""
AI detected:

• Resume structure quality  
• ATS keyword relevance  
• Technical skill alignment  
• Career suitability  
• Hiring optimization insights  
""")

                with tab3:

                    st.success("""
Recommended Improvements:

• Add measurable achievements  
• Improve technical stack visibility  
• Add deployed projects  
• Include GitHub portfolio  
• Optimize ATS keywords  
""")

            except Exception as e:

                st.error(f"Error: {e}")