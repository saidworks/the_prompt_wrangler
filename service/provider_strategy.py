from service import OllamaModelService,AzureOpenAIModelService

class ProviderStrategy:
    def __init__(self, provider_name: str) -> None:
        if provider_name == "ollama":
            self.provider = OllamaModelService()
        elif provider_name == "azure_open_ai":
            self.provider = AzureOpenAIModelService()
        else:
            raise ValueError("Invalid provider name")
        






