import streamlit as st
import pickle
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# ── NLTK SETUP
@st.cache_resource
def load_nltk():
    nltk.download('punkt_tab')
    nltk.download('punkt')
    nltk.download('stopwords')

load_nltk()

ps = PorterStemmer()

# ── LOAD MODEL
tfidf = pickle.load(open("vectorizer.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))

# ── PAGE CONFIG
st.set_page_config(page_title="SpamShield — Shreyash Bansod", page_icon="📩", layout="centered")

# ── CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Poppins:wght@300;400;500;600&display=swap');

:root {
  --bg:     #080d0a;
  --card:   #111a14;
  --green:  #9CFF00;
  --cyan:   #00ffe0;
  --text:   #e6f5ec;
  --muted:  #7da890;
  --border: rgba(156,255,0,0.15);
  --glow:   rgba(156,255,0,0.25);
}

html, body, [class*="css"] {
  background-color: var(--bg);
  color: var(--text);
  font-family: 'Poppins', sans-serif;
}

/* noise overlay */
body::before {
  content: '';
  position: fixed; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none; z-index: 0; opacity: 0.35;
}

/* animated grid */
.stApp::before {
  content: '';
  position: fixed; inset: 0;
  background-image:
    linear-gradient(rgba(156,255,0,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(156,255,0,0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  animation: gridShift 20s linear infinite;
  z-index: 0; pointer-events: none;
}
@keyframes gridShift {
  0% { background-position: 0 0; }
  100% { background-position: 60px 60px; }
}

/* ambient blob */
.stApp::after {
  content: '';
  position: fixed;
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(156,255,0,0.07) 0%, transparent 70%);
  top: -150px; right: -100px;
  border-radius: 50%; filter: blur(80px);
  pointer-events: none; z-index: 0;
  animation: blobFloat 8s ease-in-out infinite;
}
@keyframes blobFloat {
  0%,100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-30px) scale(1.05); }
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 2rem; max-width: 700px; position: relative; z-index: 2; }

/* scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--green); border-radius: 2px; }

/* progress bar */
.progress-bar {
  position: fixed; top: 0; left: 0; height: 3px;
  background: linear-gradient(90deg, var(--green), var(--cyan));
  box-shadow: 0 0 8px var(--green);
  z-index: 9999; width: 100%;
  animation: progressLoad 1.5s ease forwards;
}
@keyframes progressLoad { from{width:0%} to{width:100%} }

/* hero */
.hero { text-align: center; padding: 3rem 0 2rem; }
.hero-label {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 5px 16px; border: 1px solid var(--border); border-radius: 30px;
  font-size: 11px; color: var(--green); letter-spacing: 2px;
  text-transform: uppercase; background: rgba(156,255,0,0.04);
  margin-bottom: 16px; animation: labelPulse 3s ease-in-out infinite;
}
@keyframes labelPulse {
  0%,100% { box-shadow: 0 0 0 rgba(156,255,0,0); }
  50% { box-shadow: 0 0 15px rgba(156,255,0,0.1); }
}
.hero-label .dot {
  width: 6px; height: 6px; background: var(--green); border-radius: 50%;
  box-shadow: 0 0 6px var(--green);
  animation: dotBlink 1.5s ease-in-out infinite; display: inline-block;
}
@keyframes dotBlink { 0%,100%{opacity:1} 50%{opacity:0.2} }

.hero h1 {
  font-family: 'Anton', sans-serif;
  font-size: clamp(2.5rem, 8vw, 5rem);
  background: linear-gradient(90deg, #9CFF00, #7dffb3, #ffffff, #9CFF00);
  background-size: 300%;
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  animation: heroGrad 6s linear infinite;
  line-height: 1.05; margin: 0; letter-spacing: 0.05em;
}
@keyframes heroGrad { 0%{background-position:0%} 100%{background-position:300%} }

.hero p {
  color: var(--muted); font-size: 0.9rem;
  letter-spacing: 0.2em; text-transform: uppercase; margin-top: 10px;
}

/* divider */
.divider {
  width: 100%; height: 1px;
  background: linear-gradient(90deg, transparent, var(--green), transparent);
  position: relative; overflow: visible; margin: 1.8rem 0;
}
.divider::after {
  content: ''; position: absolute; top: -3px; left: 50%; transform: translateX(-50%);
  width: 6px; height: 6px; background: var(--green); border-radius: 50%;
  box-shadow: 0 0 10px var(--green), 0 0 20px var(--green);
}

/* section header */
.section-header { display: flex; align-items: center; gap: 20px; margin-bottom: 30px; }
.section-num-big { font-family: 'Anton', sans-serif; font-size: 80px; color: rgba(156,255,0,0.08); line-height: 1; user-select: none; }
.section-title-wrap h2 { font-family: 'Anton', sans-serif; font-size: 36px; margin-bottom: 5px; color: var(--text); }
.section-title-wrap .line { height: 3px; width: 60px; background: linear-gradient(90deg, var(--green), transparent); border-radius: 2px; }

/* input box */
.stTextArea > div > div > textarea,
div[data-testid="stTextInput"] > div > div > input {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  color: var(--text) !important;
  font-family: 'Poppins', sans-serif !important;
  font-size: 0.95rem !important;
  padding: 1rem !important;
}
.stTextArea > div > div > textarea:focus,
div[data-testid="stTextInput"] > div > div > input:focus {
  border-color: var(--green) !important;
  box-shadow: 0 0 20px var(--glow) !important;
}

/* label */
div[data-testid="stTextInput"] label,
.stTextArea label {
  color: var(--muted) !important;
  font-size: 0.8rem !important;
  letter-spacing: 1px !important;
  text-transform: uppercase !important;
}

/* button */
div[data-testid="stButton"] > button {
  background: var(--green) !important; color: #000 !important;
  font-family: 'Poppins', sans-serif !important; font-size: 0.95rem !important;
  font-weight: 600 !important; border: none !important; border-radius: 30px !important;
  padding: 0.6rem 2.2rem !important;
  transition: transform 0.3s, box-shadow 0.3s !important; width: 100% !important;
}
div[data-testid="stButton"] > button:hover {
  transform: translateY(-3px) !important;
  box-shadow: 0 0 20px rgba(156,255,0,0.5) !important;
}

/* result card */
.result-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  margin-top: 1.5rem;
  position: relative;
  overflow: hidden;
}
.result-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--green), transparent);
}
.result-card.spam::before {
  background: linear-gradient(90deg, transparent, #ff4d4d, transparent);
}
.result-icon { font-size: 3rem; margin-bottom: 0.5rem; }
.result-label {
  font-family: 'Anton', sans-serif;
  font-size: 2rem; letter-spacing: 0.1em;
  margin-bottom: 0.5rem;
}
.result-label.spam { color: #ff4d4d; }
.result-label.safe { color: var(--green); }
.result-desc {
  color: var(--muted); font-size: 0.85rem;
  letter-spacing: 0.1em; text-transform: uppercase;
}

/* stats row */
.stats-row {
  display: flex; gap: 16px; margin-top: 1.5rem;
}
.stat-box {
  flex: 1; background: var(--card);
  border: 1px solid var(--border); border-radius: 12px;
  padding: 1rem; text-align: center;
  transition: 0.3s;
}
.stat-box:hover {
  border-color: rgba(156,255,0,0.4);
  transform: translateY(-3px);
}
.stat-num {
  font-family: 'Anton', sans-serif;
  font-size: 1.8rem; color: var(--green); display: block;
}
.stat-label {
  font-size: 10px; color: var(--muted);
  text-transform: uppercase; letter-spacing: 1px;
}

/* tech stack tags */
.tech-stack { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.tech-tag {
  padding: 4px 12px; border-radius: 20px; font-size: 11px;
  color: var(--green); border: 1px solid rgba(156,255,0,0.3);
  background: rgba(156,255,0,0.04); font-weight: 500;
}

div[data-testid="stSpinner"] { color: var(--green) !important; }
</style>
""", unsafe_allow_html=True)

# ── PROGRESS BAR
st.markdown('<div class="progress-bar"></div>', unsafe_allow_html=True)

# ── HERO
st.markdown("""
<div class="hero">
  <div class="hero-label"><span class="dot"></span> NLP · Machine Learning</div>
  <h1>SpamShield</h1>
  <p>Detect spam before it reaches you</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── STATS ROW
st.markdown("""
<div class="stats-row">
  <div class="stat-box">
    <span class="stat-num">98%</span>
    <span class="stat-label">Accuracy</span>
  </div>
  <div class="stat-box">
    <span class="stat-num">NLP</span>
    <span class="stat-label">Powered</span>
  </div>
  <div class="stat-box">
    <span class="stat-num">TF-IDF</span>
    <span class="stat-label">Vectorizer</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── SECTION HEADER
st.markdown("""
<div class="section-header">
  <span class="section-num-big">01</span>
  <div class="section-title-wrap">
    <h2>Classify Message</h2>
    <div class="line"></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── INPUT
input_sms = st.text_input("", placeholder="Paste your SMS or email message here…")

# ── TECH TAGS
st.markdown("""
<div class="tech-stack">
  <span class="tech-tag">Python</span>
  <span class="tech-tag">NLTK</span>
  <span class="tech-tag">Scikit-Learn</span>
  <span class="tech-tag">TF-IDF</span>
  <span class="tech-tag">Naive Bayes</span>
  <span class="tech-tag">Streamlit</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── PREDICT BUTTON + RESULT
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()
    stop_words = stopwords.words('english')
    for i in text:
        if i not in stop_words and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))
    return " ".join(y)

if st.button("🔍  Analyze Message"):
    if input_sms.strip() == "":
        st.markdown("""
        <div class="result-card">
          <div class="result-icon">⚠️</div>
          <div class="result-label" style="color:#f5a623;">No Input</div>
          <div class="result-desc">Please enter a message to analyze</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Analyzing message…"):
            transformed = transform_text(input_sms)
            vector_input = tfidf.transform([transformed])
            result = model.predict(vector_input)[0]

        if result == 1:
            st.markdown("""
            <div class="result-card spam">
              <div class="result-icon">🚨</div>
              <div class="result-label spam">SPAM DETECTED</div>
              <div class="result-desc">This message has been classified as spam</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-card">
              <div class="result-icon">✅</div>
              <div class="result-label safe">NOT SPAM</div>
              <div class="result-desc">This message appears to be legitimate</div>
            </div>
            """, unsafe_allow_html=True)
