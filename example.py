from auto_complete import AutoCompleter, getWordsFile



print("A continuación escribe algo, lo que se te ocurra")

userInput = AutoCompleter(dictionary=getWordsFile('popular_words.txt'))()

print("Final sentence:", userInput)


