import streamlit as st
import requests

# --- Page Config ---
st.set_page_config(page_title="Kissht Incentive Assistant", page_icon="🤖")
st.title("💬 Kissht CSM Incentive Assistant")
st.markdown("Ask me anything about the **login/disbursal incentive structure (June 20–27)**.")

# --- Gemini API Key (from Streamlit Secrets) ---
api_key = st.secrets.get("gemini_api_key", "")

if not api_key:
    st.error("🚫 Gemini API key not found. Add it in Streamlit secrets.")
    st.stop()

# --- Incentive Context ---
incentive_guide = """
INCENTIVES FOR CSMs (June 20–27):

🔹 [Login Incentive]
- SM with ≥2 logins → ₹500 per SM (Min 8 SMs)
- Branch with ≥15 logins → ₹2500 (Min 1 branch)

🔹 [Disbursal Incentive]
- SM with ≥2 disbursals → ₹1000 per SM (Min 8 SMs)
- Branch with disbursal ≥₹25L → ₹5000 (Min 3 branches)

✔️ Stackable: Branch + SM incentives apply
✔️ Valid only from June 20 to June 27
"""

# --- User Input ---
question = st.text_input("🔍 Ask your question here")

# --- Gemini Function ---
def get_gemini_response(question_text):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": f"You are a helpful assistant. Answer only using this policy:\n{incentive_guide}"}]},
            {"parts": [{"text": question_text}]}
        ]
    }
    response = requests.post(f"{url}?key={api_key}", headers=headers, json=data)
    result = response.json()
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "❌ Error: Could not generate a response. Try again."

# --- On Submit ---
if st.button("Get Answer") and question:
    with st.spinner("💭 Thinking..."):
        reply = get_gemini_response(question)
        st.success(reply)
