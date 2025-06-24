import streamlit as st
from openai import OpenAI

# --- Set page config ---
st.set_page_config(page_title="Kissht CSM Incentive Assistant", page_icon="💸")

st.title("💸 Kissht CSM Incentive Assistant")
st.markdown("Ask me anything about the **CSM login/disbursal incentive structure** for the week of June 20–27.")

# --- Your incentive structure logic here ---
incentive_guide = """
INCENTIVE STRUCTURE SUMMARY FOR KISSHT (For CSMs)

[INC-1]
- If a Sales Manager (SM) does 2 or more logins → ₹500 per SM (Min 8 SMs)
- If a branch achieves 15 logins → ₹2500 per branch (Min 1 branch)

[INC-2]
- If a Sales Manager (SM) does 2 or more disbursals → ₹1000 per SM (Min 8 SMs)
- If a branch disburses ₹25 lakhs or more → ₹5000 per branch (Min 3 branches)

VALIDITY: June 20 to June 27 (inclusive)

NOTES:
- Incentives are stackable. SM and branch level incentives can be earned simultaneously.
- Eligibility depends on both activity (logins/disbursals) and number of SMs/branches.
"""

# --- Get user question ---
st.subheader("Ask a question 👇")
user_question = st.text_input("Type your question here")

if st.button("Get Answer") and user_question:
    if "openai_api_key" not in st.secrets:
        st.error("OpenAI API key not found in Streamlit secrets.")
    else:
        client = OpenAI(api_key=st.secrets["openai_api_key"])

        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant. Answer only from the policy:\n\n{incentive_guide}"},
                    {"role": "user", "content": user_question}
                ],
                temperature=0.3
            )

            st.success(response.choices[0].message.content)
