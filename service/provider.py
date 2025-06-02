from abc import ABCMeta, abstractmethod

class Provider:
    __metaclass__ = ABCMeta
    @abstractmethod
    def generate_prompt(self, input_text): raise NotImplementedError
    
    @abstractmethod
    def load_ollama_model(self): raise NotImplementedError
    @abstractmethod
    def call_llm(self, input_text): raise NotImplementedError



