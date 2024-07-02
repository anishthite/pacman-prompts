from dotenv import load_dotenv

load_dotenv()

import pacman.pacman as pacman
from pydantic import BaseModel, Field


class Output(BaseModel):
    chain_of_thought: str = Field(
        ..., description="Think step by step to determine the correct title"
    )
    answer: int  =  Field(description="the integer answer to the question")


# Initialize prompts
prompts = pacman.load("./InstructorAnyscale.yml")


thinker_prompt = prompts["instructor"]


def QAchain(context, question):
    msgs = [
        {"role": "user", "content": "blah"},
        {"role": "assistant", "content": "blah"},
    ]
    system_input = {"name": "Claros"}
    user_input = {"context": context, "question": question}
    response_model = thinker_prompt(
        system_inputs=system_input,
        user_inputs=user_input,
        messages=msgs,
        few_shot=True,
        debug=True,
        response_model=Output,
    )
    return response_model


resp = QAchain(
    "I have a sister named Anna, Anna has a sister named Elsa",
    "How many sisters do I have?",
)
print(type(resp))
print(resp)
