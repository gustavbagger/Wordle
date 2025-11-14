import sys
import os
import random
import math
import json

'''
1) run this file
2) start the game with 'wordle()'
3) use this filepath when prompted:
./valid_wordle_words.txt
4) type in the game key when prompted
'''

def RemoveNames(filepath: str):
    file = open(filepath,"r")
    file_string = file.read()
    words = file_string.split("\n")
    culled_words = list()
    for word in words:
        if word != "" and not word[0].isupper():
            culled_words.append(word)
    
    output_file = open(filepath[:-4]+"_culled.txt","w")
    output_file.write("\n".join(culled_words))

class Trie:
    def exists(self, word: str):
        current = self.root
        for letter in word:
            if letter not in current:
                return False
            current = current[letter]
        return self.end_symbol in current

    def add(self, word: str):
        current = self.root
        for letter in word:
            if letter not in current:
                current[letter] = {}
            current = current[letter]
        current[self.end_symbol] = True
        self.size += 1
        self.data.append(word)

    def add_list(self, wordlist: list):
        for word in wordlist:
            self.add(word)

    def add_dict(self, filepath: str):
        words_file = open(filepath,"r")
        words_list = (words_file.read()).split("\n")
        self.add_list(words_list)

    def __init__(self):
        self.root = {}
        self.end_symbol = "*"
        self.size = 0
        self.data = list()
    
    def __repr__(self):
        return json.dumps(self.root, sort_keys = True,indent = 2)

def hints(guess: str, solution: str) -> list[int]:
    wordlength = len(guess)
    hint_list = list()
    for i in range(wordlength):
        if guess[i] == solution[i]:
            hint_list.append(2)
    
        elif guess[i] in solution:
            hint_list.append(1)
        else:
            hint_list.append(0)
        
    return hint_list

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



def wordle():
    print("\n======================================================================")
    print("Welcome to Wordle")
    print("======================================================================")

    #Setup phase
    if len(sys.argv)==2:
        current_dict = sys.argv[1]
    else:
        current_dict = input("\nWhat dictionary shall I use? (filepath)\n")
        
    while True:
        print(f"\nYou have imported the dictionary '{current_dict}'.")
        mode_correct = input("Is this the mode you want? (y/n)\n")
        if mode_correct == "y":
            if os.path.isfile(current_dict):
                break
            else:
                print("\nThis is not a valid filepath.")
                mode_correct = "n"
                
        if mode_correct == "n":
            current_dict = input("\nWhat dictionary shall I use instead? (filepath)\n")
            continue

        print("\nPlease respond with 'y' for yes or 'n' for no.")

    words_trie = Trie()
    words_trie.add_dict(current_dict)

    while True:
        keyQ = input("\nDo you have a game key? (y/n)\n")
        if keyQ == "y":
            key = int(input("\nPlease type in your key: \n"))
            solution = game_key(words_trie,key)[0]
            break
        if keyQ == "n":
            solution,key = game_key(words_trie)
            break

        print("\nPlease respond with 'y' for yes or 'n' for no.")


    print("\n======================================================================")
    print(f"Setup complete, your key is {key}")
    print("======================================================================")

    unused_letters = list(map(chr, range(97, 123)))
    correct_letters = list()
    guesses = list()
    solution_check = [2]*len(solution)

    #Game loop
    while True:
        print("----------------------------------------------------------------------")
        print("Remaining letters:\n ")
        print(f"Unused  - {" ".join(unused_letters)}")
        print(f"Correct - {" ".join(correct_letters)}\n")
        print("Gamestate:\n")
        for guess in guesses:
            print(f"{" ".join(list(guess[0]))}")
            print(f"{" ".join(map(str,guess[1]))}")  
        print("----------------------------------------------------------------------")
        guess_word = input("what word would you like to try?\n")

        if guess_word == "End":
            wonQ = False
            break
            
        if not words_trie.exists(guess_word):
            print("\nInvalid word\n")
            continue

        guess_hints = hints(guess_word,solution)
        if guess_hints == solution_check:
            wonQ = True
            break

        guesses.append((guess_word,guess_hints))

        for i in range(len(guess_word)):
            letter = guess_word[i]
            if letter in unused_letters:
                unused_letters.remove(letter)
            if guess_hints[i]>0 and letter not in correct_letters:
                correct_letters.append(letter)
    if wonQ:
        print("\n======================================================================")
        print(f"Correct! The solution was indeed {solution}")
        print(f"If you want to challange someone, send them this key: {key}")
        print("======================================================================")
    else:
        print("\n======================================================================")

        if input("Do you want the solution? (y/n)\n") == "y":
            print(f"The solution was '{solution}'")
            print(f"If you want to challange someone, send them this key: {key}")
        else:
            print(f"If you want to challange someone or try again, use key: {key}")
        print("======================================================================")


wordle()