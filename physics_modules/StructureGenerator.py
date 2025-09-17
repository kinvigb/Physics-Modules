import random
import numpy as np

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
        
def rand(length):
    length = int(round((1 / np.sqrt(5)) * (((1 + np.sqrt(5)) / 2) ** (length + 1) - ((1 - np.sqrt(5)) / 2) ** (length + 1))))
    structure = [random.choice(['A', 'B']) for _ in range(length)]
    structure = [''.join(structure)]
    return structure

def rand_L(length):
    structure = [random.choice(['A', 'B']) for _ in range(length)]
    structure = [''.join(structure)]
    return structure
    
    
def cst(length):
    length = int(round((1 / np.sqrt(5)) * (((1 + np.sqrt(5)) / 2) ** (length + 1) - ((1 - np.sqrt(5)) / 2) ** (length + 1))))
    structure = ['A' * length]
    return structure
    
def periodic(length):
    length = int(round((1 / np.sqrt(5)) * (((1 + np.sqrt(5)) / 2) ** (length + 1) - ((1 - np.sqrt(5)) / 2) ** (length + 1))))
    structure = ['AB' * (length//2)] if length % 2 == 0 else ['AB' * (length//2) + 'A']
    return structure


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

    indices_a = [i for i, x in enumerate(input_chars) if x == 'A']
    indices_b = [i for i, x in enumerate(input_chars) if x == 'B']

    for _ in range(swap_count):
        if not indices_a or not indices_b:  # Check if either list is empty
            break
        if random.choice([True, False]):
            index_to_swap = random.choice(indices_a)
            input_chars[index_to_swap] = 'C'
            indices_a.remove(index_to_swap)
            indices_b.append(index_to_swap)
        else:
            index_to_swap = random.choice(indices_b)
            input_chars[index_to_swap] = 'C'
            indices_b.remove(index_to_swap)
            indices_a.append(index_to_swap)

    return [''.join(input_chars)]

def phason_flip(input_list, sym_pres, flip_count, is_looped=False):
    """
    Performs conditional swaps of 'A's and 'B's, with optional circular logic.

    Args:
        input_list (list): A list containing a single string of 'A's and 'B's.
                           e.g., ['AABABA']
        sym_pres (bool): A flag to control the swapping logic.
                         - True: Swaps only if it DOES NOT create "AAA" or "BB".
                         - False: Swaps only if it DOES create "AAA" or "BB".
        flip_count (int): The desired number of swaps to perform.
        is_looped (bool): If True, treats the string as a circular structure
                          where the last character is adjacent to the first.
                          Defaults to False.

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

    for _ in range(flip_count):
        chars = list(current_string)
        
        # --- Step 1: Find all possible swaps (now includes looped case) ---
        potential_swap_indices = []
        for i in range(n - 1):
            if chars[i] != chars[i+1]:
                potential_swap_indices.append(i)
        
        # NEW: If looped, check for a swap between the last and first characters.
        if is_looped and n > 1 and chars[n-1] != chars[0]:
            # Use n-1 as a special index for the wrap-around swap.
            potential_swap_indices.append(n-1)

        if not potential_swap_indices:
            break

        # --- Step 2: Filter swaps based on the sym_pres rule ---
        valid_swap_indices = []
        for index in potential_swap_indices:
            temp_chars = chars[:]
            
            # NEW: Handle the wrap-around swap for the temporary string.
            if is_looped and index == n - 1:
                temp_chars[index], temp_chars[0] = temp_chars[0], temp_chars[index]
            else:
                temp_chars[index], temp_chars[index+1] = temp_chars[index+1], temp_chars[index]
            
            temp_string = "".join(temp_chars)

            # Check for the pattern within the string
            has_pattern = "AAA" in temp_string or "BB" in temp_string
            
            # NEW: If looped, check for wrap-around patterns like A...AA or BB...B
            if not has_pattern and is_looped and n >= 3:
                if (temp_string[-1] == temp_string[0] == temp_string[1]) or \
                   (temp_string[-2] == temp_string[-1] == temp_string[0]):
                    has_pattern = True
            
            if sym_pres and not has_pattern:
                valid_swap_indices.append(index)
            elif not sym_pres and has_pattern:
                valid_swap_indices.append(index)

        # --- Step 3: Execute a random valid swap ---
        if valid_swap_indices:
            chosen_index = random.choice(valid_swap_indices)
            
            # NEW: Handle the wrap-around swap execution.
            if is_looped and chosen_index == n - 1:
                chars[chosen_index], chars[0] = chars[0], chars[chosen_index]
            else:
                chars[chosen_index], chars[chosen_index+1] = chars[chosen_index+1], chars[chosen_index]
            
            current_string = "".join(chars)
        else:
            break

    return [current_string]














