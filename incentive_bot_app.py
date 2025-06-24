import streamlit as st
import requests

# --- Setup ---
st.set_page_config(page_title="Kissht Incentive Bot", page_icon="💸", layout="centered")
st.title("💬 Kissht CSM Incentive Assistant")
st.markdown("Ask about **Login/Disbursal incentives (June 20–27)**")

# --- Load API Key ---
api_key = st.secrets.get("gemini_api_key", "")
if not api_key:
    st.error("❌ Gemini API key is missing. Please add it in Streamlit secrets.")
    st.stop()

# --- Incentive Policy Text ---
incentive_guide = """
**INCENTIVES FOR CSMs (June 20–27):**

🔹 *Login Incentive*
- SM with ≥2 logins → ₹500 per SM (Min 8 SMs)
- Branch with ≥15 logins → ₹2500 (Min 1 branch)

🔹 *Disbursal Incentive*
- SM with ≥2 disbursals → ₹1000 per SM (Min 8 SMs)
- Branch with disbursal ≥₹25L → ₹5000 (Min 3 branches)

✅ Stackable for SM + Branch  
✅ Valid only from June 20 to June 27
"""

# --- Gemini Call Function ---
def ask_gemini(query: str) -> str:
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [{
            "role": "user",
            "parts": [{
                "text": f"Answer ONLY using the following:\n{incentive_guide}\n\nQ: {query}"
            }]
        }]
    }

    try:
        response = requests.post(
            f"{url}?key={api_key}",
            headers=headers,
            json=body,
            timeout=30  # increased timeout to avoid ReadTimeout
        )
        result = response.json()

        if response.status_code == 503:
            return "⚠️ Gemini is currently overloaded. Please try again shortly."

        if "candidates" not in result:
            return f"❌ Error: {result.get('error', {}).get('message', 'Unknown error')}"

        return result["candidates"][0]["content"]["parts"][0]["text"]

    except requests.exceptions.RequestException as e:
        return f"❌ Request failed: {e}"

# --- Input Form with Enter Support ---
with st.form("qa_form"):
    query = st.text_input("🔍 Ask your question:", placeholder="e.g., What if 9 SMs do 2 logins each?")
    submitted = st.form_submit_button("Get Answer")

# --- Output Section ---
if submitted and query:
    with st.spinner("💬 Getting answer (may take a few seconds)..."):
        reply = ask_gemini(query)

    if reply.startswith("⚠️") or reply.startswith("❌"):
        st.warning(reply)
    else:
        st.success("✅ Answer")
        st.write(reply)
