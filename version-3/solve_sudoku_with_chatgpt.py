from aiworkshop import ChatSession, get_tokens
import tiktoken
import time
import os
import sudoku_tools as st


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

def get_last_n_tokens_from_string(string, n):
    encoding = tiktoken.encoding_for_model("gpt-4-0613")
    encoded_response = encoding.encode(string)
    return encoded_response[-n:]

def get_tokens_from_string(string):
    encoding = tiktoken.encoding_for_model("gpt-4-0613")
    return encoding.encode(string)

def get_string_from_tokens(token_list):
    encoding = tiktoken.encoding_for_model("gpt-4-0613")
    return encoding.decode(token_list)

def log_message_to_file(
        entries_to_log,
        system_message,
        model,
        temperature,
        file_path='Logs/message logs.txt',
        turn=None,
        prompt_token_count=0,
        completion_token_count=0,
        total_prompt_token_count=0,
        total_completion_token_count=0,
        start_time=None,
        seed=None,
        fingerprint=None,
        ):
    if not isinstance(entries_to_log, list):
        entries_to_log = [entries_to_log]
    with open(file_path, 'a') as f:
        if turn is not None:
            f.write(f'turn {turn} - prompt_{"A" if turn % 2 == 1 else "B"}\n\n')
        if start_time is not None:
            finish_time = time.time()
            f.write(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}\n")
            f.write(f"Finished at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(finish_time))}\n")
            f.write(f'Time taken: {finish_time - start_time} seconds\n\n')
        else:
            f.write(f"Finished at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\n\n")
        if prompt_token_count > 0 and completion_token_count > 0:
            f.write(f'Prompt tokens: {prompt_token_count}\nCompletion tokens: {completion_token_count}\nTotal tokens: {prompt_token_count + completion_token_count}\n\n')
        if total_prompt_token_count > prompt_token_count and total_completion_token_count > completion_token_count:
            f.write(f'Total prompt tokens: {total_prompt_token_count}\nTotal completion tokens: {total_completion_token_count}\nTotal tokens: {total_prompt_token_count + total_completion_token_count}\n\n')
        f.write(f'model:\n{model}\n\n')
        f.write(f'temperature:\n{temperature}\n\n')
        if seed is not None:
            f.write(f'seed:\n{seed}\n\n')
        if fingerprint is not None:
            f.write(f'fingerprint:\n{fingerprint}\n\n')
        for index, entry in enumerate(entries_to_log):
            f.write(f'entry {index + 1} of {len(entries_to_log)}\n')
            f.write(f'{entry["role"]}:\n')
            f.write(f'{entry["content"]}\n\n')
        f.write('-'*100 + '\n'*11)





def run_prompt(
        prompt,
        message_history=None,
        system_message=None,
        log_files=None,
        max_tokens=None,
        temperature=0,
        stream=None,
        seed=None,
        turn=None,
        return_output=False,
        **kwargs
        ):
    start_time = time.time()
    print(f'Start time: {time.strftime("%H:%M:%S", time.localtime(start_time))}\n')

    model = 'gpt-4-1106-preview'
    max_tokens = max_tokens if max_tokens is not None else 4000
    stream = stream if stream is not None else False
    temperature = temperature if temperature is not None else 0
    if model.startswith('gpt-4-1106'):
        seed = 1 if seed is None else seed
    else:
        seed = None

    chat = ChatSession(
        message_history=message_history,
        print_enabled=True,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=stream,
        seed=seed,
        include_response_object=True)
    response_message, response_object = chat.send_message(prompt)

    if stream:
        prompt_token_count = 0
        for message in message_history[:-1]:
            prompt_token_count += get_tokens(message['content'])
        completion_token_count = get_tokens(response_message)
    else:
        prompt_token_count = response_object.usage.prompt_tokens
        completion_token_count = response_object.usage.completion_tokens
    
    total_prompt_token_count = kwargs.get('previous_prompt_token_count', 0) + prompt_token_count
    total_completion_token_count = kwargs.get('previous_completion_token_count', 0) + completion_token_count

    if kwargs.get('fingerprint', False):
        fingerprint = response_object.system_fingerprint
    else:
        fingerprint = None

    for log_file in log_files:
        log_message_to_file(
            entries_to_log=message_history,
            system_message=system_message,
            model=model,
            temperature=temperature,
            file_path=log_file,
            turn=turn,
            prompt_token_count=prompt_token_count,
            completion_token_count=completion_token_count,
            total_prompt_token_count=total_prompt_token_count,
            total_completion_token_count=total_completion_token_count,
            start_time=start_time,
            seed=seed,
            fingerprint=fingerprint,
            )    

    print(f'\nStart time: {time.strftime("%H:%M:%S", time.localtime(start_time))}')
    print(f'End time: {time.strftime("%H:%M:%S", time.localtime(time.time()))}')
    print(f'Prompt_A took {time.time() - start_time} seconds')
    print(f'Prompt tokens: {prompt_token_count}')
    print(f'Completion tokens: {completion_token_count}')
    print(f'Combined tokens: {prompt_token_count + completion_token_count}\n')

    if return_output:
        return response_message, response_object





def run_prompt_A(prompt, puzzle_input, **kwargs):    
    system_message_prompt_A = get_text_from_file('Prompts/system message - Prompt_A - version 3.txt')

    if kwargs.get('test', False):
        prompt = "Testing!"
        puzzle_input = "Testing!"
        system_message_prompt_A = "Give 5 different words each time"
        kwargs['max_tokens'] = 1

    if kwargs.get('message_history', False):
        message_history = kwargs['message_history']
    else:
        message_history = [
                {"role": "system", "content": system_message_prompt_A},
                {"role": "user", "content": puzzle_input},
                {"role": "assistant", "content": "Awaiting instructions."},
            ]

    log_files = ['Logs/message logs.txt', 'Logs/message log - prompt_A.txt']
    log_files = kwargs.get('log_files', log_files)

    response_message, response_object = run_prompt(
        prompt=prompt,
        message_history=message_history,
        system_message=system_message_prompt_A,
        log_files=log_files,
        temperature=kwargs.get('temperature', 0),
        max_tokens=kwargs.get('max_tokens', 4000),
        stream=kwargs.get('stream', True),
        seed=kwargs.get('seed', 1),
        return_output=True,
        previous_prompt_token_count=kwargs.get('previous_prompt_token_count', 0),
        previous_completion_token_count=kwargs.get('previous_completion_token_count', 0),
        turn=kwargs.get('turn', None),
        fingerprint=kwargs.get('fingerprint', None),
        )

    if kwargs.get('return_message_history', False):
        return response_message, response_object, message_history

    if kwargs.get('return_output', False):
        return response_message, response_object





def run_prompt_B(prompt, puzzle_input, previous_results, **kwargs):
    system_message_prompt_B = """Follow ALL instructions METHODICALLY and IN FULL. Your task is to calculate the possible candidate elements for the given cells using the given information, then to update the non-rejected cells of the given sudoku using the calculated candidate elements, then to shift the rows, and finally to output the updated and shifted sudoku. Once you begin you must complete ALL of these tasks BEFORE stopping. After receiving the full instructions you have ONLY one message to finish the task, as soon as you stop responding the final section of your response is sent to the next part of the process. Thus the final text you write MUST be the updated and shifted Sudoku, in the correct format, after ALL other sections have been completed. Do not use spaces in lists, only use commas without spaces to separate elements. Begin as soon as you receive the full instruction set."""
    prompt_B_pre_message = """Respond to this message with "Awaiting instructions." and nothing else. When you receive the current sudoku in <output> tags, say only "Awaiting instructions." and nothing else. You will then receive the last few hundred characters of the previous analysis results. When you receive the previous results say "Awaiting instructions." and nothing else. You will then receive instructions. When you receive the instructions, you may begin."""

    if kwargs.get('message_history', False):
        message_history = kwargs['message_history']
    else:
        message_history = [
            {"role": "system", "content": system_message_prompt_B},
            {"role": "user", "content": prompt_B_pre_message},
            {"role": "assistant", "content": "Awaiting instructions."},
            {"role": "user", "content": puzzle_input},
            {"role": "assistant", "content": "Awaiting instructions."},
            {"role": "user", "content": previous_results},
            {"role": "assistant", "content": "Awaiting instructions."},
        ]

    log_files = ['Logs/message logs.txt', 'Logs/message logs - Prompt_B.txt']
    log_files = kwargs.get('log_files', log_files)

    response_message, response_object = run_prompt(
        prompt=prompt,
        message_history=message_history,
        system_message=system_message_prompt_B,
        log_files=log_files,
        max_tokens=kwargs.get('max_tokens', 4000),
        temperature=kwargs.get('temperature', 0),
        stream=kwargs.get('stream', True),
        seed=kwargs.get('seed', 1),
        return_output=True,
        previous_prompt_token_count=kwargs.get('previous_prompt_token_count', 0),
        previous_completion_token_count=kwargs.get('previous_completion_token_count', 0),
        turn=kwargs.get('turn', None),
        fingerprint=kwargs.get('fingerprint', None),
        )

    if kwargs.get('return_message_history', False):
        return response_message, response_object, message_history

    if kwargs.get('return_output', False):
        return response_message, response_object






def make_folder_structure(folder, puzzle):
    os.makedirs(folder, exist_ok=True)
    os.makedirs(folder + 'logs by turn/', exist_ok=True)
    if not os.path.exists(folder + 'initial puzzle.txt'):
        append_to_text_file(folder + 'initial puzzle.txt', '<output>\n' + str(st.get_input_str_with_names_from_flat_string(puzzle)) + '\n</output>')
    if not os.path.exists(folder + 'turns_taken.txt'):
        append_to_text_file(folder + 'turns_taken.txt', '0')



def full_attempt_prompt_A(folder, puzzle_date, **kwargs):
    turn = int(get_text_from_file(folder + 'turns_taken.txt')) + 1
    puzzle_input_file = folder + 'initial puzzle.txt' if turn == 1 else folder + 'truncated response_B.txt'
    full_attempt_log_file_with_turns = folder + f'FULL LOG with turns - {puzzle_date} puzzle - prompt version 3.txt'
    turn_log_file = folder + 'logs by turn/' + f'turn {turn} - prompt_A - log.txt'
    responses = []
    log_files = [
        'Logs/message logs.txt',
        'Logs/message log - prompt_A.txt',
        full_attempt_log_file_with_turns,
        turn_log_file,
        ]

    seed = 2
    max_tokens = 4000
    prompt_file = "Prompts/Prompt_A - version 3.txt"
    prompt = get_text_from_file(prompt_file)
    puzzle_input = get_text_from_file(puzzle_input_file)

    total_prompt_tokens = 0
    total_completion_tokens = 0

    prompt_A_parameters = {
        'prompt': prompt,
        'puzzle_input': puzzle_input,
        'return_message_history': True,
        'stream': True,
        'seed': seed,
        'max_tokens': max_tokens,
        'previous_prompt_token_count': total_prompt_tokens,
        'previous_completion_token_count': total_completion_tokens,
        'turn': turn,
        'log_files': log_files,
        'fingerprint': True,
    }

    if kwargs.get('test', False):
        prompt_A_parameters['test'] = True

    try:
        response_message, response_object, message_history = run_prompt_A(**prompt_A_parameters)
    except:
        print("Encountered API error, trying again in 60 seconds, please wait...")
        time.sleep(60)
        response_message, response_object, message_history = run_prompt_A(**prompt_A_parameters)
    
    for message in message_history[:-1]:
        total_prompt_tokens += get_tokens(message['content'])
    total_completion_tokens += get_tokens(response_message)
    prompt_A_parameters['previous_prompt_token_count'] = total_prompt_tokens
    prompt_A_parameters['previous_completion_token_count'] = total_completion_tokens
    responses.append(response_message)

    prompt_A_parameters['prompt'] = "continue"
    prompt_A_parameters['message_history'] = message_history
    for repeats in range(2):
        if response_object.choices[0].finish_reason == 'length':
            message_history_backup = message_history.copy()
            encountered_error = False
            
            if kwargs.get('pause', False):
                time.sleep(60)
                input("Press Enter to continue...")

            try:
                response_message, response_object, message_history = run_prompt_A(**prompt_A_parameters)
            except:
                print("Encountered API error, trying again in 60 seconds, please wait...")
                time.sleep(60)
                message_history = message_history_backup.copy()
                response_message, response_object, message_history = run_prompt_A(**prompt_A_parameters)
            
            for message in message_history[:-1]:
                total_prompt_tokens += get_tokens(message['content'])
            total_completion_tokens += get_tokens(response_message)
            prompt_A_parameters['previous_prompt_token_count'] = total_prompt_tokens
            prompt_A_parameters['previous_completion_token_count'] = total_completion_tokens
            responses.append(response_message)

    print(f"\nTotal prompt tokens: {total_prompt_tokens}")
    print(f"Total completion tokens: {total_completion_tokens}\n")

    if kwargs.get('test', False):
        return
    
    tokenized_responses = [get_tokens_from_string(response) for response in responses]
    concatenated_tokenized_responses = []
    for tokenized_response in tokenized_responses:
        concatenated_tokenized_responses.extend(tokenized_response)
    prompt_A_last_tokens = concatenated_tokenized_responses[-400:]

    overwrite_text_file(folder + 'truncated response_A.txt', get_string_from_tokens(prompt_A_last_tokens))
    if turn == 1:
        append_to_text_file(folder + 'sudoku state output - log.txt', 'turn: 0 (initial input)\n\n' + get_text_from_file(puzzle_input_file) + '\n\n\n\n')
    overwrite_text_file(folder + 'turns_taken.txt', str(turn))
    time.sleep(1)





def full_attempt_prompt_B(folder, puzzle_date, **kwargs):
    turn = int(get_text_from_file(folder + 'turns_taken.txt')) + 1
    puzzle_input_file = folder + 'initial puzzle.txt' if turn == 2 else folder + 'truncated response_B.txt'
    previous_results_file = folder + 'truncated response_A.txt'
    full_attempt_log_file_with_turns = folder + f'FULL LOG with turns - {puzzle_date} puzzle - prompt version 3.txt'
    turn_log_file = folder + 'logs by turn/' + f'turn {turn} - prompt_B - log.txt'
    responses = []
    log_files = [
        'Logs/message logs.txt',
        'Logs/message logs - Prompt_B.txt',
        full_attempt_log_file_with_turns,
        turn_log_file,
        ]
    
    seed = 2
    max_tokens = 4000
    prompt_file = "Prompts/Prompt_B - version 3.txt"
    prompt = get_text_from_file(prompt_file)
    puzzle_input = get_text_from_file(puzzle_input_file)
    previous_results = get_text_from_file(previous_results_file)

    total_prompt_tokens = 0
    total_completion_tokens = 0

    prompt_B_parameters = {
        'prompt': prompt,
        'puzzle_input': puzzle_input,
        'previous_results': previous_results,
        'return_message_history': True,
        'stream': True,
        'seed': seed,
        'max_tokens': max_tokens,
        'previous_prompt_token_count': total_prompt_tokens,
        'previous_completion_token_count': total_completion_tokens,
        'turn': turn,
        'log_files': log_files,
        'fingerprint': True,
    }
    
    try:
        response_message, response_object, message_history = run_prompt_B(**prompt_B_parameters)
    except:
        print("Encountered API error, trying again in 60 seconds, please wait...")
        time.sleep(60)
        response_message, response_object, message_history = run_prompt_B(**prompt_B_parameters)
    for message in message_history[:-1]:
        total_prompt_tokens += get_tokens(message['content'])
    total_completion_tokens += get_tokens(response_message)
    prompt_B_parameters['previous_prompt_token_count'] = total_prompt_tokens
    prompt_B_parameters['previous_completion_token_count'] = total_completion_tokens
    responses.append(response_message)

    prompt_B_parameters['prompt'] = "continue"
    prompt_B_parameters['message_history'] = message_history
    for repeats in range(2):
        if response_object.choices[0].finish_reason == 'length':
            message_history_backup = message_history.copy()

            if kwargs.get('pause', False):
                time.sleep(2)
                input("Press Enter to continue...")
            
            try:
                response_message, response_object, message_history = run_prompt_B(**prompt_B_parameters)
            except:
                print("Encountered API error, trying again in 60 seconds, please wait...")
                time.sleep(60)
                message_history = message_history_backup.copy()
                response_message, response_object, message_history = run_prompt_B(**prompt_B_parameters)
            
            for message in message_history[:-1]:
                total_prompt_tokens += get_tokens(message['content'])
            total_completion_tokens += get_tokens(response_message)
            prompt_B_parameters['previous_prompt_token_count'] = total_prompt_tokens
            prompt_B_parameters['previous_completion_token_count'] = total_completion_tokens
            responses.append(response_message)

    print(f"Total prompt tokens: {total_prompt_tokens}")
    print(f"Total completion tokens: {total_completion_tokens}\n")

    tokenized_responses = [get_tokens_from_string(response) for response in responses]
    concatenated_tokenized_responses = []
    for tokenized_response in tokenized_responses:
        concatenated_tokenized_responses.extend(tokenized_response)
    prompt_B_last_tokens = concatenated_tokenized_responses[-204:]

    overwrite_text_file(folder + 'truncated response_B.txt', get_string_from_tokens(prompt_B_last_tokens))
    append_to_text_file(folder + 'sudoku state output - log.txt', f'turn: {"0 (initial input)" if turn == 1 else str(turn)}\n\n' + get_text_from_file(puzzle_input_file) + '\n\n\n\n')
    overwrite_text_file(folder + 'turns_taken.txt', str(turn))
    time.sleep(1)




def solvable_with_version_3(puzzle_str_list):
    row_list, turn, reason, reason_code = st.simulate_run(
        st.string_to_list(puzzle_str_list),
        print_enabled=False,
        max_turns=46, # Since the puzzle will inevitably take an extra few turns, there's no sense wasting a run on a 48 turn puzzle only to be short a turn.
        max_cells_checked_per_turn=20,
        max_cells_updated_per_turn=6,
    )
    if reason_code == 1:
        return True
    return False





def check_sudoku(solution_strings, folder=None):
    if folder == None:
        exit()
    if os.path.exists(folder + 'truncated response_B.txt'):
        puzzle_path = folder + 'truncated response_B.txt'
    elif os.path.exists(folder + 'initial puzzle.txt'):
        puzzle_path = folder + 'initial puzzle.txt'
    else:
        return
    current_puzzle_string = st.extract_numbers_from_string(get_text_from_file(puzzle_path))
    if (current_puzzle_string == solution_strings[0] or current_puzzle_string == solution_strings[1] or current_puzzle_string == solution_strings[2]) and current_puzzle_string.count('0') == 0 and solution_strings[0].count('0') == 0 and solution_strings[1].count('0') == 0 and solution_strings[2].count('0') == 0:
        print("\nSudoku solved!")
        print(current_puzzle_string)
        if current_puzzle_string == solution_strings[0]:
            print(solution_strings[0])
        elif current_puzzle_string == solution_strings[1]:
            print(solution_strings[1])
        elif current_puzzle_string == solution_strings[2]:
            print(solution_strings[2])
        else:
            raise ValueError('Uhh... actually maybe check the solution manually, something went wrong here.')
        print()
        exit()
    valid = st.valid_sudoku_so_far(current_puzzle_string, solution_strings[0]) or st.valid_sudoku_so_far(current_puzzle_string, solution_strings[1]) or st.valid_sudoku_so_far(current_puzzle_string, solution_strings[2])
    if not valid:
        print("Invalid sudoku")
        print(current_puzzle_string)
        print(solution_strings[0])
        print(solution_strings[1])
        print(solution_strings[2])
        exit()





folder = 'Transcripts/November 11th - version 3/'
puzzle = st.latimes_november[10]
make_folder_structure(folder, puzzle)
puzzle_date = 'November 11th'

initial_puzzle_string = st.extract_numbers_from_string(get_text_from_file(folder + 'initial puzzle.txt'))

if not solvable_with_version_3(initial_puzzle_string):
    print("\nPuzzle not solvable with version 3 prompt\n")
    exit()

row_list, turns_taken_to_solve, ending_state, ending_state_code = st.simulate_run(
    st.string_to_list(initial_puzzle_string),
    print_enabled=False,
    max_turns=243,
    max_cells_checked_per_turn=27,
    max_cells_updated_per_turn=27,
    )
solution_string = st.extract_numbers_from_string(str(row_list))
solution_strings = [solution_string, solution_string[27:] + solution_string[:27], solution_string[54:] + solution_string[:54]]
check_sudoku(solution_strings, folder)

input("Press Enter to run ChatGPT on the Sudoku...")
for i in range(3):
    full_attempt_prompt_A(folder, puzzle_date, pause=False)
    full_attempt_prompt_B(folder, puzzle_date, pause=False)
    check_sudoku(solution_strings, folder)

