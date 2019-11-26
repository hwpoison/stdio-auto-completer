import msvcrt

__autor__ = 'srbill1996'


def iamdictionary():
    word_list = []
    with open("popular_words.txt", "r", encoding='utf-8') as file:
        for e in file.read().split(' '):
            word_list.append(e)
    print(f"Loaded {len(word_list)} words.")
    return word_list


class AutoCompleter:
    def __init__(self, dictionary):
        self.sentence = ''
        self.word_list = dictionary
        self.clear_screen = False

    def clearScreen(self):
        os_type = os.sys.platform
        if(self.clear_screen):
            os.system('cls' if os_type == 'win32' else 'clear')

    def getInputKey(self):
        input_char = msvcrt.getch()
        return input_char

    def deleteLastWord(self):
        space = self.getLastSpace()
        if not space:
            self.sentence = ''
        else:
            self.sentence = self.sentence[:space+1]

    def getLastSpace(self):
        isspace = self.sentence.rfind(' ')
        if isspace is -1:
            return 0
        else:
            return isspace

    def replaceLastWord(self, newword):
        self.deleteLastWord()
        self.sentence += newword

    def getLastWord(self):
        space = self.getLastSpace()
        if not space:
            return self.sentence
        else:
            return self.sentence[space+1:]

    def addWord(self, newword):
        self.sentence += ' ' + newword

    def addLetter(self, letter):
        self.sentence += letter

    def backSpace(self):
        self.sentence = self.sentence[:-1]

    def decodeChar(self, char):
        encode_table = {
            b'\xa4': 'ñ'
        }  # fixme
        if(char in encode_table):
            return encode_table[char]
        return str(char, 'utf-8', 'ignore')

    def __call__(self):
        word_cache = ''
        auto_complete = True  # enable auto complete
        auto_completed = False  # word complete?
        while True:
            input_char = self.getInputKey()
            last_word = self.getLastWord()
            if input_char == b'\r':
                break
            # elif(input_char == b'\xe0'): # up key
            #	if candidates:
            #		candidates.insert(0, candidates.pop(candidates.index(candidates[-1])))
            #		self.replaceLastWord(candidates[0])
            #		actual_candidate = candidates[0]
            #		alternate_mode = True
            elif(input_char == b'\x08'):  # backspace
                if(word_cache):
                    self.replaceLastWord(word_cache)  # restore previous input
                    word_cache = ''  # clear cache
                    auto_complete, auto_completed = False, False
                else:
                    self.backSpace()
            else:
                if(input_char is b' '):  # space key
                    self.sentence += ' '
                    word_cache = ''
                    auto_complete = True
                else:
                    input_char = self.decodeChar(input_char)
                    if auto_completed:  # discard auto complete candidate
                        self.replaceLastWord(word_cache)
                        auto_complete, auto_completed = True, False
                    self.addLetter(input_char)  # add new letter
                    last_word = self.getLastWord()  # get last word
                    for word in self.word_list:
                        if(word.find(last_word) == 0
                           and len(last_word) > 2
                           and auto_complete):
                            word_cache = last_word  # save previous input
                            self.replaceLastWord(word)
                            auto_completed = True

            self.clearScreen()
            print(self.sentence)

        return self.sentence


getUserInput = AutoCompleter(dictionary=iamdictionary())

completed = getUserInput()

print("Final sentence:", completed)
