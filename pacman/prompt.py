# defines an llm prompt class
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# openai.ChatCompletion.create = reliableGPT(openai.ChatCompletion.create,
#     user_email='claros@claros.so',
#     #model_limits_dir = {"gpt-3.5-turbo-0613": {"max_token_capacity": 90000, "max_request_capacity": 3500}},
#     fallback_strategy=['gpt-3.5-turbo-0613', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo', 'gpt-3.5-turbo-16k'],
#     caching=False)

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
        return self.prompt.format(**inputs)

    def run(self, inputs, **kwargs):
        #format string
        complete_prompt = self.compile(inputs)
        if  kwargs.get('debug', True):
            print(complete_prompt)
        #run in language model
        res = client.completions.create(
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


        if kwargs.get('initial_role', None):
            initial_message_list = [{"role": kwargs['initial_role'],"content": complete_prompt}]
        else:
            initial_message_list = [{"role": "user","content": complete_prompt}]

        #if messages passed in add the system prompt to the beginning
        if kwargs.get('messages', None):
            messages = initial_message_list + kwargs['messages']
        else:
            messages = initial_message_list 


        #TODO: fix the inut s . its flat
        #TODO: make this all creatable inside the yaml config
        #TODO: messages is a reserved kwarg, so dont put it in a prompt
        #run in language model
        
        # if self.config['stream'] == True:
        #     try:
        #         resp = ''
        #         for chunk in openai.ChatCompletion.create(
        #             model="gpt-3.5-turbo",
        #             messages=messages,
        #             **self.config.__dict__,
        #         ):
        #             content = chunk["choices"][0].get("delta", {}).get("content")
        #             if content is not None:
        #                 print(content, end='')
        #                 resp += content
        #                 yield f'{content}'
        #     except Exception as e:
        #         print(e)
        #         return str(e)
        # else:


        if kwargs.get('debug', True):
            print("complete prompt:")
            print(messages)


        res = client.chat.completions.create(
            messages=messages,
            **self.config.__dict__
            #stop='\n'
        )
        return res
