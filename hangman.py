import random
import string
import math

class Hangman:
    def __init__(self):
        self.dictionary = self.read_words()
        self.possible_words = self.dictionary
        self.possible_letters = [l for l in string.ascii_lowercase]
        self.guesses = 0

    def read_words(self):
        with open('words_alpha.txt', 'r') as f:
            dictionary = f.read().splitlines()
        return dictionary
    
    def bits(self, x):
        return -math.log(x, 2)
    
    def get_expected_info(self, guess, words):
        sum = 0
        for word in words:
            if guess in word:
                sum += 1
        # sum - the number of words with the guess in them
        # Expected information = (P(e in word) * Information gained if e in word) * (P(e in not word) * Information gained if e not in word)
        expected_info = ((sum / len(words)) * self.bits(sum / len(words))) + ((1 - (sum / len(words))) * self.bits(1 - (sum / len(words))))
        return expected_info
    
    def get_all_infos(self, letters, words):
        expected_infos = { letter: self.get_expected_info(letter, self.possible_words) for letter in letters }
        return expected_infos
    
    def guess(self, letter):
        guesses += 1
        self.possible_letters.remove(letter)
        response = input(f'Is {letter} in your word? (y/n)\n')
        if response.lower() == 'y':
            self.possible_letters.remove(letter)

        print(self.possible_letters)


    def game(self, word_length):
        self.possible_words = [word for word in self.dictionary if len(word) == word_length]

        expected_info = self.get_all_infos(self.possible_letters, self.possible_words)
        expected_info = sorted(expected_info.items(), key=lambda x: x[1], reverse=True)
        self.guess(expected_info[0][0])


print('\n' * 20)
game = Hangman()
game.game(5)
