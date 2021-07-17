#!/usr/bin/python

import sys
from game_engine import GameEngine
from collections import defaultdict

delay_scaling_factor = 200 # magic number for adjusting the text speed

engine = GameEngine() #initialize the game engine 

# figure out which argument is our game file (should be our last file)
game_file = sys.argv[-1]

# double check the user actually entered the command right and that the game file exists 
if ".game" not in game_file:
    print("Something is wrong with your command")
    print("Run the following command: python run_game.py adam.game")
    raise Exception("Command not valid")

# check game file exists and is valid 
try: 
    game_file = open(game_file)
except FileNotFoundError:
    print('game file not found check that it exists')
    raise FileNotFoundError()

sections = defaultdict(lambda: [])
current_section = ''

# parse the file and store each section 
for line in game_file.readlines():
    line = line.strip()
    if line.startswith('#'):
        section = line[1:].strip()
        current_section =  section
    else: 
        sections[current_section].append(line)    

# if all that works start the game 
states = {
    '' : engine.do_nothing,
    'talk': engine.talk,
    'question': engine.ask_question, 
}

current_state = ''
current_section = ''

play_game = True

while play_game: 
    for line in sections[current_section]:
        if line == 'kill_game': 
            play_game = False
            break;
        elif line == 'adjust_delay': 
            current_delay = engine.character_delay
            if current_delay == None: 
                current_delay = .025
            
            current_delay *= delay_scaling_factor
            
            engine.print(f'The current set delay is {current_delay} ')
            engine.print('>> ', end='')
            new_delay = float(input())
            engine.character_delay = new_delay/delay_scaling_factor

        elif line.startswith('>'): #this means change sections
            current_section = line[1:].strip()
            current_state = ''
            break;
        elif line.startswith('['): # this means state change
            current_state = line[1:-1].strip()
        else: 
            response = states[current_state](line)
            if type(response) == str:
                current_section = response
                current_state = ''
                break;
    