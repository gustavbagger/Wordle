
'''
output in ternary with 
0 = wrong letter
1 = correct letter, wrong spot
2 = correct letter, correct spot
'''

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