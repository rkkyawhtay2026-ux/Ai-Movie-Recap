import streamlit as st
import google.generativeai as genai
import yt_dlp
import os
import asyncio
import edge_tts

st.set_page_config(page_title="AI Movie Recap", layout="wide")

st.title("🎬 AI Movie Recap (Professional Edition)")

# 1. API SETUP
api_key = st.text_input("🔑 Gemini API Key", type="password", help="Enter your Google AI Studio Key", autocomplete="off")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        st.success("🟢 Engine Connected!")
    except:
        st.error("🔴 Invalid API Key")
        st.stop()
else:
    st.info("💡 Please enter your Gemini API Key to start.")
    st.stop()

# 2. INPUT SECTIONS
video_url = st.text_input("VIDEO SOURCE (TikTok Link)")
uploaded_file = st.file_uploader("OR UPLOAD CLIP", type=["mp4", "mov", "mp3"])
voice_map = {"Bright & Clear (Female)": "my-MM-NilarNeural", "Thiha (Male)": "my-MM-ThihaNeural"}
selected_voice = st.selectbox("Select Voice Character", list(voice_map.keys()))

if st.button("▶️ START RECAP"):
    with st.spinner("AI is analyzing..."):
        try:
            temp_name = "temp.mp3"
            if video_url:
                ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'temp.%(ext)s', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([video_url])
            else:
                with open(temp_name, "wb") as f: f.write(uploaded_file.getbuffer())

            audio_file = genai.upload_file(path=temp_name)
            response = model.generate_content([audio_file, "Create a viral Myanmar movie recap script for TikTok. Output ONLY Myanmar text."])
            st.subheader("📝 Generated Script:")
            st.write(response.text)
            
            asyncio.run(edge_tts.Communicate(response.text, voice_map[selected_voice]).save("final.mp3"))
            st.audio("final.mp3")
            os.remove(temp_name)
        except Exception as e:
            st.error(f"Error: {str(e)}")
