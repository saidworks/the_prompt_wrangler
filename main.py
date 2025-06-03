import streamlit as st
from ui.user_session import (
    create_chatModel,
    create_sidebar,
    init_session_state,
    update_sidebar_stats,
)
from util.llm_constants import OLLAMA_MODELS

# set a default model value
DEFAULT_MODEL = OLLAMA_MODELS.GEMMA3_12B.value


st.set_page_config(page_title="Prompt Wrangler")
st.title("Prompt Wrangler")
init_session_state()
create_sidebar()
# initialize model service using the strategy pattern
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
        col1, col2 = st.columns(2)
        with col1:
            st.header("Output: ")
            st.write(result)
        with col2:
            update_sidebar_stats(metadata)
    except Exception as e:
        st.error(f"An error occurred while displaying the results: {e}")
