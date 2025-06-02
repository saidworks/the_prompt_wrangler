# Prompt Wrangler API

[![License](https://img.shields.io/license/MIT/master)](https://github.com/your-username/prompt-wrangler/blob/master/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11
+-informational)](https://www.python.org/)

## Overview

The Prompt Wrangler API provides a secure and controlled interface for interacting with Language Models (LLMs). It focuses on input sanitization, parameter control, and observability to ensure responsible and reliable LLM usage. Built with Streamlit and Langchain, it prioritizes clean API design and robust error handling.

## Features

*   **Secure Input Sanitization:**  Prevents injection attacks and malicious inputs by escaping special characters and removing unnecessary whitespace.
*   **Controlled LLM Parameters:** Limits `temperature`, `max_tokens`, and `top_p` to ensure predictable and manageable outputs.
*   **Observability:** Logs processing time to monitor performance.  (Token counting is a planned enhancement).
*   **FastAPI Integration:** Provides a modern, performant API built on FastAPI.
*   **Langchain Powered:** Leverages Langchain for efficient LLM interaction.
*   **Clear Error Handling:**  Provides detailed error messages for debugging.

## Prerequisites

*   **Python 3.11+**
*   **Ollama:** A framework to run language models locally.  [https://ollama.com/](https://ollama.com/)
*   **An LLM Model:** You're using the default gemma3:12b. Can be changed in the code.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/prompt-wrangler.git
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
2.  **Install dependencies:**
    To install dependencies you will need to install uv follow instruction on the following (link)[https://docs.astral.sh/uv/getting-started/installation/]
    ```bash
    uv sync
    ```

3.  **Run Ollama and download the model:**

    Ensure you have Ollama installed and running, if not use the following (link)[https://ollama.com/] to install it.  Then ensure that the default model (gemma3:12b) is available. If not, pull the model:

    ```bash
    ollama pull gemma3:12b
    ```
## LLM Providers:

-   **OLLAMA:** Supports models like `gemma3:12b`, `qwen3:latest`, and `granite3.3:latest`. 
    best results were achieved using the `gemma3:12b` model based on multiple empirical testing with provided inputs.
-   **AZURE:** Supports model `gpt-35-turbo` is the only model I tried and it achieves similar results to `gemma3:12b` model. 





## Usage

1.  **Start the API:**

    ```bash
    uvicorn main:app --reload
    ```
    (Replace `main` with the name of your Python file if it's different.)  The `--reload` flag enables automatic code reloading during development.

2.  **Send a POST request to `/process_text/`:**

    Use a tool like `curl`, `Postman`, or a Python `requests` script to send a JSON payload to the API endpoint.

    **Example using `curl`:**

    ```bash
    curl -X POST \
      http://localhost:8000/process_text/ \
      -H 'Content-Type: application/json' \
      -d '{"text": "Your input text here"}'
    ```

    **Example using Python `requests`:**

    ```python
    import requests
    import json

    url = "http://localhost:8000/process_text/"
    headers = {'Content-Type': 'application/json'}
    data = {'text': 'Your input text here'}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(response.json())
    ```

## API Endpoint

*   **`POST /process_text/`**: Processes the provided input text using the configured LLM.

    *   **Request Body:**  JSON payload with a `text` field containing the input string.
        ```json
        {
          "text": "Your input text here"
        }
        ```
    *   **Response:** JSON payload containing the result of the LLM processing, or an error message.
        *   **Success:**
            ```json
            {
              "result": "The LLM's generated response",
              "status": "success"
            }
            ```
        *   **Error:**
            ```json
            {
              "error": "Error message from the LLM or API",
              "status": "failed"
            }
            ```

## Configuration

*   **Model Name:**  The default model is `gemma3:12b`.  You can change this by modifying the `model_name` parameter in the `PromptWrangler` class constructor within the `main.py` file.
*   **LLM Parameters:** The `temperature`, `max_tokens`, and `top_p` parameters are configured within the `llm_params` dictionary.  Adjust these values to fine-tune the LLM's output.

## Future Enhancements

*   **Token Counting:** Implement token counting to accurately measure API usage and costs.
*   **Input Validation:** Add more robust input validation to prevent errors and enhance security.
*   **Authentication:**  Add authentication to control API access.
*   **Rate Limiting:**  Implement rate limiting to prevent abuse and ensure fair usage.
*   **Asynchronous Processing:**  Use asynchronous processing to improve performance and scalability.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/your-username/prompt-wrangler/blob/master/LICENSE) file for details.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](https://github.com/your-username/prompt-wrangler/blob/master/CONTRIBUTING.md) file for details on how to contribute.