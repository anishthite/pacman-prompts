# defines an llm prompt class
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')
if openai.api_key is None:
    raise Exception("OpenAI API key not set")

class PromptConfig:
    def __init__(self, config):
        #set attributes from config
        for name, value in config.items():
            setattr(self, name, value)

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
            prompt=complete_prompt,
            **self.config.__dict__
            #stop='\n'
        )
        return res
        #return output


    def __call__(self, inputs, **kwargs):
        return self.run(inputs, **kwargs)

def load_prompt(loaded_file):
    prompt = Prompt(**loaded_file)

#make copy of Prompt class but use ChatCompletion in run method
class ChatPrompt(Prompt):
    def run(self, inputs, **kwargs):
        #format string
        complete_prompt = self.compile(inputs)
        if  kwargs.get('debug', True):
            print(complete_prompt)
        #run in language model
        res = openai.ChatCompletion.create(
            messages=[{"role": "user","content": complete_prompt}],
            **self.config.__dict__
            #stop='\n'
        )
        return res
        #return output

