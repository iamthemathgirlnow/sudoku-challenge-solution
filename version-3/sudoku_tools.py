from utils import get_text_from_file
import re


def get_text_from_file(file_path):
    with open(file_path, "r") as f:
        text = f.read()
    return text

def string_to_list(puzzle_string):
    return [[int(puzzle_string[i * 9 + j]) for j in range(9)] for i in range(9)]

def list_to_string(puzzle_list):
    return ''.join([str(puzzle_list[i][j]) for i in range(9) for j in range(9)])

def identical_puzzles(puzzle_list_1, puzzle_list_2):
    return list_to_string(puzzle_list_1) == list_to_string(puzzle_list_2)

def list_to_string_list(number_list):
    string_list = []
    for number in number_list:
        string_list.append(str(number))
    string_list = '[' + ','.join(string_list) + ']'
    return string_list


def raw_list_to_list(string_input_sudoku):
    split_list = string_input_sudoku.strip().split('\n')
    if len(split_list) == 11:
        split_list = split_list[1:len(split_list) - 1]
    row_names = []
    rows = []
    for row in split_list:
        row_names.append(row[:row.index(':')])
        rows.append(row[row.index(' ') + 1:])
    
    rows_as_strings = rows.copy()
    rows_as_lists = []
    # convert string of a list to an actual list. For example '[1,2,3,4,5,6,7,8,9]' becomes [1,2,3,4,5,6,7,8,9]
    for row in rows:
        numbers_in_row = row.strip().strip('[]').split(',')
        rows_as_lists.append([int(number) for number in numbers_in_row])

    return row_names, rows_as_lists, rows_as_strings


def display_list(list_to_display):
    for i in range(len(list_to_display)):
        print(list_to_display[i])
    print()

def display_multiple_lists(*args):
    for i in range(len(args)):
        if isinstance(args[i], list):
            display_list(args[i])

def display_full_puzzle_list(puzzle_list):
    print()
    display_list(puzzle_list)
    print()
    display_list(rows_to_columns(puzzle_list))
    print()
    display_list(rows_to_squares(puzzle_list))
    print()


def rows_to_columns(row_list):
    return [[row_list[j][i] for j in range(9)] for i in range(9)]

def rows_to_squares(row_list):
    return [[row_list[3 * (i // 3) + j // 3][3 * (i % 3) + j % 3] for j in range(9)] for i in range(9)]


def candidates_from_group(group):
    all_digits = [1,2,3,4,5,6,7,8,9]
    return [digit for digit in all_digits if digit not in group]

def all_row_candidates(row_list):    
    candidates_list = []
    for i in range(9):
        candidates_list.append(candidates_from_group(row_list[i]))
    return candidates_list

def all_column_candidates(column_list):
    candidates_list = []
    for i in range(9):
        candidates_list.append(candidates_from_group(column_list[i]))
    return candidates_list

def all_square_candidates(square_list):
    candidates_list = []
    for i in range(9):
        candidates_list.append(candidates_from_group(square_list[i]))
    return candidates_list

def all_candidates(row_list):
    return all_row_candidates(row_list), all_column_candidates(rows_to_columns(row_list)), all_square_candidates(rows_to_squares(row_list))


def find_zeros_in_row_list(row_list):
    zero_indices = []
    for i in range(9):
        zero_indices.append([])
        for j in range(9):
            if row_list[i][j] == 0:
                zero_indices[i].append(j)
    return zero_indices


def all_cell_candidates(row_list):
    row_candidates, column_candidates, square_candidates = all_candidates(row_list)
    cell_candidates = []
    for i in range(9):
        cell_candidates.append([])
        for j in range(9):
            if row_list[i][j] == 0:
                cell_candidates[i].append(sorted(list(set(row_candidates[i]) & set(column_candidates[j]) & set(square_candidates[3 * (i // 3) + j // 3]))))
            else:
                cell_candidates[i].append([])
    return cell_candidates


def move_top_row_to_bottom(input_str):
    row_names, row_lists, row_lists_as_strings = raw_list_to_list(input_str)
    # row_names.append(row_names.pop(0))
    row_lists.append(row_lists.pop(0))
    row_lists_as_strings.append(row_lists_as_strings.pop(0))
    # return as input_str
    return '\n'.join([row_names[i] + ': ' + row_lists_as_strings[i] for i in range(len(row_names))]) + '\n'

def move_top_three_rows_to_bottom(input_str):
    rotated_input_str = move_top_row_to_bottom(input_str)
    rotated_input_str = move_top_row_to_bottom(rotated_input_str)
    rotated_input_str = move_top_row_to_bottom(rotated_input_str)
    return rotated_input_str



input_str = """
RowZero: [0,0,0,6,0,0,0,8,1]
RowOne: [2,0,4,9,7,8,6,5,0]
RowTwo: [8,0,0,0,0,1,9,0,2]
RowThree: [5,0,0,0,0,0,0,0,0]
RowFour: [1,0,0,8,6,9,0,0,0]
RowFive: [0,2,8,4,5,0,7,0,9]
RowSix: [0,0,6,7,0,0,2,4,0]
RowSeven: [0,0,0,0,8,0,0,0,6]
RowEight: [0,8,0,2,0,0,0,0,7]
"""

rotated_input_str = move_top_three_rows_to_bottom(input_str)
# print(rotated_input_str)
# print(move_top_three_rows_to_bottom(move_top_three_rows_to_bottom(input_str)))


# # Getting candidates from a standard form input sudoku (RowZero, RowOne, etc.)
# row_list = raw_list_to_list(input_str)[1]
# row_candidates, column_candidates, square_candidates = all_candidates(row_list)
# # Printing the cell candidates for all empty squares in the first three rows
# print()
# print(input_str)
# print()
# print(all_cell_candidates(row_list)[:3][0])
# print(all_cell_candidates(row_list)[:3][1])
# print(all_cell_candidates(row_list)[:3][2])
# print()
# print(all_cell_candidates(row_list)[3:6][0])
# print(all_cell_candidates(row_list)[3:6][1])
# print(all_cell_candidates(row_list)[3:6][2])
# print()
# print(all_cell_candidates(row_list)[6:9][0])
# print(all_cell_candidates(row_list)[6:9][1])
# print(all_cell_candidates(row_list)[6:9][2])
# print()



# Simulating the results of running the current method
def simulate_run(row_list, print_enabled=None, max_turns=None, max_cells_checked_per_turn=None, max_cells_updated_per_turn=None):
    from math import floor
    print_enabled = print_enabled if print_enabled is not None else True
    max_turns = floor(max_turns/2) if max_turns is not None else 25
    max_cells_checked_per_turn = max_cells_checked_per_turn if max_cells_checked_per_turn is not None else 20
    max_cells_updated_per_turn = max_cells_updated_per_turn if max_cells_updated_per_turn is not None else 6

    no_cells_found_count = 0
    if print_enabled:
        print()
    for turn in range(1, max_turns+1):
        zero_indices = find_zeros_in_row_list(row_list)
        capped_zero_count = min(sum([len(zero_indices[i]) for i in range(9)]), max_cells_checked_per_turn)
        if capped_zero_count == 0:
            if print_enabled:
                print(f"Sudoku Solved!")
                print(f"Turn {(turn-1)*2}")
            return row_list, (turn-1)*2, "Solved", 1

        empty_cells_checked = 0
        cells_to_update = []
        for i in range(9):
            for j in range(9):
                if empty_cells_checked >= capped_zero_count:
                    break
                if row_list[i][j] == 0:
                    empty_cells_checked += 1
                if row_list[i][j] == 0 and len(all_cell_candidates(row_list)[i][j]) == 1:
                    cells_to_update.append([i,j,all_cell_candidates(row_list)[i][j][0]])

        if print_enabled:
            print(f"Turn {turn*2}")
            print(cells_to_update)

        cells_to_update = cells_to_update[:max_cells_updated_per_turn]
        for cell in cells_to_update:
            row_list[cell[0]][cell[1]] = cell[2]

        if (len(cells_to_update) > 0):
            if print_enabled:
                display_list(row_list)
        else:
            if print_enabled:
                print("No cells with only one candidate found.\n")
            no_cells_found_count += 1
        
        row_list = row_list[3:] + row_list[:3]

        if no_cells_found_count >= 3:
            if print_enabled:
                print("No cells with only one candidate found for all three turns in one cycle, stopping search.")
            return row_list, turn*2, "No Single Candidate Cells", -1

        if turn % 3 == 0:
            no_cells_found_count = 0
        
        zero_indices = find_zeros_in_row_list(row_list)
        capped_zero_count = min(sum([len(zero_indices[i]) for i in range(9)]), max_cells_checked_per_turn)
        if capped_zero_count == 0:
            if print_enabled:
                print(f"Sudoku Solved!")
                print(f"Turn {turn*2}")
            return row_list, turn*2, "Solved", 1
        
    return row_list, turn*2, "Unsolved: Max Turns Reached", -2







# # Testing raw_list_to_list
# print()
# string_input_sudoku = get_text_from_file('prompt - puzzle input.txt')
# print(string_input_sudoku)
# print()
# row_names, row_list, row_list_strings = raw_list_to_list(string_input_sudoku)
# print(row_names)
# print()
# print(row_list)
# print()
# print(row_list_strings)
# print()



# Testing the basics, also the display functions
ny_times_oct_17 = '075396000000050209968000057430600810600543000009100603007005026096002030500061070'
oct_01_string = '041670258000000003700052600204000080000000064010030020030080490092041000060709005'
oct_03_string = '000394650060000003008150000039007000457002060800900014000000080900061000015280046'
oct_19_string = '702000300640038057050710000076020180814906030030080506000041260108005000000370000'

# row_list = string_to_list(oct_03_string)
# column_list = rows_to_columns(row_list)
# square_list = rows_to_squares(row_list)

# row_candidates, column_candidates, square_candidates = all_candidates(row_list)

# # display_full_puzzle_list(row_list)
# # print('\n')
# # display_multiple_lists_of_lists(row_candidates, column_candidates, square_candidates)
# # print('\n')
# # display_list(find_zeros_in_puzzle_list(row_list))

# display_list(row_list)


latimes_october = [
    "041670258000000003700052600204000080000000064010030020030080490092041000060709005", # October 1, 2023
    "000240000092005300000000081583090720000780500740002000000916003301408065008507000", # October 2, 2023
    "000394650060000003008150000039007000457002060800900014000000080900061000015280046", # October 3, 2023
    "097014002030000900026500080000000030602308100010050047009000001365002490000089020", # October 4, 2023
    "050004000000900370900801000803006100060010827091008600700080903000290004030160500", # October 5, 2023
    "458200090960070030002010605000350971000001860210009003023004000146583020090020004", # October 6, 2023
    "081023006300590807060080002000050001013000700200600900509002030104800560030910004", # October 7, 2023
    "160903400300070000970080350097040028400000000003100674000806502035204790216000000", # October 8, 2023
    "031790008005014090000620105000140000100509204000208006008461000060000901010080047", # October 9, 2023
    "028017904600480000000020610010050070070061490009000003700008240053000000184000065", # October 10, 2023
    "002000347030140506500003008000800000200005009090204065005000801900000700871050694", # October 11, 2023
    "000000300900100056000735090059062040321400500000003000690007001147200030000000089", # October 12, 2023
    "076040008000100900401908076100560000307402069009080100800601400005030680614000390", # October 13, 2023
    "006028000052000610040000000000903580008406090304005000000000073260031840703500020", # October 14, 2023
    "036000902008500410000080600803000107900017304710030000307651040095740200000900706", # October 15, 2023
    "000400010600502000450080690000000082026970000183200900001053400308620050205810706", # October 16, 2023
    "007630210014590000200070900000000170300710009000000603020000005600208090700340800", # October 17, 2023
    "431080600702004300000020010005003900093508007100006500000000006920000005057000100", # October 18, 2023
    "702000300640038057050710000076020180814906030030080506000041260108005000000370000", # October 19, 2023
    "018090050030100640006035008704513900000270010052000034205060001691000000003951006", # October 20, 2023
    "000000083000000000108300470030810900020900068059004007000080006370060024080240030", # October 21, 2023
    "006700240000080006080200007000600081204978650800001902500000000100869000028450709", # October 22, 2023
    "000300079006009100100050006700000030800000905390208000610905040250043001007001020", # October 23, 2023
    "000703068760208054089050000200900640050012007890400205000009000048571026072000080", # October 24, 2023
    "650070004489000637300090500800006720971000300063507000000001473000305906030749008", # October 25, 2023
    "060050000284007300000014208509000700000006103002070000920705000001200580850031000", # October 26, 2023
    "408060500005200006016000302284090000703005100150700064802901050090030040007600020", # October 27, 2023
    "007059108104720000080016005000045020210800050405200906390060700560030800001000560", # October 28, 2023
    "016000530020006098903008000007000000200645087000079004580001300700463800061507020", # October 29, 2023
    "974800005620400030000259000480000090300607040790000003008910070047005600030086014", # October 30, 2023
    "530004100007000023019005084001020078000003950000000231950067800280100600070042000", # October 31, 2023
]

latimes_november = [
    '',
    '',
    '',
    '',
    '',
    '000078001080510004100006358820001609000600800790002140007000400201007500630005920', # November 6, 2023
    '900306400201807960700050083400600300003200070070003049054760200020000004309020008', # November 7, 2023
    '002047906000609300091050700000000100203900060086012430000090250100200000004370000', # November 8, 2023
    '000109080900000051030040096003001007400008605501692008804007130020013864000020000', # November 9, 2023
    '203008045080050021010002600000060019040203000007000482300809000002070050874105000', # November 10, 2023
    '023000000001370096000000700205090670009080314408000500080042060006950082190060407', # November 11, 2023
]

def extract_numbers_from_string(string):
    numbers = []
    for char in string:
        if char.isdigit():
            numbers.append(char)
    return ''.join(numbers)


def valid_sudoku_so_far(string_test, string_solution):
    string_test = extract_numbers_from_string(string_test)
    string_solution = extract_numbers_from_string(string_solution)
    if len(string_test) != 81 or len(string_solution) != 81:
        return False
    for i in range(81):
        if string_test[i] != '0' and string_test[i] != string_solution[i]:
            return False
    return True


# number_to_word = {0: 'Zero', 1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6:'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine'}
# word_to_number = {'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five':5, 'Six': 6, 'Seven': 7, 'Eight': 8}
number_to_word = {0: 'One', 1: 'Two', 2: 'Three', 3: 'Four', 4: 'Five', 5: 'Six', 6:'Seven', 7: 'Eight', 8: 'Nine'}
word_to_number = {'One': 0, 'Two': 1, 'Three': 2, 'Four': 3, 'Five':4, 'Six': 5, 'Seven': 6, 'Eight': 7, 'Nine': 8}

# Outputs the same form as `RowZero: [0,0,0,3,9,4,6,5,0]` for each row
def get_input_str_with_names_from_flat_string(flat_string):
    row_list = string_to_list(flat_string)
    row_names = [f"Row{number_to_word[i]}" for i in range(9)]
    list_of_formatted_row_strings = []
    for i in range(9):
        list_of_formatted_row_strings.append(f"{row_names[i]}: {list_to_string_list(row_list[i])}")
    return '\n'.join(list_of_formatted_row_strings)

# print()
# print(get_input_str_with_name_from_flat_string(latimes_october[21]))
# print()


# # Testing the run method on multiple puzzles
# print()
# puzzles_solved = 0
# max_turns = 46
# max_cells_checked_per_turn = 20
# max_cells_updated_per_turn = 6
# # puzzle_list = latimes_october
# puzzle_list = latimes_november
# month = "November"
# empty_puzzle_strings = 0
# for index, puzzle in enumerate(puzzle_list):
#     if puzzle == '' or len(puzzle) != 81:
#         empty_puzzle_strings += 1
#         continue
#     row_list, turn, reason, reason_code = simulate_run(string_to_list(puzzle), print_enabled=False, max_turns=max_turns, max_cells_checked_per_turn=max_cells_checked_per_turn, max_cells_updated_per_turn=max_cells_updated_per_turn)
#     print(f"{month} {index + 1}")
#     print(f"Turns: {turn if reason_code == 1 else 'Stopped at ' + str(turn)}")
#     print(f"Reason: {reason}\n")
#     if reason_code == 1:
#         puzzles_solved += 1
# print(f"Turns Per Puzzle: {max_turns}")
# print(f"Cells Checked Per Turn: {max_cells_checked_per_turn}")
# print(f"Cells Updated Per Turn: {max_cells_updated_per_turn}")
# print(f"\nPuzzles Solved: {puzzles_solved} out of {len(puzzle_list) - empty_puzzle_strings}")
# print()



# # Testing the run method on a single puzzle with print enabled
# print()
# puzzle_str_list = raw_list_to_list(rotated_input_str)[1]
# 
# print()
# # puzzle = latimes_october[27]
# puzzle = latimes_november[11]
# puzzle_str_list = string_to_list(puzzle)
# # display_list(puzzle_str_list)
# row_list, turn, reason, reason_code = simulate_run(
#     puzzle_str_list,
#     print_enabled=True,
#     max_turns=50,
#     max_cells_checked_per_turn=20,
#     max_cells_updated_per_turn=6,
#     )