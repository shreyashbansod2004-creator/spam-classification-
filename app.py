import streamlit as st
import pickle
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# -------- FIX NLTK ERROR (STREAMLIT CLOUD) --------
@st.cache_resource
def load_nltk():
    nltk.download('punkt_tab')
    nltk.download('punkt')
    nltk.download('stopwords')

load_nltk()

ps = PorterStemmer()

# ---------- LOAD MODEL ----------
tfidf = pickle.load(open("vectorizer.pkl","rb"))
model = pickle.load(open("model.pkl","rb"))

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Spam Classifier", page_icon="📩", layout="centered")

# ---------- CSS ----------
st.markdown("""
<style>

.stApp{
background: radial-gradient(circle at 30% 40%, #13201A 0%, #111B18 60%, #0d1512 100%);
color:white;
overflow:hidden;
}

/* METEOR AREA */

.meteor-container{
position:fixed;
bottom:0;
left:0;
width:100%;
height:100%;
pointer-events:none;
z-index:0;
overflow:hidden;
}

/* METEOR */

.meteor{
position:absolute;
width:3px;
height:140px;
background:linear-gradient(white, transparent);
opacity:0;
transform: rotate(-45deg);
animation: meteor 5s linear infinite;
}

/* RANDOM START POSITIONS */

.meteor:nth-child(1){ bottom:-10%; left:10%; animation-delay:0s;}
.meteor:nth-child(2){ bottom:-20%; left:30%; animation-delay:1s;}
.meteor:nth-child(3){ bottom:-15%; left:50%; animation-delay:2s;}
.meteor:nth-child(4){ bottom:-10%; left:70%; animation-delay:3s;}
.meteor:nth-child(5){ bottom:-25%; left:90%; animation-delay:4s;}
.meteor:nth-child(6){ bottom:-15%; left:20%; animation-delay:2.5s;}
.meteor:nth-child(7){ bottom:-10%; left:40%; animation-delay:1.5s;}
.meteor:nth-child(8){ bottom:-20%; left:60%; animation-delay:3.5s;}
.meteor:nth-child(9){ bottom:-15%; left:80%; animation-delay:4.5s;}
.meteor:nth-child(10){ bottom:-10%; left:5%; animation-delay:5s;}

@keyframes meteor {

0%{
transform: translate(0,0) rotate(-45deg);
opacity:1;
}

100%{
transform: translate(-700px,-700px) rotate(-45deg);
opacity:0;
}

}

/* TITLE */

.title{
text-align:center;
font-size:48px;
font-weight:700;
margin-bottom:30px;
color:white;
}

/* INPUT */

.stTextInput>div>div>input{
background-color:rgba(0,0,0,0.6);
border:2px solid #00ffb3;
color:white;
border-radius:10px;
padding:12px;
}

/* BUTTON */

.stButton>button{
width:100%;
background: rgba(0,0,0,0.6);
border-radius:20px;
padding:20px;
font-size:22px;
font-weight:600;
color:white;
border:1px solid rgba(0,255,150,0.3);
box-shadow:0 0 40px rgba(0,255,150,0.25);
transition: all 0.25s ease;
}

.stButton>button:hover{
transform:scale(1.03);
box-shadow:
0 0 20px #ADFF2F,
0 0 40px #ADFF2F,
0 0 80px rgba(173,255,47,0.6);
}

.result{
text-align:center;
font-size:34px;
font-weight:bold;
margin-top:25px;
}

</style>
""", unsafe_allow_html=True)

# ---------- METEOR HTML ----------
st.markdown("""
<div class="meteor-container">
<span class="meteor"></span>
<span class="meteor"></span>
<span class="meteor"></span>
<span class="meteor"></span>
<span class="meteor"></span>
<span class="meteor"></span>
<span class="meteor"></span>
<span class="meteor"></span>
<span class="meteor"></span>
<span class="meteor"></span>
</div>
""", unsafe_allow_html=True)

# ---------- TEXT PROCESS ----------
def transform_text(text):

    text = text.lower()
    text = nltk.word_tokenize(text)

    y=[]

    for i in text:
        if i.isalnum():
            y.append(i)

    text=y[:]
    y.clear()

    stop_words = stopwords.words('english')

    for i in text:
        if i not in stop_words and i not in string.punctuation:
            y.append(i)

    text=y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

# ---------- UI ----------
st.markdown('<div class="title">📩 SMS Spam Classifier</div>', unsafe_allow_html=True)

input_sms = st.text_input("Enter your message")

if st.button("Predict"):

    transformed = transform_text(input_sms)

    vector_input = tfidf.transform([transformed])

    result = model.predict(vector_input)[0]

    if result == 1:
        st.markdown('<p class="result" style="color:#ff4d4d;">🚨 Spam Message</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="result" style="color:#00ffb3;">✅ Not Spam</p>', unsafe_allow_html=True)
