import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import base64
import os
import time
from io import BytesIO

st.set_page_config(page_title="Text to Speech Cloner", layout="centered")

# ========== CSS ========== #
st.markdown("""
<style>
.title {
    font-size: 48px;
    font-weight: bold;
    color: #4CAF50;
    text-align: center;
    margin-bottom: 10px;
}
.banner {
    background-color: #dff0d8;
    color: #3c763d;
    font-weight: bold;
    padding: 10px;
    text-align: center;
    animation: move 10s linear infinite;
    white-space: nowrap;
    overflow: hidden;
}
@keyframes move {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}
.output-text span {
    display: inline-block;
    opacity: 0;
    animation: appear 0.05s forwards;
}
@keyframes appear {
    to { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# ========== UI Header ========== #
st.markdown('<div class="title">🎤 Text to Speech Cloner</div>', unsafe_allow_html=True)
st.markdown('<div class="banner">Clone Your Text Into 5 Unique Voices Instantly!</div>', unsafe_allow_html=True)

# ========== Input ========== #
text_input = st.text_area("Enter your text here:", height=150)
submit = st.button("Enter and Process")

# ========== Voice Selection and Processing ========== #
voices = {
    "Voice 1 - Male": "en",
    "Voice 2 - Female": "en",
    "Voice 3 - British": "en-uk",
    "Voice 4 - Indian": "en-in",
    "Voice 5 - Slow": "en"
}

def generate_tts(text, lang='en', slow=False):
    tts = gTTS(text=text, lang=lang, slow=slow)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    return mp3_fp

if submit and text_input.strip():
    st.subheader("Choose a Voice to Clone:")

    selected_voice = st.radio("Available Voices", list(voices.keys()))

    # Simulate voice parameters
    lang = voices[selected_voice]
    slow = True if "Slow" in selected_voice else False

    with st.spinner("Generating voice..."):
        audio_bytes = generate_tts(text_input, lang=lang, slow=slow)
        audio_base64 = base64.b64encode(audio_bytes.getvalue()).decode()
        audio_html = f"""
            <audio autoplay controls>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

    # Animated Text
    st.markdown("### 📝 Cloned Text Output:")
    st.markdown('<div class="output-text">', unsafe_allow_html=True)
    output_html = ""
    for i, char in enumerate(text_input):
        output_html += f"<span style='animation-delay:{i * 0.03}s'>{char}</span>"
    st.markdown(output_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
