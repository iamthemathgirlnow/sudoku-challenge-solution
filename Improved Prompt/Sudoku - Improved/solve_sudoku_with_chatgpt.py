from aiworkshop import send_message, ChatSession, get_tokens
import tiktoken
import time


def get_text_from_file(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    return text

def overwrite_text_file(file_path, str):
    with open(file_path, 'w') as f:
        f.write(str)

def append_to_text_file(file_path, str):
    with open(file_path, 'a') as f:
        f.write(str)

def get_last_n_tokens_from_file(file_path, n):
    encoding = tiktoken.encoding_for_model("gpt-4-0613")
    encoded_response = encoding.encode(get_text_from_file(file_path))
    reduced_encoded_response = encoded_response[-n:]
    return encoding.decode(reduced_encoded_response)

def get_last_n_tokens_from_string(string, n):
    encoding = tiktoken.encoding_for_model("gpt-4-0613")
    encoded_response = encoding.encode(string)
    reduced_encoded_response = encoded_response[-n:]
    return encoding.decode(reduced_encoded_response)

def log_message_to_file(prompts, system_message, message, model, temperature, file_path='message logs.txt', turn=None, prompt_token_count=None, completion_token_count=None):
    if not isinstance(prompts, list):
        prompts = [prompts]
    with open(file_path, 'a') as f:
        if turn is not None:
            f.write(f'turn {turn} - prompt_{"A" if turn % 2 == 1 else "B"}\n\n')
        if prompt_token_count is not None and completion_token_count is not None:
            f.write(f'Prompt tokens: {prompt_token_count}\nCompletion tokens: {completion_token_count}\nTotal tokens: {prompt_token_count + completion_token_count}\n\n')
        f.write(f'model:\n{model}\n\n')
        f.write(f'temperature:\n{temperature}\n\n')
        f.write(f'system_message:\n{system_message}\n\n')
        for index, prompt in enumerate(prompts):
            f.write(f'prompt {index + 1} of {len(prompts)}:\n{prompt}\n\n')
        f.write(f'response:\n{message}\n\n')
        f.write('-'*100 + '\n'*11)





def run_prompt_A(
        puzzle_input_file=None,
        full_attempt=None,
        turn=None,
        full_attempt_log_file_with_turns=None,
        full_attempt_log_file_without_turns=None,
        turn_log_file=None,
        last_response_file=None,
        prompt_file = None,
        ):
    full_attempt = False if full_attempt is None else full_attempt
    prompt_file = 'MAIN - Prompt_A.txt' if prompt_file is None else prompt_file

    if full_attempt:
        if puzzle_input_file is None:
            raise ValueError('input_file must be specified when full_attempt is True')
        if turn is None:
            raise ValueError('turn_number must be specified when full_attempt is True')
        if turn % 2 != 1:
            raise ValueError('turn_number must be odd when full_attempt is True')
        if full_attempt_log_file_with_turns is None:
            raise ValueError('attempt_log_file must be specified when full_attempt is True')
        if full_attempt_log_file_without_turns is None:
            raise ValueError('full_attempt_log_file_without_turns must be specified when full_attempt is True')
        if turn_log_file is None:
            raise ValueError('response_log_file must be specified when full_attempt is True')
        if last_response_file is None:
            raise ValueError('last_response_file must be specified when full_attempt is True')
        
    puzzle_input_file = puzzle_input_file if puzzle_input_file is not None else 'prompt - puzzle input.txt'

    system_message_A = """Follow instructions as given to analyze the current sudoku. When you receive the current sudoku in <output> tags, say ONLY "Awaiting instructions." and NOTHING ELSE. You will then receive instructions including an example sudoku to demonstrate the steps. When you receive the instructions, begin following them Immediately and Fully to analyze the sudoku which was received in the previous message."""
    sudoku_prompt = get_text_from_file(prompt_file)
    puzzle_input_prompt = get_text_from_file(puzzle_input_file)

    model = 'gpt-4-0613'
    prompt_token_count = get_tokens(sudoku_prompt) + get_tokens(puzzle_input_prompt) + get_tokens(system_message_A) + 4 + 19
    max_tokens = 8178 - prompt_token_count
    temperature = 0

    message_history = [
        {"role": "system", "content": system_message_A},
        {"role": "user", "content": puzzle_input_prompt},
        {"role": "assistant", "content": "Awaiting instructions."},
    ]

    chat = ChatSession(message_history=message_history, print_enabled=True, model=model, max_tokens=max_tokens, temperature=temperature)
    response = chat.send_message(sudoku_prompt)

    log_message_to_file(prompts=[puzzle_input_prompt, "Awaiting instructions.", sudoku_prompt], system_message=system_message_A, message=response, model=model, temperature=temperature, file_path='message logs.txt', prompt_token_count=prompt_token_count, completion_token_count=get_tokens(response))
    log_message_to_file(prompts=[puzzle_input_prompt, "Awaiting instructions.", sudoku_prompt], system_message=system_message_A, message=response, model=model, temperature=temperature, file_path='message log - prompt_A.txt', prompt_token_count=prompt_token_count, completion_token_count=get_tokens(response))
    if full_attempt:
        overwrite_text_file(last_response_file, response)
        log_message_to_file(prompts=[puzzle_input_prompt, "Awaiting instructions.", sudoku_prompt], system_message=system_message_A, message=response, model=model, temperature=temperature, file_path=full_attempt_log_file_with_turns, turn=turn, prompt_token_count=prompt_token_count, completion_token_count=get_tokens(response))
        log_message_to_file(prompts=[puzzle_input_prompt, "Awaiting instructions.", sudoku_prompt], system_message=system_message_A, message=response, model=model, temperature=temperature, file_path=full_attempt_log_file_without_turns)
        log_message_to_file(prompts=[puzzle_input_prompt, "Awaiting instructions.", sudoku_prompt], system_message=system_message_A, message=response, model=model, temperature=temperature, file_path=turn_log_file, turn=turn, prompt_token_count=prompt_token_count, completion_token_count=get_tokens(response))





def run_prompt_B(
        puzzle_input_file=None,
        previous_results_file=None,
        full_attempt=None,
        turn=None,
        full_attempt_log_file_with_turns=None,
        full_attempt_log_file_without_turns=None,
        turn_log_file=None,
        last_response_file=None,
        prompt_file = None,
        ):
    full_attempt = False if full_attempt is None else full_attempt
    prompt_file = 'MAIN - Prompt_B.txt' if prompt_file is None else prompt_file

    if full_attempt:
        if puzzle_input_file is None:
            raise ValueError('input_file must be specified when full_attempt is True')
        if previous_results_file is None:
            raise ValueError('previous_results_file must be specified when full_attempt is True')
        if turn is None:
            raise ValueError('turn_number must be specified when full_attempt is True')
        if turn % 2 != 0:
            raise ValueError('turn_number must be even when full_attempt is True')
        if full_attempt_log_file_with_turns is None:
            raise ValueError('attempt_log_file must be specified when full_attempt is True')
        if full_attempt_log_file_without_turns is None:
            raise ValueError('full_attempt_log_file_without_turns must be specified when full_attempt is True')
        if turn_log_file is None:
            raise ValueError('response_log_file must be specified when full_attempt is True')
        if last_response_file is None:
            raise ValueError('last_response_file must be specified when full_attempt is True')
        
    puzzle_input_file = puzzle_input_file if puzzle_input_file is not None else 'prompt - puzzle input.txt'
    previous_results_file = previous_results_file if previous_results_file is not None else 'response - Prompt_A last tokens.txt'

    system_message_B = """Follow ALL instructions METHODICALLY and IN FULL. Your task is to calculate the possible candidate elements for the given cells using the given information, then to update the non-rejected cells of the given sudoku using the calculated candidate elements, then to shift the rows, and finally to output the updated and shifted sudoku. Once you begin you must complete ALL of these tasks BEFORE stopping. After receiving the full instructions you have ONLY one message to finish the task, as soon as you stop responding the final section of your response is sent to the next part of the process. Thus the final text you write MUST be the updated and shifted Sudoku, in the correct format, after ALL other sections have been completed. Begin as soon as you receive the full instruction set."""
    prompt_B_pre_message = """Respond to this message with "Awaiting instructions." and nothing else. When you receive the current sudoku in <output> tags, say only "Awaiting instructions." and nothing else. You will then receive the last few hundred characters of the previous analysis results. When you receive the previous results say "Awaiting instructions." and nothing else. You will then receive instructions. When you receive the instructions, you may begin."""
    puzzle_input_prompt = get_text_from_file(puzzle_input_file)
    previous_results = get_text_from_file(previous_results_file)
    prompt_B = get_text_from_file(prompt_file)

    model = 'gpt-4-0613'
    prompt_token_count = get_tokens(prompt_B) + get_tokens(puzzle_input_prompt) + get_tokens(prompt_B_pre_message) + get_tokens(previous_results) + get_tokens(system_message_B) + 12 + 32
    max_tokens = 8178 - prompt_token_count
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

    log_message_to_file(prompts=[prompt_B_pre_message, "Awaiting instructions.", puzzle_input_prompt, "Awaiting instructions.", previous_results, "Awaiting instructions.", prompt_B], system_message=system_message_B, message=response, model=model, temperature=temperature, file_path='message logs.txt', prompt_token_count=prompt_token_count, completion_token_count=get_tokens(response))
    log_message_to_file(prompts=[prompt_B_pre_message, "Awaiting instructions.", puzzle_input_prompt, "Awaiting instructions.", previous_results, "Awaiting instructions.", prompt_B], system_message=system_message_B, message=response, model=model, temperature=temperature, file_path='message log - prompt_B.txt', prompt_token_count=prompt_token_count, completion_token_count=get_tokens(response))
    if full_attempt:
        overwrite_text_file(last_response_file, response)
        log_message_to_file(prompts=[prompt_B_pre_message, "Awaiting instructions.", puzzle_input_prompt, "Awaiting instructions.", previous_results, "Awaiting instructions.", prompt_B], system_message=system_message_B, message=response, model=model, temperature=temperature, file_path=full_attempt_log_file_with_turns, turn=turn, prompt_token_count=prompt_token_count, completion_token_count=get_tokens(response))
        log_message_to_file(prompts=[prompt_B_pre_message, "Awaiting instructions.", puzzle_input_prompt, "Awaiting instructions.", previous_results, "Awaiting instructions.", prompt_B], system_message=system_message_B, message=response, model=model, temperature=temperature, file_path=full_attempt_log_file_without_turns)
        log_message_to_file(prompts=[prompt_B_pre_message, "Awaiting instructions.", puzzle_input_prompt, "Awaiting instructions.", previous_results, "Awaiting instructions.", prompt_B], system_message=system_message_B, message=response, model=model, temperature=temperature, file_path=turn_log_file, turn=turn, prompt_token_count=prompt_token_count, completion_token_count=get_tokens(response))





def full_attempt_prompt_A(folder, puzzle_date):
    turn = int(get_text_from_file(folder + 'turns_taken.txt')) + 1
    puzzle_input_file = folder + 'initial puzzle.txt' if turn == 1 else folder + 'truncated response_B.txt'
    full_attempt = True
    full_attempt_log_file_with_turns = folder + f'FULL LOG with turns - {puzzle_date} puzzle - prompt version 2.txt'
    full_attempt_log_file_without_turns = folder + f'FULL LOG without turns - {puzzle_date} puzzle - prompt version 2.txt'
    turn_log_file = folder + 'logs by turn/' + f'turn {turn} - prompt_A - log.txt'
    last_response_file = folder + 'last response.txt'

    run_prompt_A(
        puzzle_input_file=puzzle_input_file,
        full_attempt=full_attempt,
        full_attempt_log_file_with_turns=full_attempt_log_file_with_turns,
        full_attempt_log_file_without_turns=full_attempt_log_file_without_turns,
        turn_log_file=turn_log_file,
        last_response_file=last_response_file,
        turn=turn,
    )

    prompt_A_last_tokens = get_last_n_tokens_from_file(folder + 'last response.txt', 400)
    overwrite_text_file(folder + 'truncated response_A.txt', prompt_A_last_tokens)
    if turn == 1:
        append_to_text_file(folder + 'sudoku state output - log.txt', 'turn: 0 (initial input)\n\n' + get_text_from_file(puzzle_input_file) + '\n\n\n\n')
    overwrite_text_file(folder + 'turns_taken.txt', str(turn))
    time.sleep(1)





def full_attempt_prompt_B(folder, puzzle_date):
    turn = int(get_text_from_file(folder + 'turns_taken.txt')) + 1
    puzzle_input_file = folder + 'initial puzzle.txt' if turn == 2 else folder + 'truncated response_B.txt'
    previous_results_file = folder + 'truncated response_A.txt'
    full_attempt = True
    full_attempt_log_file_with_turns = folder + f'FULL LOG with turns - {puzzle_date} puzzle - prompt version 2.txt'
    full_attempt_log_file_without_turns = folder + f'FULL LOG without turns - {puzzle_date} puzzle - prompt version 2.txt'
    turn_log_file = folder + 'logs by turn/' + f'turn {turn} - prompt_B - log.txt'
    last_response_file = folder + 'last response.txt'

    run_prompt_B(
        puzzle_input_file=puzzle_input_file,
        previous_results_file=previous_results_file,
        full_attempt=full_attempt,
        full_attempt_log_file_with_turns=full_attempt_log_file_with_turns,
        full_attempt_log_file_without_turns=full_attempt_log_file_without_turns,
        turn_log_file=turn_log_file,
        last_response_file=last_response_file,
        turn=turn,
    )

    prompt_B_last_tokens = get_last_n_tokens_from_file(folder + 'last response.txt', 210)
    overwrite_text_file(folder + 'truncated response_B.txt', prompt_B_last_tokens)
    append_to_text_file(folder + 'sudoku state output - log.txt', f'turn: {"0 (initial input)" if turn == 1 else str(turn)}\n\n' + get_text_from_file(puzzle_input_file) + '\n\n\n\n')
    overwrite_text_file(folder + 'turns_taken.txt', str(turn))
    time.sleep(1)



# run_prompt_A()
# run_prompt_B()

folder = 'Transcripts/October 5th - improved prompt/'
puzzle_date = 'October 5th'

full_attempt_prompt_A(folder, puzzle_date)
full_attempt_prompt_B(folder, puzzle_date)

full_attempt_prompt_A(folder, puzzle_date)
full_attempt_prompt_B(folder, puzzle_date)

full_attempt_prompt_A(folder, puzzle_date)
full_attempt_prompt_B(folder, puzzle_date)