import random
import string
import math

class Hangman:
    def __init__(self):
        self.dictionary = self.read_words()
        self.possible_words = self.dictionary
        self.possible_letters = [l for l in string.ascii_lowercase]
        self.guesses = 0
        self.cur_info = []

    def read_words(self):
        with open('words_alpha.txt', 'r') as f:
            dictionary = f.read().splitlines()
        return dictionary
    
    def bits(self, x):
        return -math.log(x, 2) # if this defaults then there are no words left
    
    def get_expected_info(self, guess, words):
        sum = 0
        for word in words:
            if guess in word:
                sum += 1
        # sum - the number of words with the guess in them
        # Expected information = (P(e in word) * Information gained if e in word) * (P(e in not word) * Information gained if e not in word)
        try:
            expected_info = ((sum / len(words)) * self.bits(sum / len(words))) + ((1 - (sum / len(words))) * self.bits(1 - (sum / len(words))))
        except:
            expected_info = 0 # FIX THIS
        return expected_info
    
    def get_all_infos(self, letters, words):
        expected_infos = { letter: self.get_expected_info(letter, self.possible_words) for letter in letters }
        return expected_infos
    
    def check_match(self, info, word):
        for a, b in zip(info, word):
            if ((b not in info)) and (a == 0) and (b in self.possible_letters):
                continue
            if a != b:
                return False
        return True
    
    def remove_words(self, pattern):
        new_words = []
        for word in self.possible_words:
            if self.check_match(pattern, list(word)):
                new_words.append(word)
        return new_words
    
    def guess(self, letter):
        self.guesses += 1
        self.possible_letters.remove(letter)
        response = input(f'Is {letter} in your word? (y/n)\n').lower()
        if response == 'y':
            spots = input('In which spots? (respond with the index of the each spot seperated by a space)\n')
            spots = spots.split(' ')
            for spot in spots:
                self.cur_info[int(spot) - 1] = letter

        self.possible_words = self.remove_words(self.cur_info)


    def game(self, word_length):
        self.possible_words = [word for word in self.dictionary if len(word) == word_length]
        self.cur_info = [0 for _ in range(word_length)]

        while True:
            expected_info = self.get_all_infos(self.possible_letters, self.possible_words)
            expected_info = sorted(expected_info.items(), key=lambda x: x[1], reverse=True)
            best_guess = expected_info[0][0]
            self.guess(best_guess)
            
            print(f"{' '.join(['_' if letter == 0 else letter for letter in self.cur_info])}  {len(self.possible_words)} possible words\n")

            if len(self.possible_words) == 0:
                print("I don't know that word")
                break
            if 0 not in self.cur_info:
                print(f"Is your word {''.join(self.cur_info)}?")
                break


print('\n' * 20)
game = Hangman()
game.game(7)
