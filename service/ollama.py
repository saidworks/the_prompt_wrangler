from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from model.output_parser import Output
from service.provider import Provider
from util.log_util import logger
import time
import json
from util.llm_constants import PROMPT_TEMPLATE
from util.usage_statistics import extract_metadata


class OllamaModelService(Provider):
    def __init__(
        self, model_reference, temperature, max_tokens, top_p, top_k, parser=Output
    ):
        self.model_reference = model_reference
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.top_k = top_k
        self.parser = parser

    def load_model(self):
        """Loads and initializes the Ollama Chat model."""
        try:
            ollama_client = ChatOllama(
                model=self.model_reference,
                temperature=self.temperature,
                num_predict=self.max_tokens,
                top_k=self.top_k,
                top_p=self.top_p,
            )
            ollama_structured = ollama_client.with_structured_output(
                self.parser, include_raw=True
            )
            return ollama_structured
        except Exception as e:
            logger.info(f"Failed to initialize Ollama client: {e}")
            raise Exception

    def generate_prompt(self, input_text):
        """Generates the prompt for the language model."""
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", PROMPT_TEMPLATE.DEFAULT_SYSTEM_PROMPT.value),
                ("human", input_text),
            ]
        )
        return prompt

    def call_llm(self, input_text):
        """Calls the language model to generate a response."""
        try:
            start_time = time.time()
            prompt = self.generate_prompt(input_text)
            ollama_client = self.load_model()
            chain = prompt | ollama_client
            response = chain.invoke({})
            end_time = time.time()
            response_time = end_time - start_time
            metadata = extract_metadata(response["raw"])
            logger.info(f"response looks like {response}")
            logger.info(f"LLM response time: {response_time} seconds")
            return response["parsed"].final_output, metadata
        except Exception as e:
            logger.error(f"Error during LLM execution: {e}")
            return json.dumps({"error": str(e)})
