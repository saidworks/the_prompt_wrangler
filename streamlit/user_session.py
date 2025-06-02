import streamlit as st
from util.log_util import logger
from typing import Dict, Any
from util.llm_constants import AVAILABLE_MODELS, PROMPT_TEMPLATE






def init_session_state() -> None:
    '''
    Initialize the streamlit session state with default variables

    this function set up the default session state for llm without user intervation
    '''
    defaults : Dict[str, Any] = {
        "model": AVAILABLE_MODELS,
        "input_token": 0,
        "output_token": 0,
        "total_tokens": 0,
        "total_duration": 0,
        "max_tokens": 512,
        "seed": 4_503_599_627_370_496,
        "temperature": 0.5,
        "top_p":0.9,
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v



def create_sidebar()-> None: 
    """
    Create a sidebar with options to select model and other parameters
    
    This function will allow user to change the model and its parameters interactively.
    """
    with st.sidebar:
        st.header("Inference Settings")
        st.session_state.system_prompt = st.text_area(label="System Prompt",
                                                      value=PROMPT_TEMPLATE.DEFAULT_SYSTEM_PROMPT.value,
                                                      help="Set the context the AI Model will operate in.")
        







