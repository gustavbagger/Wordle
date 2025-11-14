from helpers.RemoveNames import RemoveNames

from helpers.prefix_tree import Trie

test_tree = Trie()
test_tree.add_dict("./dictionaries/five_letter_words_culled.txt")

print(test_tree.exists("quota"))

print(test_tree)