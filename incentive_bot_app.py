import streamlit as st
from openai import OpenAI
import time

# --- App config ---
st.set_page_config(page_title="Kissht Incentive Assistant", page_icon="💸")
st.title("💸 Kissht CSM Incentive Assistant")
st.markdown("Ask anything about CSM login/disbursal incentives (June 20–27).")

# --- Incentive guide (concise for token efficiency) ---
incentive_guide = """
INCENTIVES FOR CSM (June 20–27):

[INC-1]
- SM with ≥2 logins → ₹500 each (Min 8 SMs)
- Branch with ≥15 logins → ₹2500 (Min 1 branch)

[INC-2]
- SM with ≥2 disbursals → ₹1000 each (Min 8 SMs)
- Branch with ≥₹25L disbursed → ₹5000 (Min 3 branches)

Stackable: Branch + SM incentives both applicable.
"""

# --- Input from user ---
user_question = st.text_input("🔍 Type your question:")

if st.button("Get Answer") and user_question:
    if "openai_api_key" not in st.secrets:
        st.error("API key not found in secrets.")
    else:
        client = OpenAI(api_key=st.secrets["openai_api_key"])
        
        with st.spinner("Generating response..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # Use gpt-4 if allowed
                    messages=[
                        {"role": "system", "content": f"Answer user queries using ONLY the incentive guide:\n{incentive_guide}"},
                        {"role": "user", "content": user_question}
                    ],
                    max_tokens=300,        # Reduce tokens returned
                    temperature=0.2        # Stable, factual answers
                )
                st.success(response.choices[0].message.content)
            except Exception as e:
                st.error("⚠️ API Rate Limit hit. Please try again in a minute.")
                st.info(f"Error: {type(e).__name__}")
                time.sleep(10)

