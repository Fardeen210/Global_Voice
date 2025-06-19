import streamlit as st
import requests

API_BASE_URL = "https://globalvoice-production.up.railway.app"

st.title("🌍 Global Voice - Multimodal Translator")

youtube_link = st.text_input("📹 Paste a YouTube video link")

target_language = st.selectbox("🌐 Select output language", ["en", "es", "fr", "de", "ar", "hi", "zh"])

if st.button("🔄 Process"):
    if youtube_link:
        with st.spinner("Processing... please wait ⏳"):
            try:
                response = requests.get(
                    f"{API_BASE_URL}/process_youtube",
                    params={"url": youtube_link, "lang": target_language}
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Translated video: {data['title']}")

                    with st.expander("📝 Original Transcript"):
                        st.text_area("Transcript", value=data["original_transcript"], height=300)

                    with st.expander("🌐 Translated Transcript"):
                        st.text_area("Translation", value=data["translated_transcript"], height=300)

                else:
                    try:
                        error_detail = response.json().get("detail", "Unknown error.")
                    except Exception:
                        error_detail = response.text
                    st.error(f"❌ Backend error: {error_detail}")
            except Exception as e:
                st.error(f"❌ API call failed: {e}")
    else:
        st.warning("⚠️ Please paste a valid YouTube link.")
