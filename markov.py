import random
import string
import re
import sys
import pickle

class markov:
	def __init__(self, seedlengths):
		self.chain = {}
		self.terminals = []
		self.begin = []
		self.terminals.append('')
		self.seedlength = seedlengths

	def insert(self, word, next, terminal, start):
		if word not in self.chain:
			if terminal:
				self.terminals.append(next)
			if start:
				self.begin.append(word)
			self.chain[word] = []
			self.chain[word].append([1.0, next])
			return
		else:
			for x in self.chain[word]:
				if next in x:
					x[0] = x[0] + 1.0
					return
			self.chain[word].append([1.0, next])
			return

	def isterminal(self, word):
		if not word:
			return 1
		if word in self.terminals:
			return 1
		else:
			return 0

	def normalize(self):
		for x in self.chain:
			accumulator = 0.0
			for n in self.chain[x]:
				accumulator = accumulator + n[0]
			for n in self.chain[x]:
				n[0] = n[0] / accumulator
			self.chain[x].sort(key = lambda n : n[0])
		return

	def getnext(self, word):
		chance = random.uniform(0.0, 1.0)

		if word in self.chain:
			length = len(self.chain[word])
			i = 0
			while i < length:
				if i == (length - 1):
					return self.chain[word][i][1]
				if chance <= self.chain[word][i][0]:
					x = 0
					tempchance = self.chain[word][i][0]
					while i + x < length and self.chain[word][i + x][0] == tempchance:
						x += 1
					x = x - 1
					index = random.randint(0, x)
					return self.chain[word][i + x][1]

				i = i + 1
		else:
			wordlist = word.split(" ")
			if wordlist[-1] not in self.chain:
				return ''
			else:
				self.getnext(wordlist[-1])

	def learn(self, filename):
		file = open(filename, 'r')	
		istring = file.read()
		istring = istring.lower()
		regex = re.compile('((\n)(\n)*)|(\")')
		istring = regex.sub(' ', istring)
		strings = re.split(';|!|\.|\?', istring)
		wordlists = [[]]
		i = 0
		for n in strings:
			wordlists.append(n.split(" "))
			wordlists[i] = [x for x in wordlists[i] if x != '']
			i = i + 1

		wordlists = [x for x in wordlists if x]

		for n in wordlists:
			i = 0
			length = len(n)
			while i + self.seedlength < length:
				if i + self.seedlength == length:
					tempseed = " ".join(n[i:i + (self.seedlength)])
					self.insert(tempseed, n[i + self.seedlength] , 1, 0)
				elif i == 0:
					tempseed = " ".join(n[i:i + (self.seedlength)])
					self.insert(tempseed, n[i + self.seedlength] , 0, 1)	
				else:
					tempseed = " ".join(n[i:i + (self.seedlength)])
					self.insert(tempseed, n[i + self.seedlength] , 0, 0)				
				i = i + 1
		seedlength = 1
		for n in wordlists:
			i = 0
			length = len(n)
			while i + seedlength < length:
				if i + seedlength == length:
					tempseed = " ".join(n[i:i + (seedlength)])
					self.insert(tempseed, n[i + seedlength] , 1, 0)
				elif i == 0:
					tempseed = " ".join(n[i:i + (seedlength)])
					self.insert(tempseed, n[i + seedlength] , 0, 1)	
				else:
					tempseed = " ".join(n[i:i + (seedlength)])
					self.insert(tempseed, n[i + seedlength] , 0, 0)				
				i = i + 1		
		self.normalize()

def main(argv):
	markovchain = markov(3)
	markovchain.learn(argv[1])
	generated = []
	seed = ""
	output = ""
	while len(output) < 50 or len(output) > 140:
		seedlist = []
		while len(seedlist) < 3:
			beginsize = len(markovchain.begin) - 1
			randindex = random.randint(0, beginsize)
			seed = markovchain.begin[randindex]
			seedlist = seed.split(" ")

		for n in seedlist:
			generated.append(n)

		ended = 0

		while not ended:
			result = markovchain.getnext(seed)
			ended = markovchain.isterminal(result)
			if not ended:
				generated.append(result)
				seed = " ".join(generated[-3:-1])

		print(generated)
		output = " ".join(generated)

	print(output)

main(sys.argv)