import sys
import os

from helpers.RemoveNames import RemoveNames

from helpers.prefix_tree import Trie

from helpers.positional_hints import hints

from helpers.generate_instance import simple_encr_decr, game_key

#test with ./dictionaries/valid_wordle_words.txt

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
        for i in range(len(guesses)):
            guess = guesses[i]
            print(f"({i+1}) {" ".join(list(guess[0]))}")
            print(f"    {" ".join(map(str,guess[1]))}")  
        
        if len(guesses) != 0 and guesses[-1][1] == solution_check:
            wonQ = True
            break
        print("----------------------------------------------------------------------")

        guess_word = input("what word would you like to try?\n")

        if guess_word == "End":
            wonQ = False
            break
            
        if not words_trie.exists(guess_word):
            print("\nInvalid word\n")
            continue

        guess_hints = hints(guess_word,solution)

        guesses.append((guess_word,guess_hints))

        for i in range(len(guess_word)):
            letter = guess_word[i]
            if letter in unused_letters:
                unused_letters.remove(letter)
            if guess_hints[i]>0 and letter not in correct_letters:
                correct_letters.append(letter)
    if wonQ:
        print("\n======================================================================")
        print(f"Correct! The solution was indeed '{solution}'")
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