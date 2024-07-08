# load yml and initialize the prompts
from .file_utils import load_yml
from .prompt import Prompt, ChatPrompt, InstuctorPrompt
import os


def load(yaml_path):
    """Load a yaml file and return the prompts"""
    parsed_file = load_yml(yaml_path)
    prompt_collection = {}
    if "Prompts" in parsed_file:
        for name, config in parsed_file["Prompts"].items():
            prompt_collection[name] = Prompt(
                config["prompts"], config["provider"], config["config"], name
            )
    if "ChatPrompts" in parsed_file:
        for name, config in parsed_file["ChatPrompts"].items():
            if "prompts" in config:
                prompt_collection[name] = ChatPrompt(
                    config["prompts"], config["provider"], config["config"], name
                )
            else:
                prompt_collection[name] = ChatPrompt(
                    config["prompt"], config["provider"], config["config"], name
                )
    if "InstructorPrompts" in parsed_file:
        for name, config in parsed_file["InstructorPrompts"].items():
            if "prompts" in config:
                prompt_collection[name] = InstuctorPrompt(
                    config["prompts"], config["provider"], config["config"], name
                )
            else:
                prompt_collection[name] = ChatPrompt(
                    config["prompt"], config["provider"], config["config"], name
                )

    return prompt_collection


def load_folder(folder_path):
    """Load a folder of yaml files and return the prompts"""
    prompt_collection = {}
    for file in os.listdir(folder_path):
        if file.endswith(".yml"):
            prompts = load(os.path.join(folder_path, file))
            prompt_collection.update(prompts)
    return prompt_collection
