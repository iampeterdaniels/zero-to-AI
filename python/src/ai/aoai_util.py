import asyncio
import sys
import os
import traceback

from pprint import pprint

from docopt import docopt
from dotenv import load_dotenv

import openai
from openai import OpenAI
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

            if self.completions_client is None:
                print("Lazy-initializing the completions client")
                print(f"url: {url}")
                # print(f"key: {key}")
                print(f"version: {vers}")
                print(f"deployment: {dep}")
                self.completions_client = AzureOpenAI(
                    api_key=key, api_version=vers, azure_endpoint=url
                )

            # response = self.completions_client.chat.completions.create(
            #     messages=[
            #         {
            #             "role": "system",
            #             "content": "You are a helpful assistant.",
            #         },
            #         {
            #             "role": "user",
            #             "content": "I am going to Paris, what should I see?",
            #         }
            #     ],
            #     max_completion_tokens=16384,
            #     model=dep
            # )

            completion = self.completions_client.chat.completions.create(
                model=dep,  # MUST be the deployment name, not necessarily the model name
                messages=[
                    {"role": "system", "content": system_context},
                    {"role": "user", "content": user_prompt},
                ],
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
