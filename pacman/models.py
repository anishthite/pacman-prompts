# defines an llm prompt class
import os
import openai
import anthropic
import instructor
from groq import Groq
from enum import Enum
import logfire

logfire.configure(token=os.environ["LOGFIRE_TOKEN"])


openai_client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
anthropic_client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
)
anyscale_client = openai.OpenAI(
    base_url="https://api.endpoints.anyscale.com/v1",
    api_key=os.environ["MISTRAL_API_KEY"],
)
groq_client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

instructor_openai_client = instructor.patch(
    openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
)
instructor_anthropic_client = instructor.from_anthropic(anthropic_client)
instructor_anyscale_client = instructor.patch(openai.OpenAI(
        base_url="https://api.endpoints.anyscale.com/v1",
        api_key=os.environ["MISTRAL_API_KEY"],
    ), mode=instructor.Mode.JSON_SCHEMA,
)
instructor_groq_client = instructor.from_groq(groq_client, mode=instructor.Mode.TOOLS)


try:
    logfire.instrument_openai(openai_client)
except Exception as e:
    print("Failed to instrument OpenAI client with Logfire.", e)

try:
    logfire.instrument_anthropic(anthropic_client)
except Exception as e:
    print("Failed to instrument Anthropic client with Logfire.", e)

try:
    logfire.instrument_openai(instructor_openai_client)
except Exception as e:
    print("Failed to instrument Instructor OpenAI client with Logfire.", e)

try:
    logfire.instrument_anthropic(instructor_anthropic_client)
except Exception as e:
    print("Failed to instrument Instructor Anthropic client with Logfire.", e)


groq_anyscale_model_id_map = {
    "llama3-70b-8192": "meta-llama/Meta-Llama-3-70B-Instruct",
    "mixtral-8x7b-32768": "mistralai/Mixtral-8x7B-Instruct-v0.1"
}


class Provider(Enum):
    OPENAI = "openai"
    ANYSCALE = "anyscale"
    ANTHROPIC = "anthropic"
    GROQ = "groq"

