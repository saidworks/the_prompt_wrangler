import streamlit as st
from service.azure_open_ai import AzureOpenAIModelService
from service.ollama import OllamaModelService
from util.ollama_available_models import AVAILABLE_MODELS
from service.provider_strategy import ProviderStrategy
# set a default model value
DEFAULT_MODEL = AVAILABLE_MODELS.gemma3_12b.value 

# Streamlit UI
def main():
    st.set_page_config(page_title="Prompt Wrangler")
    st.title("Prompt Wrangler")
    #initialize model service
    provider_strategy = ProviderStrategy("azure_open_ai")
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