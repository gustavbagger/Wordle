import nltk
from nltk.corpus import words

# Download the word list if not already present
nltk.download('words')

# Filter for 6-letter words
five_letter_words = [word for word in words.words() if len(word) == 5]

# Save to a .txt file
with open("five_letter_words.txt", "w") as file:
    for word in five_letter_words:
        file.write(word + "\n")

print(f"Saved {len(five_letter_words)} words to five_letter_words.txt")