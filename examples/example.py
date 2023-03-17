import pacman.pacman as pacman

#Initialize prompts
prompts = pacman.load('./example.yml')

thinker_prompt = prompts['thinker_prompt']
final_prompt = prompts['final_prompt']

def QAchain(context, question):
    input = {'context': context, 'question': question}
    reasoning = thinker_prompt(input, debug=True)
    
    input = {'question': question, 'reasoning': reasoning}
    out = final_prompt(input, debug=True)
    return out

QAchain('I have a sister named Anna, Anna has a sister named Elsa', 'How many sisters do I have?')


