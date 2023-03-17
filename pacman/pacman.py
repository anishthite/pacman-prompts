# load yml and initialize the prompts
from .file_utils import load_yml
from .prompt import Prompt

def load(yaml_path):
    """Load a yaml file and return the prompts"""
    parsed_file = load_yml(yaml_path)
    prompt_collection = {} 
    for name, config in parsed_file['Prompts'].items():
        prompt_collection[name] = Prompt(config['prompt'], config['config'])
    return prompt_collection
