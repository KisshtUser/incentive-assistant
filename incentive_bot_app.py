import streamlit as st
import requests

# --- Setup ---
st.set_page_config(page_title="Kissht Incentive Chat", page_icon="💬", layout="centered")
st.title("💬 Kissht CSM Incentive Chat Assistant")
st.markdown("Ask anything about **Login/Disbursal Incentives (June 20–27)**")

# --- Gemini API Key ---
api_key = st.secrets.get("gemini_api_key", "")
if not api_key:
    st.error("❌ Gemini API key missing. Please add in secrets.")
    st.stop()

# --- Incentive Guide ---
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

# --- Initialize Chat State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Gemini Chat Function ---
def chat_with_gemini(chat_history):
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    messages = [
        {"role": "user", "parts": [{"text": f"You are an assistant for CSM Incentives. Use only this:\n{incentive_guide}"}]}
    ]

    for entry in chat_history:
        messages.append({"role": "user", "parts": [{"text": entry['user']}]})
        messages.append({"role": "model", "parts": [{"text": entry['bot']}]})

    # Only send the last user query with full context
    if chat_history:
        query = chat_history[-1]['user']
        messages.append({"role": "user", "parts": [{"text": query}]})

    data = { "contents": messages }

    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}",
            headers=headers,
            json=data,
            timeout=30
        )
        res_json = response.json()

        if response.status_code == 503:
            return "⚠️ Gemini is currently overloaded. Try again shortly."

        if "candidates" not in res_json:
            return f"❌ Error: {res_json.get('error', {}).get('message', 'Unknown error')}"

        return res_json["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Request failed: {e}"

# --- Chat Display ---
for message in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(message["user"])
    with st.chat_message("assistant"):
        st.markdown(message["bot"])

# --- New Chat Input ---
user_query = st.chat_input("Ask your question about incentives")

if user_query:
    # Show user message
    st.chat_message("user").markdown(user_query)

    # Append temporary message to chat
    st.session_state.chat_history.append({"user": user_query, "bot": "..."})

    # Get Gemini reply
    with st.spinner("Thinking..."):
        bot_reply = chat_with_gemini(st.session_state.chat_history)

    # Update chat history
    st.session_state.chat_history[-1]["bot"] = bot_reply

    # Show bot response
    st.chat_message("assistant").markdown(bot_reply)

# --- Reset Chat Button ---
st.markdown("---")
if st.button("🔁 Reset Conversation"):
    st.session_state.chat_history = []
    st.experimental_rerun()
