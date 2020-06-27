# !/usr/bin/python3
# RootHash Password Manager
# Back End Script : Functions
# Started Date : 2019.11.8
# Developed By Hirusha Fernando

'''
This script handles login and password operations in RootHash    
'''

from colorama import Fore,Style     #For Colored Text In Terminal
from colorama import init           #For Colored Text In Terminal

from errors import PasswordNotMatchError
from initialize import Initializer

import getpass as code              #For get the windows user account name and secure input

from errors import *                #errors.py Script
import Credit as CDT                #Credit.py Script
import initialize as ITZ            #initialize.py Script
import Records as RCD               #Records.py Script
import frontUI as FUI               #frontUI.py Script
import InfoSec                      #InfoSec.py Script

import os


# Initialize colorama module
init()

# # Choose random color from above colors
# COLOR = ITZ.COLOR

# # Choose random font style from above fonts
# FONT = ITZ.FONT

# # Get the user account name
# user = ITZ.user

# # This part contains path variables
# SPATH = ITZ.SPATH           # Settings path
# DPATH = ITZ.DPATH           # Database path


def interrupt_input(func:'function'):
    # This function is called when setting master password.
    # If master password is not matching, this function is called
    # func is a parameter that decied the running situation
    # Situations:
    #           1.Changing master password
    #           2.First time that set the master password

    try:
        # Get the command from user
        cmd = str(input('\n[!] Press 1 to start again. Press 2 to exit : '))
        # Check the running situation
        if cmd == '1':
            # Call the function related to the situation
            func()
        elif cmd == '2':
            # Exit RootHash            
            quit()
        else:
            # If user entered an invalid command this part will execute
            print(Fore.RED + '\n[!] Invalid input.')
            print(Fore.RESET)
            interrupt_input(func)

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        interrupt_input(func)


def decode_root_pw(SPATH) -> str:
    # This function is called when RootHash need to use master password
    # This will decode the encrypted master password from settings file and return the password 

    PWD = ''
    try:
        # Access to setting file
        # Read encrypted password
        with open(SPATH, 'r') as PW:
            PWD = PW.read()
        PWD = PWD.split('\n')
        # Get encrypted password
        pw = PWD[1]
        # Decode Master password and get it to variable
        pw = InfoSec.Decode(pw)
        # Return decoded password
        return pw
    # if settings file is not exsist, this part will be execute
    except FileNotFoundError:        
        Initializer().first_time()


def getpw(Owner, func:int, DPATH, COLOR, FONT) -> str:
    # This function will execute when getting password for a record from user.
    # This will return a string contain the password.
    # func is a parameter that decied which is the running situation.
    # Situations: 
    #           1.Creating new record
    #           2.Modifying exsiting record

    try:
        # Get passord from user
        password = code.getpass('[!] Enter account password : ')
        # Confirm password
        confirm = code.getpass('[!] Confirm account password : ')
        
        # Matching above two passwords
        isMatched = matchPassword(password, confirm)

        if isMatched:
            # Retrun Password
            return password

    except PasswordNotMatchError as e:
        print(Fore.RED + '\n[!] Password is not matching! Press any key to start again')
        print(Fore.RESET)
        os.system('PAUSE > nul')

        # Check the running situation.
        if func == 1:
            RCD.new_entry(Owner, DPATH, COLOR, FONT)
        else: 
            RCD.modify(Owner, DPATH, COLOR, FONT)

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        getpw(Owner, func, DPATH, COLOR, FONT)


def change_mastercode(SPATH, COLOR, FONT):
    # This function is called when changing master password
    
    try:        
        # Displays RootHash ASCII Art
        CDT.displayTitle(COLOR, FONT)

        # Get old master password from user
        opw = code.getpass('[!] Enter old root password : ')

        # Check old master password user entered above
        checkRoot(opw, SPATH)
        
        # Get new master password from user
        NewP = code.getpass('[!] Enter new root password : ')

        # Get new master password again from user
        ConfirmP = code.getpass('[!] Confirm root password : ')
        
        # Matching new master password
        matchPassword(NewP, ConfirmP)
        
        # Validate password
        ValidatePassword(NewP)
        
        Owner = ''
        # Access settings file
        with open(SPATH, 'r') as sfile:
            # Get owner name
            Owner = sfile.readline()

        # Access settings file
        with open(SPATH, 'w') as sfile:
            # Write new encrypteed master password on settings file 
            sfile.write(f'{Owner}{InfoSec.Encode(NewP)}')
            
        print(Fore.GREEN + '\n[+] Password changed successfully')
        print(Fore.RESET)
        os.system('PAUSE')
        # Return to user options screen.
        FUI.UserOptions()           

    except PasswordNotMatchError as e:
        print(Fore.RED + '\n[!] Password is not matching!')
        print(Fore.RESET)
        interrupt_input(lambda : change_mastercode(SPATH, COLOR, FONT))

    except WrongPasswordError as e:
        print(Fore.RED + '\n[!] Old root password is incorrect')
        print(Fore.RESET)
        interrupt_input(lambda : change_mastercode(SPATH, COLOR, FONT))

    except WeekPasswordError as e:
        if e.error_code == "25":            
            print(Fore.RED+Style.BRIGHT + '\n[!] Password must contains at least 1 digit')
            
        elif e.error_code == "26":
            print(Fore.RED+Style.BRIGHT + '\n[!] Password must contains at least 1 letter')

        elif e.error_code == "27":
            print(Fore.RED+Style.BRIGHT + '\n[!] Password must contains at least 8 characters')

        print(Fore.RESET)                    
        interrupt_input(lambda : change_mastercode(SPATH, COLOR, FONT))

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        change_mastercode(SPATH, COLOR, FONT)


def login(COLOR, FONT, SPATH):
    # RootHash Login function
    
    try:
        # Displays RootHash ASCII Art
        CDT.displayTitle(COLOR, FONT)
        
        # Get password as secure input
        password = code.getpass('[!] Enter root password : ')

        # Verify Password
        isCorrect = checkRoot(password, SPATH)
        
        if isCorrect:
            # Enter the RootHash
            FUI.UserOptions()

    except WrongPasswordError as e:
        # Invalid Password
        print(Fore.RED + '\n[!] Invalid root password!')
        print(Fore.RESET)
        # Run windows PAUSE command 
        os.system('PAUSE')
        login(COLOR, FONT, SPATH)

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        login(COLOR, FONT, SPATH)


def ValidatePassword(password) -> bool:
    # This function validate master password when changing or setting it
    # This will return boolean value
    
    # Check password lenght
    if len(password) < 8:
        raise WeekPasswordError(" Password's  minimum length is 8", "27")
        
    # Check, if password only contains digits
    if password.isdigit():
        raise WeekPasswordError(" Password must have at least 1 digit", "25")
        
    # Check, if password only contains letters
    if password.isalpha():
        raise WeekPasswordError(" Password must have at least 1 letter", "26")
        
    # Check if password contains ascii characters
    if password.isascii():
        return True 


def matchPassword(first, second) -> bool:
    #This function will check, if two passwords  are same

    if first != second:
        raise PasswordNotMatchError("Passowrd is not matching")
    return True

def checkRoot(password, SPATH) -> bool:
    # This function check the user input password with real password

    # Get decoded root password of RootHash from settings file
    pw = decode_root_pw(SPATH)

    if password != pw:
        raise WrongPasswordError("Password incorrect")
    return True

def validateCommand(cmds:tuple, ui:str) -> bool:
    if not ui in cmds:
        raise InvalidCommandError("Invalid command")
    return True