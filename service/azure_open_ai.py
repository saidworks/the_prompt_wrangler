from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from model.output_parser import Output
from service.provider import Provider
from util.log_util import logger
import time
import json
import os
"""
TO DO use load config with .env file to get azure openai endpoint and api key
"""

class AzureOpenAIModelService(Provider):
    def __init__(self, temperature, max_tokens, parser=Output):
        self.azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
        self.azure_openai_api_key = os.environ["AZURE_OPENAI_API_KEY"]
        self.model = "gpt-35-turbo"
        self.api_version = "2024-12-01-preview"
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.parser = parser

    def load_model(self):
        """Loads and initializes the Azure OpenAI Chat model."""
        try:
            print("Loading Azure OpenAI model...")
            print(self.azure_openai_endpoint)
            azure_client = AzureChatOpenAI(
                azure_endpoint=self.azure_openai_endpoint,
                openai_api_key=self.azure_openai_api_key,
                deployment_name=self.model,
                model_name=self.model,
                api_version = self.api_version,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                logprobs = True
                )
            return azure_client.with_structured_output(self.parser)
        except Exception as e:
            logger.info(f"Failed to initialize Azure OpenAI client: {e}")
            raise Exception

    def generate_prompt(self, input_text):
        """Generates the prompt for the language model."""
        system_prompt = """You are a medical data extraction assistant, your job is to extract metadata about medical equipment
                                from an unstructured user text input.."""

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("user",input_text),

            ]
        )
        return prompt

    def call_llm(self, input_text):
        """Calls the language model to generate a response."""
        try:
            start_time = time.time()
            prompt = self.generate_prompt(input_text)
            azure_client = self.load_model()
            chain = prompt | azure_client 
            response = chain.invoke({})
            end_time = time.time()
            response_time = end_time - start_time
            logger.info(f"LLM response time: {response_time} seconds")
            return response.final_output
        except Exception as e:
            logger.error(f"Error during LLM execution: {e}")
            return json.dumps({"error": str(e)})
        
