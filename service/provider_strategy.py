from service.azure_open_ai import AzureOpenAIModelService
from service.ollama import OllamaModelService
from util.llm_constants import AVAILABLE_MODELS

# set a default model value
DEFAULT_MODEL = AVAILABLE_MODELS.gemma3_12b.value 

class ProviderStrategy:
    def __init__(self, provider_name: str, model_reference : str = DEFAULT_MODEL,  temperature:float = 0.7, max_tokens:int = 512) -> None:
        if provider_name == "ollama":
            self.provider = OllamaModelService(model_reference, temperature, max_tokens)
        elif provider_name == "azure_open_ai":
            self.provider = AzureOpenAIModelService(temperature, max_tokens)
        else:
            raise ValueError("Invalid provider name")
    def call_llm(self, input_text):
        return self.provider.call_llm(input_text)
