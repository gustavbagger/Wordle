import random
import math
from .prefix_tree import Trie

def simple_encr_decr(value: int, max_size:int, encr_decr: bool) -> int:
    shift = math.floor(0.64 * max_size)
    xor = math.floor(0.32 * max_size)

    if encr_decr:
        return (((value + shift) * 13) % max_size )^xor % max_size
    else:
        return ((value^xor)*pow(13,-1,max_size) - shift) %max_size

def game_key(words: Trie, key: int = 0) -> (str,int):
    max_size = words.size
    if key == 0:
        index = random.randint(0,max_size-1)
        new_key = simple_encr_decr(index, max_size, True)
    else:
        index = simple_encr_decr(key, max_size, False)
        new_key = key

    return words.data[index], new_key



