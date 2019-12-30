from auto_complete import AutoCompleter, iamdictionary



print("A continuación escribe algo, lo que se te ocurra")

userInput = AutoCompleter(dictionary=iamdictionary())()

print("Final sentence:", userInput)


