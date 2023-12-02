
def get_prompt_from_file(file_path):
    with open(file_path, 'r') as f:
        prompt = f.read()
    return prompt

def rotate_puzzle(file_path):
    puzzle = get_prompt_from_file('prompt - puzzle input.txt')
    puzzle = puzzle[puzzle.index('first_row'):puzzle.index('</output>') - 1]
    puzzle = puzzle.split('\n')
    puzzle = [row.split(' ') for row in puzzle]

    puzzle_row_names = []
    puzzle_row = []
    for index, row in enumerate(puzzle):
        puzzle_row_names.append(row[0])
        puzzle_row.append(row[1])

    puzzle_row = puzzle_row[3:] + puzzle_row[:3]

    puzzle_output = ''
    for index, row in enumerate(puzzle_row):
        puzzle_output += puzzle_row_names[index] + ' ' + row + '\n'

    return puzzle_output

# print()
# print(get_prompt_from_file('prompt - puzzle input.txt'))
print()
print(rotate_puzzle('prompt - puzzle input.txt'))