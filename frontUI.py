# !/usr/bin/python3
# RootHash Password Manager
# Back End Script : Front UI
# Started Date : 2019.11.8
# Developed By Hirusha Fernando

'''
This is the starting script.This will handle welcome 
screen operations. Run this script to start RootHash
'''

from art import tprint      #For Display the RootHash ASCII Art
from random import choice   #For choose random font style from styles
import getpass as code      #For get the windows user account name
import Operations as OPT    #RootHash Operations.py script 
import os
import sys

#RootHash Title Font Styles
styles = ('isometric', 'STAR WARS', 'larry 3d', 'subzero', 'swampland', 'big', 'Epic',
          'sweet', 'speed', 'poison', 'merlin1', "fire_font's", 'colossal', 'BROADWAY')

#Choose random font style from above fonts
FONT = choice(styles)

#Get the user account name
user = code.getuser() 

#This part contains path variables
path = 'C:/Users/'
expath = "/AppData/Local/RootHash"
Spath = path+user+expath+'/settings.csv'        # Settings path
Dpath = path+user+expath                        # Database path

#Strating function
def main():
    if os.path.exists(Dpath):
        #RootHash Login 
        OPT.login()
    else:
        #When RootHash execute first time in a computer, this will run
        OPT.first_time()


def UserOptions():
    # Clear terminal window
    os.system('CLS')     
    print('\n   ')
    # Display RootHash title as ASCII art
    tprint('RootHash', FONT)
    print('\n')

    #This part get the RootHash owner name from settings file
    Owner = None
    # Open settings file
    with open(Spath, 'r') as F:
        Owner = F.read()
    k = Owner.split('\n')
    # Get owner name into variable
    Owner = k[0]

    #RootHash user options in welcome screen
    print(f'Welcome To RootHash {Owner}')
    print('[1] Add New Record')
    print('[2] Modify Record')
    print('[3] Delete Record')
    print('[4] View All Records')
    print('[5] Change Root Password')
    print('[6] About RootHash')
    print('[7] Exit')
    try:
        # Get user command
        cmd = input('[>>] ')

        if cmd == '1':
            OPT.new_entry(Owner)
        elif cmd == '2':
            OPT.modify(Owner)
        elif cmd == '3':
            OPT.delete_entry(Owner)
        elif cmd == '4':
            OPT.view_all(Owner)
        elif cmd == '5':
            OPT.change_mastercode()
        elif cmd == '6':
            OPT.about()
        elif cmd == '7':
            sys.exit(2)
        else:
            print('Invalid Command.')
            # Run windows PAUSE command 
            os.system('PAUSE')
            UserOptions()
    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        UserOptions()


if __name__ == "__main__":
    main()
