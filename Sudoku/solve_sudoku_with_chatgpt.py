from aiworkshop import send_message, ChatSession, get_tokens


def get_prompt_from_file(file_path):
    with open(file_path, 'r') as f:
        prompt = f.read()
    return prompt

def log_message_to_file(prompts, system_message, message, model, temperature, file_path='message logs.txt'):
    if not isinstance(prompts, list):
        prompts = [prompts]
    with open(file_path, 'a') as f:
        f.write(f'model:\n{model}\n\n')
        f.write(f'temperature:\n{temperature}\n\n')
        f.write(f'system_message:\n{system_message}\n\n')
        for index, prompt in enumerate(prompts):
            f.write(f'prompt {index + 1} of {len(prompts)}:\n{prompt}\n\n')
        f.write(f'response:\n{message}\n\n')
        f.write('-'*100 + '\n'*11)



# model = 'gpt-3.5-turbo-0613'
# model = 'gpt-3.5-turbo-16k-0613'




# # First Turn
# log_file = 'attempt 2 - log file.txt'
# prompt_file = 'prompt - prompt_A.txt'
# system_message_A = """Follow instructions as given to analyze the current sudoku. When you receive the current sudoku in <output> tags, say ONLY "Awaiting instructions." and NOTHING ELSE. You will then receive instructions including an example sudoku to demonstrate the steps. When you receive the instructions, begin following them Immediately and Fully to solve the sudoku which was received in the previous message."""
# puzzle_input_prompt = get_prompt_from_file('prompt - puzzle input.txt')

# model = 'gpt-4-0613'
# max_tokens = 20
# temperature = 0

# message_history = [
#     {"role": "system", "content": system_message_A},
# ]

# chat = ChatSession(message_history=message_history, print_enabled=True, model=model, max_tokens=max_tokens, temperature=temperature)
# response = chat.send_message(puzzle_input_prompt)
# log_message_to_file(prompts=[puzzle_input_prompt], system_message=system_message_A, message=response, model=model, temperature=temperature, file_path=log_file)
# log_message_to_file(prompts=[puzzle_input_prompt], system_message=system_message_A, message=response, model=model, temperature=temperature, file_path='message logs.txt')





# # Prompt A
# log_file = 'attempt 2 - log file.txt'
# prompt_file = 'prompt - prompt_A.txt'
# # prompt_file = 'prompt - main prompt.txt'
# # prompt_file = 'prompt - main prompt reduced.txt'
# # prompt_file = 'prompt - main prompt testing.txt'
# system_message_A = """Follow instructions as given to analyze the current sudoku. When you receive the current sudoku in <output> tags, say ONLY "Awaiting instructions." and NOTHING ELSE. You will then receive instructions including an example sudoku to demonstrate the steps. When you receive the instructions, begin following them Immediately and Fully to solve the sudoku which was received in the previous message."""
# sudoku_prompt = get_prompt_from_file(prompt_file)
# puzzle_input_prompt = get_prompt_from_file('prompt - puzzle input.txt')

# model = 'gpt-4-0613'
# max_tokens = 8178 - get_tokens(sudoku_prompt) - get_tokens(puzzle_input_prompt) - get_tokens(system_message_A) - 4 - 32
# temperature = 0

# message_history = [
#     {"role": "system", "content": system_message_A},
#     {"role": "user", "content": puzzle_input_prompt},
#     {"role": "assistant", "content": "Awaiting instructions."},
# ]

# chat = ChatSession(message_history=message_history, print_enabled=True, model=model, max_tokens=max_tokens, temperature=temperature)
# response = chat.send_message(sudoku_prompt)
# log_message_to_file(prompts=[puzzle_input_prompt, "Awaiting instructions.", sudoku_prompt], system_message=system_message_A, message=response, model=model, temperature=temperature, file_path=log_file)
# log_message_to_file(prompts=[puzzle_input_prompt, "Awaiting instructions.", sudoku_prompt], system_message=system_message_A, message=response, model=model, temperature=temperature, file_path='message logs.txt')





# Prompt B
log_file = 'attempt 2 - log file.txt'
system_message_B = """Follow ALL instructions METHODICALLY and IN FULL. Your task is to calculate the possible candidate elements for the given cells, then to update the non-rejected cells of the given sudoku using the calculated candidate elements, then to shift the rows, and finally to output the updated and shifted sudoku. Once you begin you must complete ALL of these tasks BEFORE stopping. After receiving the full instructions you have ONLY one message to finish the task, as soon as you stop responding the final section of your response is sent to the next part of the process. Thus the final text you write MUST be the updated and shifted Sudoku, in the correct format, after ALL other sections have been completed. Begin as soon as you receive the full instruction set."""
prompt_B_pre_message = """Respond to this message with "Awaiting instructions." and nothing else. When you receive the current sudoku in <output> tags, say only "Awaiting instructions." and nothing else. You will then receive the last few hundred characters of the previous analysis results. When you receive the previous results say "Awaiting instructions." and nothing else. You will then receive instructions. When you receive the instructions, you may begin."""
puzzle_input_prompt = get_prompt_from_file('prompt - puzzle input.txt')
previous_results = get_prompt_from_file('response - Prompt_A last tokens.txt')
prompt_B = get_prompt_from_file('prompt - prompt_B.txt')

model = 'gpt-4-0613'
max_tokens = 8178 - get_tokens(prompt_B) - get_tokens(puzzle_input_prompt) - get_tokens(prompt_B_pre_message) - get_tokens(previous_results) - get_tokens(system_message_B) - 12 - 36
temperature = 0

message_history = [
    {"role": "system", "content": system_message_B},
    {"role": "user", "content": prompt_B_pre_message},
    {"role": "assistant", "content": "Awaiting instructions."},
    {"role": "user", "content": puzzle_input_prompt},
    {"role": "assistant", "content": "Awaiting instructions."},
    {"role": "user", "content": previous_results},
    {"role": "assistant", "content": "Awaiting instructions."},
]

chat = ChatSession(message_history=message_history, print_enabled=True, model=model, max_tokens=max_tokens, temperature=temperature)
response = chat.send_message(prompt_B)
log_message_to_file(prompts=[prompt_B_pre_message, "Awaiting instructions.", puzzle_input_prompt, "Awaiting instructions.", previous_results, "Awaiting instructions.", prompt_B], system_message=system_message_B, message=response, model=model, temperature=temperature, file_path=log_file)
log_message_to_file(prompts=[prompt_B_pre_message, "Awaiting instructions.", puzzle_input_prompt, "Awaiting instructions.", previous_results, "Awaiting instructions.", prompt_B], system_message=system_message_B, message=response, model=model, temperature=temperature, file_path='message logs.txt')





# # Testing Prompt C
# prompt_C = get_prompt_from_file('prompt - Prompt_C.txt')
# # system_message = """Follow ALL instructions as given. Your task is to METHODICALLY confirm or reject the cells to be updated, then to update the sudoku, then to shift the rows, and finally to output the updated and shifted sudoku. You must complete ALL of these tasks BEFORE stopping, because as soon as you stop responding the final section of your response is sent to the next part of the process. Thus the final text you write before stopping MUST be the outputted Sudoku, in the correct format, after ALL other sections have been completed."""
# system_message_C = """Follow ALL instructions METHODICALLY and IN FULL. Your task is to update specific cells of the given sudoku using the provided candidate elements, then to shift the rows, and finally to output the updated and shifted sudoku. You must complete ALL of these tasks BEFORE stopping. As soon as you stop responding the final section of your response is sent to the next part of the process. Thus the final text you write MUST be the outputted Sudoku, in the correct format, after ALL other sections have been completed."""

# model = 'gpt-4-0613'
# max_tokens = 8178 - get_tokens(prompt_C) - get_tokens(system_message_C) - 4 - 32
# temperature = 0

# message_history = [
#     {"role": "system", "content": system_message_C},
# ]

# chat = ChatSession(message_history=message_history, print_enabled=True, model=model, max_tokens=max_tokens, temperature=temperature)
# response = chat.send_message(prompt_C)
# log_message_to_file(prompts=[prompt_C], system_message=system_message_C, message=response, model=model, temperature=temperature, file_path='message logs.txt')







# # Test
# sudoku_prompt = "hello"

# model = 'gpt-4-0613'
# max_tokens = 10
# temperature = 0

# message = send_message(message=sudoku_prompt, print_enabled=True, model=model, max_tokens=max_tokens, temperature=temperature)
# log_message_to_file(prompts=sudoku_prompt, system_message="", message=message, model=model, temperature=temperature)





# # Old Code
# message = send_message(message=sudoku_prompt, print_enabled=True, model=model, max_tokens=max_tokens, temperature=temperature, system_message=system_message)
# log_message_to_file(prompts=sudoku_prompt, system_message=system_message, message=message, model=model, temperature=temperature, file_path=log_file)


# # last_response = get_prompt_from_file('last_response.txt')
# # last_response = get_prompt_from_file('response - accurate first section.txt')
# message_history = [
#     {"role": "system", "content": system_message},
#     {"role": "user", "content": sudoku_prompt},
#     {"role": "assistant", "content": last_response},
# ]
    
# chat = ChatSession(message_history=message_history, print_enabled=True, model=model, max_tokens=max_tokens, temperature=temperature)
# # response = chat.send_message("""Continue and complete all remaining instructions.""")
# response = chat.send_message(continue_prompt)
# log_message_to_file(prompts=[sudoku_prompt, last_response], system_message=system_message, message=response, model=model, temperature=temperature, file_path=log_file)