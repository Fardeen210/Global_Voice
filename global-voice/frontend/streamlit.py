import streamlit as st
import requests

API_BASE_URL = "https://your-fastapi-app.onrender.com"  # 🔁 Replace this after deployment

st.title("🌍 Global Voice - Multimodal Translator")

youtube_link = st.text_input("📹 Paste a YouTube video link")

target_language = st.selectbox("🌐 Select output language", ["en", "es", "fr", "de", "ar", "hi", "zh"])

if st.button("🔄 Process"):
    if youtube_link:
        with st.spinner("Processing... please wait ⏳"):
            response = requests.get(
                f"{API_BASE_URL}/process_youtube",
                params={"url": youtube_link, "lang": target_language}
            )

            if response.status_code == 200:
                data = response.json()
                st.success(f"✅ Video processed: {data['message']}")
                st.code(data["path"])  # placeholder; replace later with transcript, subtitle, etc.
            else:
                st.error(f"❌ Error: {response.json()['detail']}")
    else:
        st.warning("Please paste a YouTube link.")
