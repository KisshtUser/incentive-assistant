import openai.error

# --- User Input ---
user_question = st.text_input("🔍 Type your question:")

if st.button("Get Answer") and user_question:
    if "openai_api_key" not in st.secrets:
        st.error("API key not found in secrets.")
    else:
        client = OpenAI(api_key=st.secrets["openai_api_key"])

        with st.spinner("Thinking..."):
            retries = 3
            delay = 10  # seconds to wait on error
            for attempt in range(retries):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": f"Answer based on this policy:\n{incentive_guide}"},
                            {"role": "user", "content": user_question}
                        ],
                        temperature=0.2,
                        max_tokens=300
                    )
                    st.success(response.choices[0].message.content)
                    break  # success
                except openai.RateLimitError:
                    if attempt < retries - 1:
                        st.warning(f"Rate limit hit. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        st.error("Still hitting rate limits. Try again after a while.")
