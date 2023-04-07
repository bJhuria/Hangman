import random

class Hangman:
    ''' This class manages the internal details of a game of
    Hangman. No user interface is presented or managed by this
    class. '''
    
    def __init__(self, filename, max_wrong):
        ''' Initializes a game by reading a list of potential
        words to guess from the specified file. Sets the
        maximum number of wrong guesses per game. '''
        
        self.word_list = []
                
         # code to read the file
        with open(filename) as file:
#            read line by line
            for line in file:
#         strip new line character from each line
                line = line.strip()
#           insert words from the line into word_list
                [self.word_list.append(word.strip()) for word in line.split()]
        
        
        self.MAX_WRONG_GUESSES = max_wrong
        self.new_game()
        

    def new_game(self):
        ''' Starts a new game by setting the number of wrong
        guesses to 0, randomly choosing a new word to guess,
        and setting the current status of the guessed word to
        the appropriate number of dashes. '''
        
        self.number_wrong_guesses = 0
        self.answer_word = random.choice(self.word_list)
        self.guess_word = '-' * len(self.answer_word)
        

    def process_guess(self, letter):
        ''' Processes the user's guess of the specified letter
        by searching the word for the letter and updating the
        current guess word. Returns True if the guessed letter
        was found anywhere in the answer word. '''
        
        found = False
        current = ''
        for i in range(len(self.answer_word)):
            if self.answer_word[i] == letter:
                current += letter
                found = True
            else:
                current += self.guess_word[i]
        
        self.guess_word = current
        if not found:
            self.number_wrong_guesses += 1
        return found


    def get_status(self):
        ''' Returns the current status of the game as a string.
        Returns 'won' if the guessed word matches the answer word,
        'loss' if the number of wrong guesses has reached the maximum
        allowed, and 'ongoing' otherwise. '''
        
        #         this method checks the status of the game
        if self.guess_word == self.answer_word:
#         if the guessed_word is same as answer word then return won
            return 'won'
        
        if self.number_wrong_guesses == self.MAX_WRONG_GUESSES:
#             if number of wrong guesses reached max wrong limit return loss
            return 'loss'

#       else return ongoing    
        else:
            return 'ongoing'


