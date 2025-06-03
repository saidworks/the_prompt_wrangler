from service.azure_open_ai import AzureOpenAIModelService
from service.ollama import OllamaModelService
from util.llm_constants import OLLAMA_MODELS, LLM_PROVIDERS
from util.log_util import get_logger


DEFAULT_MODEL = OLLAMA_MODELS.GEMMA3_12B.value


class ProviderStrategy:
    def __init__(
        self,
        provider_name: str,
        top_p, top_k,
        model_reference: str = DEFAULT_MODEL,
        temperature: float = 0.7,
        max_tokens: int = 512, 
    ) -> None:
        self.log = get_logger(type(self).__name__)
        if provider_name == LLM_PROVIDERS.OLLAMA.name:
            self.provider = OllamaModelService(model_reference, temperature, max_tokens, top_p, top_k,)
        elif provider_name == LLM_PROVIDERS.AZURE.name:
            self.provider = AzureOpenAIModelService(temperature, max_tokens, top_p, top_k,)

        else:
            raise ValueError("Invalid provider name")

    def call_llm(self, input_text):
        return self.provider.call_llm(input_text)
