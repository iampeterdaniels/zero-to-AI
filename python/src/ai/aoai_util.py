import asyncio
import sys
import os
import traceback

from pprint import pprint

from docopt import docopt
from dotenv import load_dotenv

import openai
from openai import AzureOpenAI
from openai.types import CreateEmbeddingResponse
from openai.types.chat.chat_completion import ChatCompletion

from src.io.fs import FS

# This Python module defines a class `AOAIUtil` that encapsulates operations
# on the Azure OpenAI service.
# Chris Joakim, 3Cloud/Cognizant, 2026


class AOAIUtil:
    def __init__(self):
        self.embeddings_client = None
        self.completions_client = None

    async def generate_completion(self, system_context: str, user_prompt: str) -> object | None:
        try:
            await asyncio.sleep(0.01)
            url = os.getenv("AZURE_OPENAI_COMPLETIONS_URL")
            key = os.getenv("AZURE_OPENAI_COMPLETIONS_KEY")
            dep = os.getenv("AZURE_OPENAI_COMPLETIONS_DEP")
            vers = os.getenv("AZURE_OPENAI_COMPLETIONS_VERSION")
            #vers = "2024-12-01-preview"
            #Azure OpenAI Responses API is enabled only for api-version 2025-03-01-preview and later

            if self.completions_client is None:
                print("Lazy-initializing the completions client")
                print(f"url: {url}")
                print(f"key: {key}")
                print(f"version: {vers}")
                print(f"deployment: {dep}")
                print(f"openai.__version__: {openai.__version__}")
                self.completions_client = AzureOpenAI(
                    api_version=vers, azure_endpoint=url, api_key=key
                )
                print(f"client type: {type(self.completions_client)}")
                # <class 'openai.lib.azure.AzureOpenAI'>

            # Warning: Be aware of a SDK difference when using newer vs older models.
            # The following code works with gpt-4.1-mini (first url below)but not with 
            # gpt-5-mini (second url below) which uses the new Responses API.
            # This codebase is currently awaiting the maturity of the new Responses API documentation.
            # AZURE_OPENAI_COMPLETIONS_URL="https://xxx.cognitiveservices.azure.com/openai/deployments/gpt-4.1-mini/chat/completions?api-version=2025-01-01-preview"
            # AZURE_OPENAI_COMPLETIONS_URL="https://xxx.cognitiveservices.azure.com/openai/responses?api-version=2025-04-01-preview"

            completion = self.completions_client.chat.completions.create(
                model=dep,
                messages=[
                    {"role": "system", "content": system_context},
                    {"role": "user", "content": user_prompt},
                ],
                stream=False,
                max_completion_tokens=16384,
            )

            print("=== completion type ===")
            print(str(type(completion)))

            print("=== message ===")
            print(completion.choices[0].message)

            print("=== content ===")
            print(completion.choices[0].message.content)
            # Mickey Mantle wore the uniform number 7 for the New York Yankees throughout his Hall of Fame career.

            print("=== model_dump_json ===")
            print(completion.model_dump_json(indent=2))

        except Exception as e:
            print(f"Error generate_completion: {e}")
            print(traceback.format_exc())
            return None

    async def generate_embeddings(self, text: str) -> list[float] | None:
        try:
            await asyncio.sleep(0.01)
            url = os.getenv("AZURE_OPENAI_EMBEDDINGS_URL")
            key = os.getenv("AZURE_OPENAI_EMBEDDINGS_KEY")
            dep = os.getenv("AZURE_OPENAI_EMBEDDINGS_DEP")
            vers = os.getenv("AZURE_OPENAI_EMBEDDINGS_VERSION")

            if self.embeddings_client is None:
                print("Lazy-initializing the embeddings client")
                print(f"url: {url}")
                # print(f"key: {key}")
                print(f"version: {vers}")
                print(f"deployment: {dep}")
                self.embeddings_client = AzureOpenAI(
                    api_key=key, api_version=vers, azure_endpoint=url
                )
            return self.embeddings_client.embeddings.create(input=text, model=dep).data[0].embedding
        except Exception as e:
            print(f"Error generate_embeddings: {e}")
            return None
