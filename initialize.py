from colorama import Fore,Style     #For Colored Text In Terminal
from colorama import init           #For Colored Text In Terminal
from random import choice           #For choose random font style from styles
from art import tprint              #For Display the RootHash ASCII Art
import getpass as code              #For get the windows user account name and secure input
import tinydb as TDB                #For store data and manipulate data
import Credit as CDT                #Credit.py Script
import Operations as OPT            #Credit.py Script
import frontUI as FUI               #frontUI.py Script
import InfoSec                      #InfoSec.py Script
import os


# RootHash Title Font Styles
styles = ('isometric', 'STAR WARS', 'larry 3d', 'subzero', 'swampland', 'big', 'Epic',
          'sweet', 'speed', 'poison', 'merlin1', "fire_font's", 'colossal', 'BROADWAY')

# RootHash Colors
colors = (Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.MAGENTA, Fore.RED, Fore.YELLOW)

# Choose random color from above colors
COLOR = choice(colors)

# Choose random font style from above fonts
FONT = choice(styles)

# Get the user account name
user = code.getuser()

# This part contains path variables
path = 'C:/Users/'
expath = "/AppData/Local/RootHash"
SPATH = path+user+expath+'/settings.csv'        # Settings path
DPATH = path+user+expath                        # Database path
EPATH = DPATH+'/Algo.csv'


def create_settings(Owner, Password):
    # This function will be called in the first run of RootHash
    # Owner is the name of RootHash User
    # Password is the RootHash Login password

    # Get the encrypted pasword
    Password = InfoSec.Encode(Password)
    # Write encrypted password and owner name in settings.csv
    with open(SPATH, 'a') as sfile:
        sfile.write(f'{Owner}\n{Password}')
    print(Fore.GREEN + '\n[+] Password created.',end='')
    print(Fore.RESET)


def create_database(Owner):
    # This function will be called in the first run of RootHash 
    # Owner is the name of RootHash User

    # Set the path to databse 
    n = DPATH+'/'+Owner+'.json'
    
    # Create the database.The database is a .json file 
    # Database name is {owner}
    db = TDB.TinyDB(n)
    print(Fore.GREEN + '[+] Database created.')
    print(f'[+] Welcome to RootHash {Owner}.')
    print(Fore.RESET)
    os.system('PAUSE')
    
    # Return to User option screen
    FUI.UserOptions()


def first_time():
    # This function executes first run in RootHash.
    # This will set Master password and owner name for RootHash
    # Also initialize settings and databse files.
    
    try:
        # Displays RootHash ASCII Art
        CDT.displayTitle(COLOR, FONT)
        
        print('\nWelcome to RootHash.Please enter required details')
        # Get owner name for RootHash
        Owner = input('[!] Enter your name : ')

        # Validate Name
        if not Owner.isalpha():       
            print(Fore.RED+Style.BRIGHT + '\n[!] Name can only contain letters')
            print(Fore.RESET)
            os.system('PAUSE')
            os.system('CLS')
            first_time()

        print('\nEnter a new root password.This will required when you enter RootHash')
        # Get Master Password from user
        NewP = code.getpass('[!] New root password : ')
        # Get password again from user
        ConfirmP = code.getpass('[!] Confirm root password : ')
        # Verifying password
        if NewP != ConfirmP:
            print(Fore.RED+Style.BRIGHT + '\n[!] Password is not matching!')
            print(Fore.RESET)            
            OPT.interrupt_input(first_time)
        else:
            # Validate password
            isValidated = OPT.ValidatePassword(NewP)            
            if isValidated:
                try:
                    # Make RootHash directory
                    os.mkdir(DPATH)
                except FileExistsError:
                    pass
                # Create settings file
                create_settings(Owner, NewP)
                # Create database file
                create_database(Owner)
            else:
                print(Fore.RED+Style.BRIGHT + '\n[!] Password must contains at least 8 characters')
                print(Fore.RED+Style.BRIGHT + '[!] Password must contains at least 1 digit')
                print(Fore.RED+Style.BRIGHT + '[!] Password must contains at least 1 letter')
                print(Fore.RESET)
                os.system('PAUSE')
                OPT.interrupt_input(first_time)

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        first_time()
