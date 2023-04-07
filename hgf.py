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
        ''' TODO: Read the contents of the specified file and fill
        the word list. Make sure to strip the newline character from
        each word. '''
        
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

        
        ''' TODO: Replace the pass statement with code that fulfills
        purpose of the function as described in the function docstring. '''
        
    
    from hangman import Hangman
from tkinter import *
from functools import partial

class Hangman_Interface:
    ''' This class represents a graphical user interface for a game of
    Hangman. The game's internal details are managed by a separate object. '''
    
    def __init__(self, game):
        ''' Initializes the hangman GUI as a window containing a canvas,
        a word to guess, the letter buttons (in two rows), and a new
        game button. '''
        
        self.game = game
        
        self.root = Tk()
        self.root.title('Hangman')
        self.root.minsize(600, 350)
        self.root.configure(background='cyan')

        self.canvas = Canvas(self.root, width=400, height=300, background='white')
        self.canvas.pack(pady=(30, 10))

        self.current_guess = StringVar()
        self.current_guess.set(self.game.guess_word)
        guess_label = Label(self.root, textvariable=self.current_guess, font=('Courier', 42))
        guess_label.configure(background=self.root['background'])
        guess_label.pack(pady=10)
    
        letter_buttons1_frame = Frame(self.root, background=self.root['background'])
        letter_buttons1_frame.pack(pady=10)
        letter_buttons2_frame = Frame(self.root, background=self.root['background'])
        letter_buttons2_frame.pack(pady=10)

        self.letter_buttons1 = {}
        self.letter_buttons2 = {}
       
        for letter in 'abcdefghijklm':
            process_guess_partial = partial(self.process_guess, letter)
            self.letter_buttons1[letter] = Button(letter_buttons1_frame, text=letter, font=('Arial', 18),
                        background=self.root['background'], height=1, width=2, command=process_guess_partial)
            self.letter_buttons1[letter].pack(side=LEFT, padx=5)
        
        for letter in 'nopqrstuvwxyz':
            process_guess_partial = partial(self.process_guess, letter)
            self.letter_buttons2[letter] = Button(letter_buttons2_frame, text=letter, font=('Arial', 18),
                        background=self.root['background'], height=1, width=2, command=process_guess_partial)
            self.letter_buttons2[letter].pack(side=LEFT, padx=5)
    
        new_game_button = Button(self.root, text='New Game', font=('Arial', 18), height=1, width=12,
                                 command=self.start_new_game)
        new_game_button.pack(pady=30)
    
        self.draw_initial_scene()


    def draw_initial_scene(self):
        ''' Draws the initial content on the canvas. '''
        
        # Base
        self.canvas.create_rectangle(30, 270, 370, 300, fill='burlywood', outline='gray')
        self.canvas.create_line(300, 270, 300, 50, 200, 50, width=5)
        # Rope and noose
        self.canvas.create_line(200, 50, 200, 80, dash=(7, 4), fill='gray', width=2)
        self.canvas.create_oval(180, 80, 220, 130, dash=(7, 4), outline='gray', width=2)
        #Sun
        self.canvas.create_oval(-80, -80, 80, 80, fill='gold', outline='gold')


    
        ''' TODO: Draw the rope and noose, as well as the sun, to match
        the initial scene displayed in a new game. See the spec for
        screen shots. '''
    
    
    def process_guess(self, letter):
        ''' Updates the interface when the user presses a letter button. This
        is the event handler for all letter buttons.
        
        After the game object processes the letter, it updates either the guess
        word or the hangman figure, then disables the chosen button. Finally,
        it checks for a win or loss and updates accordingly. '''
        
        found = self.game.process_guess(letter)
            
        if found:
            self.current_guess.set(self.game.guess_word)
        else:
            self.update_figure()
        
        # Disable the chosen letter button
        if letter < 'n':
            self.letter_buttons1[letter]['state'] = 'disabled'
        else:
            self.letter_buttons2[letter]['state'] = 'disabled'
            
        status = self.game.get_status()
        if status != 'ongoing':
            self.disable_all_letter_buttons()
            if status == 'won':
                self.canvas.create_text(200, 285, text='You won!', font=('Arial', 28))
            else:
                self.canvas.create_text(200, 285, text='You lost!', font=('Arial', 28))
                self.canvas.delete(self.left_eye)
                self.canvas.delete(self.right_eye)
                self.canvas.create_text(194, 97, text='x', font=('Arial', 14))
                self.canvas.create_text(206, 97, text='x', font=('Arial', 14))
                self.canvas.create_text(100, 150, text='The word was', font=('Arial', 20))
                self.canvas.create_text(100, 170, text=self.game.answer_word, font=('Arial', 20))

            
                
                ''' TODO: Draw x characters as eyes and display the answer word.
                See the appropriate screen shot in the spec. '''


    def update_figure(self):
        ''' Updates the hangman figure on the canvas by adding the appropriate
        body part. It assumes all other previous body parts have already been
        drawn. '''
        
        body_parts = self.game.number_wrong_guesses  # number of body parts to display
        
        # Head
        if body_parts == 1:
            self.canvas.create_oval(180, 80, 220, 130, fill='beige', width=2)
            self.left_eye = self.canvas.create_oval(188, 95, 195, 102, fill='black') # left eye
            self.right_eye = self.canvas.create_oval(202, 95, 209, 102, fill='black') # right eye
            self.canvas.create_line(190, 115, 210, 115) # mouth
        elif body_parts == 2:
            self.canvas.create_line(200, 130, 200, 200, width=4) #torso
        

            
        ''' TODO: Add elif and else clauses that draw the appropriate body part
        based on the number of wrong guesses. See the screen shots in the spec. ''' 


    def enable_all_letter_buttons(self):
        ''' Enables all of the buttons used to guess a letter. '''
        for button in self.letter_buttons1.values():
            button['state'] = 'normal'
        for button in self.letter_buttons2.values():
            button['state'] = 'normal'


    def disable_all_letter_buttons(self):
        ''' Disables all of the buttons used to guess a letter. '''
        pass
        
        ''' TODO: Replace the pass statement with code that disables
        all letter buttons. '''


    def start_new_game(self):
        ''' Starts a new game by clearing the canvas and
        getting a new word to guess. '''
        
        self.game.new_game()
        self.canvas.delete('all')
        self.current_guess.set(self.game.guess_word)
        self.draw_initial_scene()
        self.enable_all_letter_buttons()


# Below is the main driver of the program. It is not part of
# the Hangman_Interface class.

def main():
    ''' Plays Hangman by creating a Hangman game object and
    an interface for it. '''
    
    game = Hangman('word_list.txt', 6)
    
    Hangman_Interface(game)


# The following statement prevents Web-CAT from running this
# program automatically. 
if __name__ == '__main__':
    main()
    

    
    
    
   


