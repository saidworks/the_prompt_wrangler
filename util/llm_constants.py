from enum import Enum


class AVAILABLE_MODELS(Enum):
    gemma3_12b = "gemma3:12b"
    mistral_7b = "mistral:latest"
    deepseek_r1 = "deepseek-r1:14b"
    azure_gpt3_5 = "gpt-35-turbo"

class PROMPT_TEMPLATE(Enum):
    DEFAULT_SYSTEM_PROMPT= """You are a medical data extraction assistant, your job is to extract metadata about medical equipment
                                from an unstructured user text input.."""