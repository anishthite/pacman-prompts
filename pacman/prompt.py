# defines an llm prompt class
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')
if openai.api_key is None:
    openai.api_key = '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'


class PromptConfig:
    def __init__(self, config):
        self.max_tokens = config['max_tokens']
        self.temperature = config['temperature']
        self.top_p = config['top_p']

class Prompt:
    def __init__(self, prompt, config):
        self.prompt = prompt
        self.config = PromptConfig(config)

    def compile(self, inputs):
        print(inputs)
        return self.prompt.format(**inputs)

    def run(self, inputs, **kwargs):
        #format string
        complete_prompt = self.compile(inputs)
        if  kwargs.get('debug', True):
            print(complete_prompt)
        #run in language model
        res = openai.Completion.create(
            model='text-davinci-003',
            prompt=complete_prompt,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            top_p=self.config.top_p
            #stop='\n'
        )
        return res['choices'][0]['text']
        #return output


    def __call__(self, inputs, **kwargs):
        return self.run(inputs, **kwargs)

def load_prompt(loaded_file):
    prompt = Prompt(**loaded_file)


