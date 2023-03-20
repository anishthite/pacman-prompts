# PACman

## Prompts Are Code, man

A package to make prompts first-party objects in Python


## Examples

example.yaml
```
Prompts:
  thinker_prompt:
    prompt: |- # this is a multiline way of writing strings 
      You are a large language model.
      Context:\ {context}
      {question}
      A:\ Let's think step by step
    inputs: [context, question]
    config:
      model: "text-davinci-003" 
      max_tokens: 100
      temperature: 0.8
      top_p: 0.9
  final_prompt:
      prompt: |- # this is a multiline way of writing strings 
        You are a large language model.
        {question}
        Reasoning:\ {reasoning}
        A:\
      inputs: [question, reasoning]
      config:
        model: "text-davinci-003" 
        max_tokens: 100
        temperature: 0.8
        top_p: 0.9
```

example.py
```
import pacman.pacman as pacman

#Initialize prompts
prompts = pacman.load('./example.yaml')

thinker_prompt = prompts['thinker_prompt']
final_prompt = prompts['final_prompt']

def QAchain(context, question):
    input = {'context': context, 'question': question}
    reasoning = thinker_prompt(input, debug=True)
    
    input = {'question': question, 'reasoning': reasoning}
    out = final_prompt(input, debug=True)
    return out

QAchain('I have a sister named Anna, Anna has a sister named Elsa', 'How many sisters do I have?')
```

## Why I made this
A lot of prompt-heavy code is hard to grasp due to mixed use of large multi-line strings and orchestrating code. Some prompt libraries automate portions of these away, but we lose flexibility in prompting. 

By extrapolating the prompt config to a yaml file and generating pure Python functions from it, we can focus our business code on orchestrating the input/outputs of prompt functions.

Another benefit of moving prompts to YAML files is that it's easy to move prompts between languages, and to track prompt changes via git.

Also, procrastination

## Install
`pip install pacman-prompts`

## Roadmap:

[x] publish package
[] type checking on prompt inputs


