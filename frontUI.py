# !/usr/bin/python3
# RootHash Password Manager
# Back End Script : Front UI
# Started Date : 2019.11.8
# Developed By Hirusha Fernando

'''
This is the starting script.This will handle welcome 
screen operations. Run this script to start RootHash
'''
from colorama import Fore,Style     #For Colored Text In Terminal
from colorama import init           #For Colored Text In Terminal
from art import tprint              #For Display the RootHash ASCII Art

from errors import InvalidCommandError

import Records as RCD                   #RootHash Records.py script
import Operations as OPT                #RootHash Operations.py script
import Credit as CDT                    #RootHash Credit.py script

import os
import sys

from initialize import Initializer


# Initialize colorama module
init(convert=True)

# Create Initializer instance
Root = Initializer()

# Choose random font style from above fonts
FONT = Root.FONT

# Choose random color from above colors
COLOR = Root.COLOR

# Get the user account name
user = Root.user

# This part contains path variables
SPATH = Root.SPATH        # Settings path
DPATH = Root.DPATH        # Database path

# Strating function
def main():
    if os.path.exists(DPATH):
        #R ootHash Login 
        OPT.login(COLOR, FONT, SPATH)

    else:
        # When RootHash execute first time in a computer, this will run
        Root.first_time()

def UserOptions():
    
    # Clear terminal window
    os.system('CLS')     
    print('\n   ')
    # Display RootHash title as ASCII art
    print(COLOR+Style.BRIGHT)
    tprint('RootHash', FONT)
    print(Fore.RESET)
    print('\n')

    # This part get the RootHash owner name from settings file
    Owner = ''

    # Open settings file
    with open(Spath, 'r') as F:
        Owner = F.read()

    k = Owner.split('\n')

    # Get owner name into variable
    Owner = k[0]

    # RootHash user options in welcome screen
    print(f' Welcome To RootHash {Owner}')
    print(' \t[1] Add New Record')
    print(' \t[2] Modify Record')
    print(' \t[3] Delete Record')
    print(' \t[4] View All Records')
    print(' \t[5] Change Root Password')
    print(' \t[6] About RootHash')
    print(' \t[7] Exit\n')
    
    try:
        # Get user command
        cmd = input('[>>] Your Command : ')

        if cmd == '1':
            RCD.new_entry(Owner, DPATH, COLOR, FONT)

        elif cmd == '2':
            RCD.modify(Owner, DPATH, COLOR, FONT)

        elif cmd == '3':
            RCD.delete_entry(Owner, DPATH, COLOR, FONT)

        elif cmd == '4':
            RCD.view_all(Owner, DPATH, COLOR, FONT)

        elif cmd == '5':
            OPT.change_mastercode(SPATH, COLOR, FONT)

        elif cmd == '6':
            CDT.about(COLOR, FONT)

        elif cmd == '7':
            sys.exit(2)

        else:
            raise InvalidCommandError("Invalid command")

    except InvalidCommandError as e:
        print(Fore.RED + '\n[!] Invalid Command')
        print(Fore.RESET)
        # Run windows PAUSE command 
        os.system('PAUSE')
        UserOptions()

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        UserOptions()


if __name__ == "__main__":
    main()
