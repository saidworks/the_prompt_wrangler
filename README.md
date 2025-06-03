# The Prompt Wrangler Project

[![Python Version](https://img.shields.io/badge/python-%3E=3.11-blue?logo=python)](https://www.python.org/)

## Overview

The Prompt Wrangler API provides a secure and controlled interface for interacting with Language Models (LLMs). It focuses on input sanitization, parameter control, and observability to ensure responsible and reliable LLM usage. Built with Streamlit and Langchain, it prioritizes clean API design and robust error handling.

## Features


*   **Controlled LLM Parameters:** 
   *   Limits `temperature`, `max_tokens`, and `top_p` to ensure predictable and manageable outputs.
   * Provider provide choice between available model providers, so far we support Azure OpenAI, and Ollama (ollama can be self-hosted, or locally run).

*   **Observability:** Logs provide insights into critical errors, also we monitors token usage to help avoid overuse.
*   **Langchain Powered:** Leverages Langchain for efficient LLM interaction.
*   **Clear Error Handling:**  Provides detailed error messages for debugging.
*   **Token Counting:** Implement token counting to accurately measure API usage and costs.

## Prerequisites

*   **Python 3.11+**
*   **Ollama:** A framework to run language models locally.  [https://ollama.com/](https://ollama.com/)
*   **An LLM Model:** You're using the default gemma3:12b. Can be changed in the code.

## Installation

1.  **Clone the repository:**
    Open your terminal and type:
    ```bash
    git clone git@github.com:saidworks/the_prompt_wrangler.git
    cd prompt-wrangler
    ```
2. **Setup virtual environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # MacOS
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    To install dependencies you will need to install uv follow instruction on the following [link](https://docs.astral.sh/uv/getting-started/installation/), then open terminal in project folder and execute:
    ```bash
    uv sync
    ```

4.  **Run Ollama and download the model:**

    Ensure you have Ollama installed and running, if not use the following [link](https://ollama.com/) to install it.  Then ensure that the default model (gemma3:12b) is available. If not, pull the model:

    ```bash
    ollama pull gemma3:12b
    ```
## LLM Providers:

-   **OLLAMA:** Supports models like `gemma3:12b`, `qwen3:latest`, and `granite3.3:latest`. 
    best results were achieved using the `gemma3:12b` model based on multiple empirical testing with provided inputs.
-   **AZURE:** Supports model `gpt-35-turbo` is the only model I tried and it achieves similar results to `gemma3:12b` model. 
    To use azure you will need to modify name of `.env.example` file to `.env` and set your own resource url and api key.


## Usage

1.  **Start the app:**
 Open terminal on the project folder and run the following command after you had setup ollama and other dependencies:
    ```bash
        streamlit run main.py    
    ```  


## Configuration

*   **Model Name:**  The default model for ollama is `gemma3:12b` and for azure .  You can change this by modifying the `model_name` parameter in the `PromptWrangler` class constructor within the `main.py` file.
*   **LLM Parameters:** The `temperature`, `max_tokens`, and `top_p` parameters are configured within the as part of dictionary and stored in streamlit session that create new instance of chat model each time the user submits a new request.  Adjust these values to fine-tune the LLM's output.
## Testing
1. **Unit Test**
 To run unit tests open terminal and execute:
 ```bash
 pytest
 ```


## Future Enhancements

*   **Input Validation:** Add more robust input validation to prevent errors and enhance security.
*   **Authentication:**  Add authentication to control API access.
*   **Rate Limiting:**  Implement rate limiting to prevent abuse and ensure fair usage.
*   **Asynchronous Processing:**  Use asynchronous processing to improve performance and scalability.
*   **Logging:**  Improve logging to provide more detailed insights into API usage and performance.
*   **Documentation:**  Expand documentation to include more examples  
*   **Secure Input Sanitization:**  Prevents injection attacks and malicious inputs by escaping special characters and removing unnecessary whitespace.
*   **FastAPI Integration:** Provides a modern, performant API built on FastAPI.
*   **Contributions:** Add details on how to contribute to this project.
*   ** Testing Improvement:** Setup behave framework for more exhaustive testing



## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](https://github.com/saidworks/the_prompt_wrangler/blob/main/CONTRIBUTING.md) file for details on how to contribute.