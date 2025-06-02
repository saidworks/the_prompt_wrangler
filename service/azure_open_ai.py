from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from model.output_parser import Output
from util.usage_statistics import extract_metadata
from service.provider import Provider
from util.llm_constants import PROMPT_TEMPLATE,AZURE_MODELS
from util.log_util import logger
import time
import json
import os

from langchain_core.output_parsers import PydanticOutputParser
"""
TO DO use load config with .env file to get azure openai endpoint and api key
"""

class AzureOpenAIModelService(Provider):
    def __init__(self, temperature, max_tokens, parser = Output ):
        self.azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
        self.azure_openai_api_key = os.environ["AZURE_OPENAI_API_KEY"]
        self.model = AZURE_MODELS.AZURE_GPT3_5.value
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
            return azure_client.with_structured_output(self.parser, include_raw=True)
        except Exception as e:
            logger.info(f"Failed to initialize Azure OpenAI client: {e}")
            raise Exception

    def generate_prompt(self, input_text):
        """Generates the prompt for the language model."""
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", PROMPT_TEMPLATE.DEFAULT_SYSTEM_PROMPT.value),
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
            metadata = extract_metadata(response['raw'], start_time, end_time)
            print(metadata)
            return response["parsed"].final_output
        except Exception as e:
            logger.error(f"Error during LLM execution: {e}")
            return json.dumps({"error": str(e)})
        
