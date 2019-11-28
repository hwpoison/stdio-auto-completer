import os

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
		self.min_autocomplete = 2
		self.default_encode = 'utf-8'
		self.word_list = dictionary
		self.clear_screen = False

	def clearScreen(self):
		os_type = os.sys.platform
		if self.clear_screen:
			os.system('cls' if os_type == 'win32' else 'clear')

	def initializeInputMethod(self):
		try:  # for Windows
			import msvcrt
			def _get_key():
				return msvcrt.getwch()
		except ImportError:  # Linux
			import tty
			import sys
			import termios
			def _get_key():
				fd = sys.stdin.fileno()
				old_settings = termios.tcgetattr(fd)
				try:
					tty.setraw(sys.stdin.fileno())
					input_char = sys.stdin.read(1)
				finally:
					termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
				return input_char
		self._get_key = _get_key  # _get_key() for get key

	def deleteLastWord(self):
		space = self.getLastSpace()
		if not space:
			self.sentence = ''
		else:
			self.sentence = self.sentence[:space+1]

	def getLastSpace(self):
		isspace = self.sentence.rfind(' ')
		return isspace if isspace else 0

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

	def toBytes(self, char):
		return bytes(char, encoding=self.default_encode)

	def decodeChar(self, char):
		return char

	def downgradeWord(self, word): # simplify word
		symbols = {
			'í':'i',
			'á':'a',
			'é':'e',
			'ó':'o',
			'ú':'u',
		}
		for s in symbols:
			word = word.replace(s, symbols[s])
		# return word.lower()
		return word

	def findWord(self, word_to_find):
		coincidendeces = []
		word_to_find = self.downgradeWord(word_to_find)
		for word in self.word_list:
			if(self.downgradeWord(word).find(word_to_find) == 0
				and len(word_to_find) > self.min_autocomplete):
					coincidendeces.append(word)
		return coincidendeces

	def __call__(self):
		self.initializeInputMethod()
		word_cache = ''
		auto_complete = True  # enable auto complete
		auto_completed = False  # word complete?
		candidates = []  # similar words candidates
		while True:
			input_char = self._get_key()
			last_word = self.getLastWord()
			if self.toBytes(input_char) == b'\r':
				break
			elif self.toBytes(input_char) == b'\t' and candidates:  # tab key
				if len(candidates) > 1:  # more of 1 sugerences
					candidates.insert(0, candidates.pop(
						candidates.index(candidates[-1])))
					self.replaceLastWord(candidates[1])  # alternate sugerence
			elif self.toBytes(input_char) == b'\x08':  # backspace
				if word_cache:
					self.replaceLastWord(word_cache)  # restore previous input
					word_cache = ''  # clear cache
					auto_complete, auto_completed = False, False
				else:
					self.backSpace()
			else:
				if self.toBytes(input_char) is b' ':  # space key
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
					candidates = self.findWord(last_word)
					if candidates and auto_complete:
						word_cache = last_word  # save previous input
						self.replaceLastWord(candidates[0])
						auto_completed = True
			self.clearScreen()
			print(self.sentence)
		return self.sentence


if __name__ == '__main__':
	getUserInput = AutoCompleter(dictionary=iamdictionary())
	completed = getUserInput()
	print("Final sentence:", completed)
