import streamlit as st
from ui.user_session import (
    create_chatModel,
    create_sidebar,
    init_session_state,
)
from util.llm_constants import OLLAMA_MODELS

# set a default model value
DEFAULT_MODEL = OLLAMA_MODELS.GEMMA3_12B.value


# Streamlit UI
def main():
    st.set_page_config(page_title="Prompt Wrangler")
    st.title("Prompt Wrangler")
    init_session_state()
    create_sidebar()
    # initialize model service
    provider_strategy = create_chatModel()

    # Define system and user prompts
    input_text = st.text_area(
        "Input Text",
        "Patient requires a full face CPAP mask with humidifier due to AHI > 20. Ordered by Dr. Cameron.",
    )

    if st.button("Run"):
        with st.spinner("Processing..."):
            result, metadata = provider_strategy.call_llm(input_text)
        try:
            st.write("Result of the query is: ", result)
            st.write("Usage statistics: ", metadata)
        except Exception as e:
            st.error(f"An error occurred while displaying the results: {e}")


if __name__ == "__main__":
    main()
