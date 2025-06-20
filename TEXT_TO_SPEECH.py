import streamlit as st
import os
import tempfile
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voice
import torchaudio
import base64

# Load Tortoise TTS model
tts = TextToSpeech()

# UI
st.title("🎤 Tortoise TTS - Voice Cloner")
st.markdown('<div style="background:#def;padding:10px;font-weight:bold;">Clone high-quality voices with Tortoise TTS</div>', unsafe_allow_html=True)

text = st.text_area("Enter the text to speak:", height=150)
submit = st.button("Generate Voice")

# Voice list
voices = ['pat', 'daniel', 'emma', 'train_dotrice', 'train_lescault']
selected_voice = st.selectbox("Select a voice:", voices)

if submit and text.strip():
    with st.spinner("Generating voice..."):
        # Generate audio
        out = tts.tts_with_preset(text, voice=selected_voice, preset='fast')

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            torchaudio.save(f.name, out.squeeze(0).cpu(), 24000)
            audio_path = f.name

        # Convert to base64 for HTML playback
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            b64 = base64.b64encode(audio_bytes).decode()

        audio_html = f"""
            <audio controls autoplay>
            <source src="data:audio/wav;base64,{b64}" type="audio/wav">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

        # Animated text output
        st.markdown("### Cloned Speech Output:")
        st.markdown(f"<div style='font-size:22px;'>{text}</div>", unsafe_allow_html=True)
