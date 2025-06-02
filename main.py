import streamlit as st
from service.azure_open_ai import AzureOpenAIModelService
from service.ollama import OllamaModelService
from ui.user_session import create_chatModel, create_sidebar, display_model_stats, init_session_state, update_sidebar_stats
from util.llm_constants import OLLAMA_MODELS
from service.provider_strategy import ProviderStrategy
# set a default model value
DEFAULT_MODEL = OLLAMA_MODELS.GEMMA3_12B.value 

# Streamlit UI
def main():
    st.set_page_config(page_title="Prompt Wrangler")
    st.title("Prompt Wrangler")
    init_session_state()
    create_sidebar()
    #initialize model service
    provider_strategy = create_chatModel()
    # diplay model stats
    display_model_stats()

    # Define system and user prompts
    input_text = st.text_area("Input Text", "Patient requires a full face CPAP mask with humidifier due to AHI > 20. Ordered by Dr. Cameron.")
    
    if st.button("Run"):
        with st.spinner("Processing..."):
            result = provider_strategy.call_llm(input_text)
        
        try:
            st.write(result)
            
        except Exception as e:
            st.error(f"An error occurred while displaying the results: {e}")
    
if __name__ == "__main__":
    main()