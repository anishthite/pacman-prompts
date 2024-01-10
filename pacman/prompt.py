# defines an llm prompt class
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
import openai



openai_client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

anyscale_client =  openai.OpenAI(
                base_url="https://api.endpoints.anyscale.com/v1",
                api_key=os.environ["MISTRAL_API_KEY"]
            )

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
    def __init__(self, prompts, config):

        self.config = PromptConfig(config)

        if 'provider' in config:
            self.provider = config['provider']
            del config['provider']
        else:
            self.provider = 'openai'

        if type(prompts) == str:
            self.user_prompt = prompts
            return

        if 'system' not in prompts and 'user' not in prompts:
            raise Exception("Prompt must have either system prompt or user prompt")
        if 'system' in prompts:
            self.system_prompt = prompts['system']
        if 'user' in prompts:
            self.user_prompt = prompts['user']


    def compile(self, inputs):
        print(**inputs)
        return self.prompt.format(**inputs)

    def run(self, system_inputs=None, user_inputs=None, **kwargs):
        #format string
        complete_prompt = self.compile(user_inputs)
        if  kwargs.get('debug', True):
            print(complete_prompt)
        #run in language model
        res = openai_client.completions.create(
            prompt=complete_prompt,
            **self.config.__dict__
            #stop='\n'
        )
        return res
        #return output

    def __call__(self, *args, system_inputs=None, user_inputs=None, **kwargs):

        if len(args) == 0:
            return self.run(system_inputs=system_inputs, user_inputs=user_inputs, **kwargs)

        if len(args) == 1:
            return self.run(user_inputs=args[0], **kwargs)

        raise ValueError("Invalid number of arguments for __call__ method.")

def load_prompt(loaded_file):
    prompt = Prompt(**loaded_file)

#make copy of Prompt class but use ChatCompletion in run method
class ChatPrompt(Prompt):

    def run(self, system_inputs=None, user_inputs=None, **kwargs):
        #format string
        if hasattr(self, 'system_prompt'):
            system_prompt = self.system_prompt.format(**system_inputs)
        if hasattr(self, 'user_prompt'):
            user_prompt = self.user_prompt.format(**user_inputs)

# if system and user add them as messages, otherwise add the one that exists
        if hasattr(self, 'system_prompt') and hasattr(self, 'user_prompt'):
            initial_message_list = [{"role": "system","content": system_prompt},{"role": "user","content": user_prompt}]
        elif hasattr(self, 'system_prompt'):
            initial_message_list = [{"role": "system","content": system_prompt}]
        elif hasattr(self, 'user_prompt'):
            initial_message_list = [{"role": "user","content": user_prompt}]
        else:
            raise Exception("Prompt must have either system_prompt or user_prompt")

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


        # [existing code to prepare messages]

        # Conditional API call based on provider
        if self.provider == "openai":
            res = openai_client.chat.completions.create(
                messages=messages,
                **self.config.__dict__
                #stop='\n'
            )
        elif self.provider == "anyscale":
            res = anyscale_client.chat.completions.create(
                model=self.config.__dict__["model"],
                messages=messages,
                temperature=self.config.__dict__["temperature"]
            )
        return res