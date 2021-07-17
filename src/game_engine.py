import time
import os
from pyfiglet import Figlet
from image_to_ascii import url_to_ascii

from image_to_ascii import image_to_ascii

class GameEngine: 
    def __init__(self): 
        self.question_options = {}
        self.character_delay = .005
    
    def print(self, string, loc = 'left', character_delay = .025, right_side_buffer = 5, end = '\n'): 
        """ print function for the engine

        :param string: string you wanna print
        :type string: str
        :param loc: location on screen you want to print options are 'right', 'left', and 'center', defaults to 'left'
        :type loc: str, optional
        :param character_delay: num seconds beween each character, defaults to .05
        :type character_delay: float, optional
        :param right_side_buffer: num characters from right edge of screen, defaults to 5
        :type right_side_buffer: int, optional
        :param end: what to end the inputted string with, defaults to '\n'
        type end: string, optional
        """
        
        if loc != 'left':
            # figure out how big the terminal is and then print the appropriate amount of white spaces
            num_coloumns = os.get_terminal_size().columns
            needed_white_space = num_coloumns - len(string) - right_side_buffer
            if loc == 'center':
                needed_white_space /= 2

            print(' '*int(needed_white_space), end = '', flush=True)

        
        # print desired characters one by one
        for character in string: 
            print(character,end='',flush=True)
            if self.character_delay != None:
                character_delay = self.character_delay
            time.sleep(character_delay)
        print(end, end= '')


    def image(self,string):
        num_coloumns = os.get_terminal_size().columns
        ascii_image = url_to_ascii(string, int(num_coloumns/3))
        for s in ascii_image: # gotta split up the string and feed it to my print function one by one or things break
            self.print(s,character_delay=0.005, loc= 'right')

    def title(self,string): 
        f = Figlet(font='small')
        formatted_string = f.renderText(string)
        for s in formatted_string.splitlines(): # gotta split up the string and feed it to my print function one by one or things break
            self.print(s,character_delay=0.005, loc= 'center')

    def subtitle(self,string):
        self.print(string, character_delay=0.05, loc= 'center')


    def talk(self,string):
        if  string.startswith('('): # this means theres a modifier for me to do here
            modifier_end_index = string.index(')')
            modifier = string[1:modifier_end_index]
            text = string[modifier_end_index+1:]
            self.__getattribute__(modifier)(text)
        else: 
            self.print(string, loc="right")

        return True
    
    def ask_question(self,string): 
        if not string: # wait for an input and return the response 
            good_input = False
            while not good_input:
                self.print('>> ', end='')
                resp = input().strip()
                try:
                    next_section = self.question_options[int(resp)]
                    good_input = True
                except: 
                    self.print('Invalid Response, Try Again')
                    pass
                      
            self.question_options = {}
            return next_section
 
        elif string.startswith('-'): #print and format and option also save them in the game memory
            option_string = string[1:].strip()
            options =  option_string.split(':')
            text = options[0].strip()
            section = options[1].strip()

            next_option_number = len(self.question_options.keys()) + 1

            self.question_options[next_option_number] = section

            self.print(f'{next_option_number}: {text}')

        else: 
            self.print(string)

        return True

    def do_nothing(self,string):
        return True

#tests cases 
if __name__=="__main__":
    engine = GameEngine()

    engine.print('Hello, World', loc = 'right')
    engine.print('Do you like waffles?', loc = 'right')
    engine.print('Yeah I like waffles!', loc = 'left')
    engine.title('I AM LARGE')
    engine.subtitle('I am less large')
    engine.talk('hello this is the computer speaking I should be on the right side of the screen')
    