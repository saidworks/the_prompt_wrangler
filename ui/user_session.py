import streamlit as st
from service.provider import Provider
from service.provider_strategy import ProviderStrategy
from typing import Dict, Any
from util.llm_constants import OLLAMA_MODELS, LLM_PROVIDERS, AZURE_MODELS


def init_session_state() -> None:
    """
    Initialize the streamlit session state with default variables

    this function set up the default session state for llm without user intervation
    """
    defaults: Dict[str, Any] = {
        "model": OLLAMA_MODELS.GEMMA3_12B.value,
        "input_token": 0,
        "output_token": 0,
        "total_tokens": 0,
        "total_duration": 0,
        "max_tokens": 512,
        "temperature": 0.5,
        "top_p": 0.9,
        "top_k": 40,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def create_sidebar() -> None:
    """
    Create a sidebar with options to select model and other parameters

    This function will allow user to change the model and its parameters interactively.
    """
    with st.sidebar:
        st.header("Inference Settings")

        st.session_state.provider = st.selectbox(
            "LLM Providers",
            options=[LLM_PROVIDERS.AZURE.name, LLM_PROVIDERS.OLLAMA.name],
        )
        if st.session_state.provider == LLM_PROVIDERS.AZURE.name:
            st.session_state.model = st.selectbox(
                "Model",
                options=AZURE_MODELS.AZURE_GPT3_5.value,
                index=0,
                help="Select the model to use.",
                key=1,
            )
        else:
            st.session_state.model = st.selectbox(
                "Model",
                options=[
                    OLLAMA_MODELS.GEMMA3_12B.value,
                    OLLAMA_MODELS.QWEN3_8B.value,
                    OLLAMA_MODELS.GRANITE3_3_8B.value,
                ],
                index=0,
                help="Select the model to use.",
                key=2,
            )

        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.01,
            help="Controls the randomness in the output.",
        )
        st.session_state.top_p = st.slider(
            "Top P",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.top_p,
            step=0.01,
            help="Controls the diversity of the model's responses.",
        )
        st.session_state.top_k = st.slider(
            "Top K",
            min_value=1,
            max_value=100,
            value=st.session_state.top_k,
            step=1,
            help="Controls the diversity of the model's responses.",
        )
        st.session_state.max_tokens = st.slider(
            "Response Tokens",
            min_value=0,
            max_value=8192,
            value=st.session_state.max_tokens,
            step=16,
            help="Sets the maximum number of tokens in the response.",
        )
        display_model_set_config()


def display_model_set_config() -> None:
    """
    Display current model configuration in the sidebar.

    This function shows the current values of model parameters and settings
    in the Streamlit sidebar.
    """
    st.markdown("---")
    st.text(
        f"""Settings Recap:
            - model: {st.session_state.model}
            - temperature: {st.session_state.temperature}
            - top_p: {st.session_state.top_p}
            - num_predict: {st.session_state.max_tokens}
        """
    )


def update_sidebar_stats(metadata: Any) -> None:
    """
    Update the sidebar with statistics from the latest model response.

    This function calculates and updates various statistics in the session state,
    including token counts, duration, and tokens per second.

    Args:
        response (Any): The response object from the chat model containing metadata.
    """
    total_duration = metadata["response_time"]
    st.session_state.total_duration = f"{total_duration:.2f} s"
    st.session_state.input_tokens = metadata["input_tokens"]
    st.session_state.output_tokens = metadata["output_tokens"]
    st.session_state.total_tokens = metadata["total_tokens"]

    st.header("Usage statistics:")
    st.metric("input_tokens :", f"{st.session_state.input_tokens}")
    st.metric("output_tokens :", f"{st.session_state.output_tokens}")
    st.metric("total_tokens :", f"{st.session_state.total_tokens}")
    st.metric("total_duration :", f"{st.session_state.total_duration}")


def create_chatModel() -> Provider:
    """
    create an instance of a provider based on session values"""
    return ProviderStrategy(
        st.session_state.provider,
        st.session_state.top_p,
        st.session_state.top_k,
        st.session_state.model,
        st.session_state.temperature,
        st.session_state.max_tokens,
    )
