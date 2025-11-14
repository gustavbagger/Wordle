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