from enum import Enum


class OLLAMA_MODELS(Enum):
    GEMMA3_12B = "gemma3:12b"
    QWEN3_8B = "qwen3:latest"
    GRANITE3_3_8B = "granite3.3:latest"


class AZURE_MODELS(Enum):
    AZURE_GPT3_5 = "gpt-35-turbo"


class PROMPT_TEMPLATE(Enum):
    DEFAULT_SYSTEM_PROMPT = """You are a medical data extraction assistant, your job is to extract metadata about medical equipment
                                from an unstructured user text input.."""


class LLM_PROVIDERS(Enum):
    OLLAMA = "ollama"
    AZURE = "azure_open_ai"
