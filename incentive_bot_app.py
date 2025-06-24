import streamlit as st
import requests

# --- Page UI ---
st.set_page_config(page_title="Kissht CSM Incentive Assistant", page_icon="💸")
st.title("💬 Kissht CSM Incentive Assistant")
st.markdown("Ask anything about the **login/disbursal incentive structure (June 20–27)**.")

# --- Load Gemini API Key from Secrets ---
api_key = st.secrets.get("gemini_api_key", "")
if not api_key:
    st.error("❌ Gemini API key is missing. Please add it in Streamlit secrets.")
    st.stop()

# --- Static Incentive Policy ---
incentive_guide = """
INCENTIVES FOR CSMs (June 20–27):

🔹 [Login Incentive]
- SM with ≥2 logins → ₹500 per SM (Min 8 SMs)
- Branch with ≥15 logins → ₹2500 (Min 1 branch)

🔹 [Disbursal Incentive]
- SM with ≥2 disbursals → ₹1000 per SM (Min 8 SMs)
- Branch with disbursal ≥₹25L → ₹5000 (Min 3 branches)

✔️ Both SM and Branch incentives are stackable
✔️ Valid only from June 20 to June 27
"""

# --- Gemini Call ---
def get_gemini_response(query):
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": f"You are a helpful assistant. ONLY answer using the following policy:\n{incentive_guide}"}]},
            {"parts": [{"text": query}]}
        ]
    }

        try:
        res = requests.post(f"{url}?key={api_key}", headers=headers, json=data)
        res_json = res.json()
        if "candidates" not in res_json:
            st.json(res_json)  # 👈 Show the full raw response on screen
            return "❌ Gemini response is missing 'candidates'. Check response above."
        return res_json["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Error: {e}"


# --- Input & Output ---
user_input = st.text_input("🔍 Ask your question here")
if st.button("Get Answer") and user_input:
    with st.spinner("Thinking..."):
        answer = get_gemini_response(user_input)
        st.success(answer)
