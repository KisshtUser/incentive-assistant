import streamlit as st
import time
from openai import OpenAI, RateLimitError, OpenAIError

# --- Page Settings ---
st.set_page_config(page_title="Kissht CSM Incentive Assistant", page_icon="💸")
st.title("💸 Kissht CSM Incentive Assistant")
st.markdown("Ask anything about the **CSM login/disbursal incentive structure (June 20–27)** and get clear answers!")

# --- Incentive Structure Prompt (shortened) ---
incentive_guide = """
INCENTIVES FOR CSMs (June 20–27):

🔹 [Login Incentive]
- SM with ≥2 logins → ₹500 per SM (Min 8 SMs)
- Branch with ≥15 logins → ₹2500 (Min 1 branch)

🔹 [Disbursal Incentive]
- SM with ≥2 disbursals → ₹1000 per SM (Min 8 SMs)
- Branch with disbursal ≥₹25L → ₹5000 (Min 3 branches)

✔️ SM and Branch incentives are stackable
✔️ Valid only from June 20 to June 27
"""

# --- Input UI ---
user_question = st.text_input("🔍 Type your question here")

# --- Handle API Call on Button Press ---
if st.button("Get Answer") and user_question:
    if "openai_api_key" not in st.secrets:
        st.error("❌ OpenAI API key is missing in Streamlit Secrets!")
    else:
        client = OpenAI(api_key=st.secrets["openai_api_key"])

        with st.spinner("🤖 Thinking..."):
            retries = 3
            delay = 8  # seconds between retries

            for attempt in range(retries):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4",  # ✅ Best version; use 'gpt-3.5-turbo' if needed
                        messages=[
                            {"role": "system", "content": f"You are an assistant. ONLY answer using this incentive guide:\n{incentive_guide}"},
                            {"role": "user", "content": user_question}
                        ],
                        max_tokens=300,
                        temperature=0.2
                    )
                    # Success
                    final_answer = response.choices[0].message.content
                    st.success(final_answer)
                    break

                except RateLimitError:
                    if attempt < retries - 1:
                        st.warning(f"⚠️ Rate limit hit. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        st.error("❌ Still hitting rate limits. Try again after some time.")
                except OpenAIError as e:
                    st.error(f"❌ OpenAI error: {str(e)}")
                    break
                except Exception as e:
                    st.error(f"⚠️ Unexpected error: {str(e)}")
                    break
