from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from model.output_parser import Output
from util.log_util import logger
import time
import json

"""
TO DO implement strategy and add another provider service
"""

class OllamaModelService:
    def __init__(self, model_reference, temperature, max_tokens, format, parser=Output):
        self.model_reference = model_reference
        self.temperature = temperature 
        self.max_tokens = max_tokens
        self.format = format
        self.parser = parser


    def load_ollama_model(self,parser=Output):
        """Loads and initializes the Ollama Chat model."""
        try:
            ollama_client = ChatOllama(model=self.model_reference,
                                       temperature=self.temperature,
                                       num_predict=self.max_tokens)
            ollama_structured = ollama_client.with_structured_output(parser)
            return ollama_structured
        except Exception as e:
          logger.info(f"Failed to initialize Ollama client: {e}") 
          raise Exception

    def generate_prompt(self, user_prompt, input_text):
        """Generates the prompt for the language model."""
        system_prompt = user_prompt if user_prompt != None else "You are a medical data extraction assistant."

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human",input_text),

            ]
        )
        return prompt

    def call_llm(self, user_prompt, input_text):
        """Calls the language model to generate a response."""
        try:
            start_time = time.time()
            prompt = self.generate_prompt(user_prompt, input_text)
            ollama_client = self.load_ollama_model()
            chain = prompt | ollama_client
            response = chain.invoke({})
            end_time = time.time()
            response_time = end_time - start_time
            logger.info(f"LLM response time: {response_time} seconds")
            return response.final_output
        except Exception as e:
            logger.error(f"Error during LLM execution: {e}")
            return json.dumps({"error": str(e)})



         


