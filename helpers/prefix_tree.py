import json

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
    
    def __repr__(self):
        return json.dumps(self.root, sort_keys = True,indent = 2)