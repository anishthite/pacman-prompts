from dotenv import load_dotenv

load_dotenv()

import pacman.pacman as pacman
import logfire
import os
# Initialize prompts
prompts = pacman.load("./example.yml")

thinker_prompt = prompts["thinker_prompt"]
final_prompt = prompts["final_prompt"]


def QAchain(context, question):
    msgs = [
        {"role": "user", "content": "blah"},
        {"role": "assistant", "content": "blah"},
    ]
    system_input = {"name": "Claros"}
    user_input = {"context": context, "question": question}
    reasoning = thinker_prompt(
        system_inputs=system_input,
        user_inputs=user_input,
        messages=msgs,
        few_shot=True,
        debug=True,
    )

    user_input = {"question": question, "reasoning": reasoning}
    out = final_prompt(user_input, debug=True)
    return out


QAchain(
    "I have a sister named Anna, Anna has a sister named Elsa",
    "How many sisters do I have?",
)
