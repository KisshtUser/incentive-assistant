import streamlit as st
import requests

# --- Page UI ---
st.set_page_config(page_title="Kissht CSM Incentive Assistant", page_icon="💸")
st.title("💬 Kissht CSM Incentive Assistant")
st.markdown("Ask anything about the **login/disbursal incentive structure (June 20–27)**.")

# --- Load Gemini API Key ---
api_key = st.secrets.get("gemini_api_key", "")
if not api_key:
    st.error("❌ Gemini API key is missing. Please add it in Streamlit secrets.")
    st.stop()

# --- Incentive Policy ---
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
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"""Use only this policy to answer:
{incentive_guide}

Question: {query}"""
                    }
                ]
            }
        ]
    }

    res = requests.post(f"{url}?key={api_key}", headers=headers, json=data)
    res_json = res.json()

    # Handle API overload
    if res.status_code == 503:
        return "OVERLOADED"

    # Handle missing response
    if "candidates" not in res_json:
        st.subheader("🔎 Debug Output from Gemini")
        st.json(res_json)
        return "❌ Gemini response is missing 'candidates'. Check debug output above."

    return res_json["candidates"][0]["content"]["parts"][0]["text"]

# --- User Input & Output ---
query = st.text_input("🔍 Ask your question here")

# State to track retry attempts
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""
if "overloaded" not in st.session_state:
    st.session_state.overloaded = False

# Submit button
if st.button("Get Answer") and query:
    with st.spinner("💭 Thinking..."):
        response = get_gemini_response(query)
        st.session_state.last_query = query

        if response == "OVERLOADED":
            st.session_state.overloaded = True
            st.warning("⚠️ Gemini is currently overloaded. Please click below to retry.")
        else:
            st.session_state.last_answer = response
            st.session_state.overloaded = False
            st.success("✅ Answer:")
            st.write(response)

# Retry button
if st.session_state.overloaded:
    if st.button("🔁 Retry"):
        with st.spinner("♻️ Retrying..."):
            response = get_gemini_response(st.session_state.last_query)
            if response == "OVERLOADED":
                st.warning("⚠️ Still overloaded. Try again in a few moments.")
            else:
                st.session_state.last_answer = response
                st.session_state.overloaded = False
                st.success("✅ Answer:")
                st.write(response)
