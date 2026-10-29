import streamlit as st
import requests

st.set_page_config(page_title="Raga Finder - Meta AI", layout="centered")
st.title("🎵 Raga Finder - Powered by Meta AI")

# Simple function to call Meta AI (Llama)
def ask_meta_ai(raga, detail):
    key = st.secrets.get("GROQ_API_KEY", "")
    if not key:
        st.error("Please add GROQ_API_KEY in Streamlit Secrets. See instructions below.")
        return
    
    prompt = f"You are a Hindustani Classical Guru. Give details for Raga {raga}. Need: {detail}. Format: Thaat, Time, Aroha, Avaroha, Pakad, Vadi Samvadi, Mood in bullet points. Use Sargam notation."
    
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body)
    
    if r.status_code == 200:
        ans = r.json()['choices'][0]['message']['content']
        st.success("Meta AI Answer:")
        st.markdown(ans)
    else:
        st.error(f"API Error: {r.text}")

# UI - No Upload
raga = st.text_input("Enter Raga Name", "Yaman")
choice = st.selectbox("What do you want?", ["Full Details", "Only Aroha Avaroha", "Beginner Explanation"])

if st.button("Get from Meta AI"):
    ask_meta_ai(raga, choice)

st.divider()
st.write("**How to add API Key?**")
st.write("1. Go to console.groq.com/keys → Create Key → Copy")
st.write("2. In Streamlit: Manage App → Settings → Secrets → Paste: GROQ_API_KEY = \"gsk_...\"")
