import random
import numpy as np

def pl_numbers(n):
    if n <= 0:
        return 1 
    elif n == 1:
        return 1
    else:
        return 2*pl_numbers(n-1) + pl_numbers(n-2)

def fibonacci(n):
    if n <= 0:
        return 1 
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci (n-2)

def qc_gm(length,f0='B'):
    structure = [f0]
    for i in range(length):
        fo = structure[i]
        fn = ''.join(['AB' if ch == 'A' else 'A' for ch in fo])
        structure.append(fn)
    return structure

def qc_sm(length,f0='B'):
    structure = [f0]
    for i in range(length):
        fo = structure[i]
        fn = ''.join(['AAB' if ch == 'A' else 'A' for ch in fo])
        structure.append(fn)
    return structure

def qc_np(length,f0='B'):
    structure = [f0]
    for i in range(length):
        fo = structure[i]
        fn = ''.join(['ABBB' if ch == 'A' else 'A' for ch in fo])
        structure.append(fn)
    return structure
        
def rand(length):
    length = int(round((1 / np.sqrt(5)) * (((1 + np.sqrt(5)) / 2) ** (length + 1) - ((1 - np.sqrt(5)) / 2) ** (length + 1))))
    structure = [random.choice(['A', 'B']) for _ in range(length)]
    structure = [''.join(structure)]
    return structure

def rand_L(length):
    structure = [random.choice(['A', 'B']) for _ in range(length)]
    structure = [''.join(structure)]
    return structure

def block_rand(length, blocks = ['ABA', 'ABAAB']):
    chain = ""
    while len(chain) < length:
        chain += random.choice(blocks)
    return [chain[:length]]
    
def cst(length):
    length = int(round((1 / np.sqrt(5)) * (((1 + np.sqrt(5)) / 2) ** (length + 1) - ((1 - np.sqrt(5)) / 2) ** (length + 1))))
    structure = ['A' * length]
    return structure
    
def periodic(length):
    length = int(round((1 / np.sqrt(5)) * (((1 + np.sqrt(5)) / 2) ** (length + 1) - ((1 - np.sqrt(5)) / 2) ** (length + 1))))
    structure = ['AB' * (length//2)] if length % 2 == 0 else ['AB' * (length//2) + 'A']
    return structure

def block_periodic(length, block):
    block_length = len(block)
    int_multiplier = int(np.ceil(length/block_length))
    structure = [block * int_multiplier]
    return structure[:length]

def random_swap(input_list, swap_count):
    if swap_count == 0:
        return input_list

    input_string = input_list[0]
    input_chars = list(input_string)

    indices_a = [i for i, x in enumerate(input_chars) if x == 'A']
    indices_b = [i for i, x in enumerate(input_chars) if x == 'B']

    for _ in range(swap_count):
        if not indices_a or not indices_b:  # Check if either list is empty
            break
        if random.choice([True, False]):
            index_to_swap = random.choice(indices_a)
            input_chars[index_to_swap] = 'B'
            indices_a.remove(index_to_swap)
            indices_b.append(index_to_swap)
        else:
            index_to_swap = random.choice(indices_b)
            input_chars[index_to_swap] = 'A'
            indices_b.remove(index_to_swap)
            indices_a.append(index_to_swap)

    return [''.join(input_chars)]

def random_swap_c(input_list, swap_count):
    if swap_count == 0:
        return input_list

    input_string = input_list[0]
    input_chars = list(input_string)
    
    letters = ['A', 'B', 'C']
    
    for _ in range(swap_count):
        idx = random.randrange(len(input_chars))
        new_char = random.choice([c for c in letters if c != input_chars[idx]])
        input_chars[idx] = new_char

    return [''.join(input_chars)]

def phason_flip(input_list, sym_pres, flip_count, is_looped=False, rev_flip=True, DEBUG=False):
    """
    Performs conditional swaps of 'A's and 'B's, with optional circular logic.

    Args:
        input_list (list):  A list containing a single string of 'A's and 'B's.
                             - e.g., ['AABABA']
        sym_pres (bool):    A flag to control the swapping logic.
                             - True: Swaps only if it DOES NOT create "AAA" or "BB".
                             - False: Swaps only if it DOES create "AAA" or "BB".
        flip_count (int):   The desired number of swaps to perform.
        is_looped (bool):   If True, treats the string as a circular structure
                            where the last character is adjacent to the first.
                            Defaults to False.
        rev_flip (bool):    If True allows the flipping functions to effectively 
                            reverse flips when flip_count > 1, when false ensures 
                            each flip is unique.
        DEBUG (bool):       A simple toggle to enable debugging options, by default 
                            false and ideally should not be used when running this 
                            code for its intended purpose.

    Returns:
        list: A list with the new string. Terminates early if no valid
              swaps are found.
    """
    if flip_count == 0:
        return input_list
        
    if not input_list or not input_list[0]:
        print("Warning: Input list is empty or contains an empty string.")
        return []

    current_string = input_list[0]
    n = len(current_string)
    last_chosen_index = []

    for _ in range(flip_count):
        chars = list(current_string)
        
        potential_swap_indices = []
        for i in range(n - 1):
            if chars[i] != chars[i+1]:
                potential_swap_indices.append(i)

        if is_looped and n > 1 and chars[n-1] != chars[0]:
            potential_swap_indices.append(n-1)

        if not potential_swap_indices:
            break
        valid_swap_indices = []
        for index in potential_swap_indices:
            if rev_flip==False and index in last_chosen_index:
                continue
            temp_chars = chars[:]

            if is_looped and index == n - 1:
                temp_chars[index], temp_chars[0] = temp_chars[0], temp_chars[index]
            else:
                temp_chars[index], temp_chars[index+1] = temp_chars[index+1], temp_chars[index]
            
            temp_string = "".join(temp_chars)

            has_pattern = "AAA" in temp_string or "BB" in temp_string
            
            if not has_pattern and is_looped and n >= 3:
                if temp_string[-1] == "B" and temp_string[0] == "B":
                    has_pattern = True
                elif (temp_string[-1] == temp_string[0] == temp_string[1]) or \
                   (temp_string[-2] == temp_string[-1] == temp_string[0]):
                    has_pattern = True
            
            if sym_pres and not has_pattern:
                valid_swap_indices.append(index)
            elif not sym_pres and has_pattern:
                valid_swap_indices.append(index)
        
        if DEBUG==True:
            print(f"Available moves for {current_string}: {valid_swap_indices}")
        
        if valid_swap_indices:
            chosen_index = random.choice(valid_swap_indices)
            last_chosen_index.append(chosen_index)
            
            if is_looped and chosen_index == n - 1:
                chars[chosen_index], chars[0] = chars[0], chars[chosen_index]
            else:
                chars[chosen_index], chars[chosen_index+1] = chars[chosen_index+1], chars[chosen_index]
            
            current_string = "".join(chars)
        else:
            break
    if DEBUG==True:
        return ([current_string], valid_swap_indices, last_chosen_index)
    else:
        return [current_string]














