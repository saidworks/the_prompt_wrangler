import streamlit as st
from service.azure_open_ai import AzureOpenAIModelService
from util.ollama_available_models import AvailableModels

# set a default model value
DEFAULT_MODEL = AvailableModels.gemma3_12b.value 

# Streamlit UI
def main():
    st.set_page_config(page_title="Prompt Wrangler")
    st.title("Prompt Wrangler")
    #initialize model service
    # ollama_service = OllamaModelService(model_reference=DEFAULT_MODEL, temperature=0.7, max_tokens=512,format="json")
    azure_service = AzureOpenAIModelService(temperature=0.7, max_tokens=512,format="json")
    # Define system and user prompts
    user_prompt = st.text_area("User Prompt", """You are a medical data extraction assistant, your job is to extract metadata about medical equipment
                                from an unstructured user text input.""")
    input_text = st.text_area("Input Text", "Patient requires a full face CPAP mask with humidifier due to AHI > 20. Ordered by Dr. Cameron.")

    if st.button("Run"):
        with st.spinner("Processing..."):
            # result = ollama_service.call_llm(user_prompt, input_text)
            result = azure_service.call_llm(user_prompt, input_text)
        try:
            st.write(result)
        except Exception as e:
            st.error(f"An error occurred while displaying the results: {e}")

if __name__ == "__main__":
    main()