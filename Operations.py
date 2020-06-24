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
import getpass as code              #For get the windows user account name and secure input
import Credit as CDT                #Credit.py Script
import initialize as ITZ            #initialize.py Script
import Records as RCD               #Records.py Script
import frontUI as FUI               #frontUI.py Script
import InfoSec                      #InfoSec.py Script
import os


# Initialize colorama module
init()

# RootHash Title Font Styles
styles = ITZ.styles

# RootHash Colors
colors = ITZ.colors

# Choose random color from above colors
COLOR = ITZ.COLOR

# Choose random font style from above fonts
FONT = ITZ.FONT

# Get the user account name
user = ITZ.user

# This part contains path variables
SPATH = ITZ.SPATH           # Settings path
DPATH = ITZ.DPATH           # Database path
EPATH = ITZ.EPATH


def interrupt_input(func):
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


def decode_root_pw():
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
        ITZ.first_time()


def getpw(Owner,func):
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
        if confirm == password:
            # Retrun Password
            return password
        else:
            print(Fore.RED + '\n[!] Password is not matching! Press any key to start again')   
            print(Fore.RESET)         
            os.system('PAUSE > nul')
            # Check the running situation.
            RCD.new_entry(Owner) if func == 1 else RCD.modify(Owner)

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        getpw(Owner,func)


def change_mastercode():
    # This function is called when changing master password
    
    try:
        # Get decoded old master password from settings file
        old = decode_root_pw()

        # Displays RootHash ASCII Art
        CDT.displayTitle(COLOR, FONT)

        # Get old master password from user
        opw = code.getpass('[!] Enter old root password : ')

        # Check old master password user entered above
        if opw != old:
            print(Fore.RED + '\n[!] Old root password is incorrect')
            print(Fore.RESET)
            interrupt_input(change_mastercode)
        else:
            # Get new master password from user
            NewP = code.getpass('[!] Enter new root password : ')
            # Get new master password again from user
            ConfirmP = code.getpass('[!] Confirm root password : ')

            # Matching new master password
            if NewP != ConfirmP:
                print(Fore.RED + '\n[!] Password is not matching!')
                print(Fore.RESET)
                interrupt_input(1)
            else:
                # Validate password
                isValidated = ValidatePassword(NewP)
                if isValidated:
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
                else:
                    print(Fore.RED+Style.BRIGHT + '\n[!] Password must contains at least 8 characters')
                    print(Fore.RED+Style.BRIGHT + '[!] Password must contains at least 1 digit')
                    print(Fore.RED+Style.BRIGHT + '[!] Password must contains at least 1 letter')
                    print(Fore.RESET)                    
                    interrupt_input(change_mastercode)

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        change_mastercode()


def login():
    # RootHash Login function
    
    try:
        # Displays RootHash ASCII Art
        CDT.displayTitle(COLOR, FONT)

        # Get decoded root password of RootHash from settings file
        pw = decode_root_pw()
        # Get password as secure input
        x = code.getpass('[!] Enter root password : ')

        # Verify Password
        if x == pw:
            # Enter the RootHash
            FUI.UserOptions()
        else:
            # Invalid Password
            print(Fore.RED + '\n[!] Invalid root password!')
            print(Fore.RESET)
            # Run windows PAUSE command 
            os.system('PAUSE')
            login()

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        login()


def ValidatePassword(password):
    # This function validate master password when changing or setting it
    # This will return boolean value
    
    # Check password lenght
    if len(password) < 8:
        return False
    # Check, if password only contains digits
    elif password.isdigit():
        return False
    # Check, if password only contains letters
    elif password.isalpha():
        return False
    # Check if password contains ascii characters
    elif password.isascii():
        return True
    
