# !/usr/bin/python3
# RootHash Password Manager
# Back End Script : Functions
# Started Date : 2019.11.8
# Developed By Hirusha Fernando

'''
This script handles all operations in RootHash
Functions Content
    >> interrupt_input    -   line 65
    >> decode_root_pw     -   line 97
    >> create_settings    -   line 116
    >> create_database    -   linw 129
    >> first_time         -   line 149
    >> view_all           -   line 185
    >> delete_entry       -   line 223
    >> check_ID           -   line 281
    >> getpw              -   line 335
    >> new_entry          -   line 363
    >> modify             -   line 413
    >> change_mastercode  -   line 493
    >> about              -   line 543
    >> login              -   line 600
    >> displayTitle      -    line 627
'''
from colorama import Fore,Style     #For Colored Text In Terminal
from colorama import init           #For Colored Text In Terminal
from art import tprint              #For Display the RootHash ASCII Art
from random import choice           #For choose random font style from styles
from time import sleep              #For make a delay in RootHash Title animation
import getpass as code              #For get the windows user account name and secure input
import tinydb as TDB                #For store data and manipulate data 
import frontUI as FUI               #frontUI.py Script
import InfoSec                      #InfoSec.py Script
import os

# Initialize colorama module
init()

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
SPATH = path+user+expath+'/settings.csv'    # Settings path
DPATH = path+user+expath                    # Database path
EPATH = DPATH+'/Algo.csv'

# This function is called when setting master password.
# If master password is not matching, this function is called
def interrupt_input(func):
    # func is a parameter that decied the running situation
    # Situations:
    #           1.Changing master password
    #           2.First time that set the master password

    try:
        # Get the command from user
        cmd = str(input('\n[!] Press 1 to start again. Press 2 to exit : '))
        # Check the running situation
        if cmd == '1':
            if func == 1:
                # Change old master password
                change_mastercode()
            elif func == 2:
                # Initialze master password
                first_time()
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

# This function is called when RootHash need to use master password
# This will decode the encrypted master password from settings file and return the password 
def decode_root_pw():
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
        first_time()

# This function will be called in the first run of RootHash
def create_settings(Owner, Password):
    # Owner is the name of RootHash User
    # Password is the RootHash Login password

    # Get the encrypted pasword
    Password = InfoSec.Encode(Password)
    # Write encrypted password and owner name in settings.csv
    with open(SPATH, 'a') as sfile:
        sfile.write(f'{Owner}\n{Password}')
    print(Fore.GREEN + '\n[+] Password created.',end='')
    print(Fore.RESET)

# This function will be called in the first run of RootHash 
def create_database(Owner):
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

# This function executes first run in RootHash.
# This will set Master password and owner name for RootHash
# Also initialize settings and databse files.
def first_time():
    try:
        # Displays RootHash ASCII Art
        displayTitle()
        
        print('\nWelcome to RootHash.Please enter required details')
        # Get owner name for RootHash
        Owner = input('[!] Enter your name : ')
        print('\nEnter a new root password.This will required when you enter RootHash')
        # Get Master Password from user
        NewP = code.getpass('[!] New root password : ')
        # Get password again from user
        ConfirmP = code.getpass('[!] Confirm root password : ')
        # Matching Passwords
        if NewP != ConfirmP:
            print(Fore.RED+Style.BRIGHT + '\n[!] Password is not matching!')
            print(Fore.RESET)
            os.system('PAUSE')
            interrupt_input(2)
        else:
            if len(NewP) >= 8:
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
                print(Fore.RESET)
                os.system('PAUSE')
                interrupt_input(2)

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        first_time()

# This function displays all records.
def view_all(Owner):
    try:
        # Get access to database.
        db = TDB.TinyDB(f'{DPATH}/{Owner}.json')
        
        # Displays RootHash ASCII Art
        displayTitle()

        print(r'====================={ ROOTHASH }====================='+'\n')
        i = 0
        # Loop through the database.
        for entry in db:
            # Record id is the Primary Key.This id is generated automatically when storing record.
            print(f' Record ID : {i}')
            i += 1
            # Loop through the record.Record is a Dictionary.
            for key, value in entry.items():
                # Decode encrypted record details.
                value = InfoSec.Decode(value)
                print(f' {key} : {value}')
            print('\n')
        print(r'====================={ ROOTHASH }====================='+'\n')
        print('\nPress 1 to Exit. Press any another key to Return Menu.')
        # Get user's command
        x = input('[>>] Your Command : ')
        if x == '1':
            # Exit RootHash
            os.system('EXIT')
        else:
            # Return to User option screen.
            FUI.UserOptions()

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        view_all(Owner)

# When deleting an exsiting record, this function is called.
# User may input the record id that wish to delete from databse
def delete_entry(Owner):
    try:
        # Access to database.
        db = TDB.TinyDB(f'{DPATH}/{Owner}.json')

        # Displays RootHash ASCII Art
        displayTitle()

        print('[!] Enter record ID for the record that you want to delete')
        print('[!] You can get the record ID from view all option')
        print('[!] Enter V for view all.Enter Q for return to menu or enter record ID for delete\n')

        # Get the record id from user and check the id is a valid id
        DeleteID = check_ID(Owner,2)

        # Loop variable
        j = 0
        # This list use to get the values of record that want to delete
        st = []

        # Loop through the database
        for i in db:
            # Check the record id is match for the id that want to delete
            if j == int(DeleteID):
                # Get the values of the record theat want to delete
                st = [v for v in i.values()]
                break
            j += 1

        # Create a database query
        # This query use to delete a record from database
        RQ = TDB.Query()
        # Delete the record
        db.remove((RQ.Account == st[0]) & (RQ.Username == st[1]) & (
            RQ.Password == st[2]) & (RQ.Note == st[3]))

        print(Fore.GREEN + '\n[+] Record deleted successfully')
        print(Fore.RESET)
        print('\nPress 1 to delete record. Press 2 to exit. Press any another key to Return Menu')

        # Get command from user.
        x = input('\n[>>] Your Command : ')
        if x == '1':
            # Delete another reocrd again
            delete_entry(Owner)
        elif x == '2':
            # Exit RootHash
            os.system('EXIT')
        else:
            # return to user options screen
            FUI.UserOptions()

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        delete_entry(Owner)

# This function is called when deleting or modifying record
# This will check the id that user enterd
def check_ID(Owner,func):
    # func is a parameter that decied the running situation
    # Situations:
    #           1.Modify reocrd
    #           2.Delete record
    try:
        # Access to database
        db = TDB.TinyDB(f'{DPATH}/{Owner}.json')

        # Get user command or record ID
        x = input('[>>] Your Command : ')
        # Check the command or record ID user enterd above 
        if x == 'V' or x == 'v':
            # View All Records
            view_all(Owner)
        elif x == 'Q' or x == 'q':
            # Return to user options screen.
            FUI.UserOptions()
        elif (x == 'V' or x == 'v') and (x == 'Q' or x == 'q') and (not x.isdigit()):
            print(Fore.RED + '\n[!] Invalid Record ID or Command.\n')
            print(Fore.RESET)
            os.system('PAUSE')
            # Check running situation
            modify(Owner) if func == 1 else delete_entry(Owner)
        else:            
            Last_Record_ID = 0
            # Loop through the database to get the last record id
            for _ in db:
                Last_Record_ID += 1
            try:
                # Validate the record id user enterd
                if int(x) <= Last_Record_ID and int(x) >= 0:
                    # Return the validated record id
                    return x
                else:
                    # This part handle invalid record id
                    print(Fore.RED + '\n[!] Invalid Record ID or Command.\n')
                    print(Fore.RESET)
                    os.system('PAUSE')
                    # Check the running situation 
                    modify(Owner) if func == 1 else delete_entry(Owner)
            except :
                print(Fore.RED + '\n[!] Invalid Record ID or Command.\n')
                print(Fore.RESET)
                os.system('PAUSE')
                # Check the running situation 
                modify(Owner) if func == 1 else delete_entry(Owner)

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        check_ID(Owner,func)

# This function will execute when getting password for a record from user.
# This will return a string contain the password.
def getpw(Owner,func):
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
            new_entry(Owner) if func == 1 else modify(Owner)

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        getpw(Owner,func)

# This function create a new record and save the record in database.
def new_entry(Owner):
    try:
        # Get access to database.
        db = TDB.TinyDB(f'{DPATH}/{Owner}.json')
        
        # Displays RootHash ASCII Art
        displayTitle()

        # Get account name from user.(Ex:- Gmail,iCloud,FB,etc....).
        account = str(input('[!] Enter account name : '))

        # Get username or email for the account from user.
        username = str(input('[!] Enter account username : '))

        # Get password for the account from user.
        password = getpw(Owner,1)

        # Get any special note about account from user.This is not required.This is an optional field.
        note = str(input('[!] Special notes(Optional) : '))

        # Encrypt details user entered above.
        account = InfoSec.Encode(account)
        username = InfoSec.Encode(username)
        password = InfoSec.Encode(password)
        note = InfoSec.Encode(note)

        # Insert encrypted details into database as new record.
        db.insert({'Account': str(account), 'Username': str(
            username), 'Password': str(password), 'Note': str(note)})
        print(Fore.GREEN + '\n[+] Account added successfully!')
        print(Fore.RESET)
        print('\nPress 1 to add new record. Press 2 to exit. Press any another key to Return Menu\n')
        # Get user's command.
        x = input('[>>] Your Command : ')
        if x == '1':
            # Create new record again.
            new_entry(Owner)
        elif x == '2':
            # Exit RootHash.
            os.system('EXIT')
        else:
            # Return to user options screen.
            FUI.UserOptions()

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        new_entry(Owner)

# This function is called when modifying an exsiting record.
#User may input the record id that wish to modify.
def modify(Owner):
    try:
        # Access to database
        db = TDB.TinyDB(f'{DPATH}/{Owner}.json')

        # Displays RootHash ASCII Art
        displayTitle()

        print('[!] Enter record ID for the record that you want to modify')
        print('[!] You can get the record ID from view all option')
        print('[!] Enter V for view all.Enter Q for return to menu or enter record ID for modify\n')
        
        # Get the record id from user and check the id is a valid id
        ModifyID = check_ID(Owner,1)
        # Create a database query
        # This query use to modify a record from database 
        RQ = TDB.Query()

        # Loop variable
        j = 0
        # This list use to store details that want to modify
        st = []
        keys = ['Account', 'Username', 'Password', 'Note']
        # Loop through the database
        for i in db:
            # Check the record id is match to the modify record id
            if j == int(ModifyID):
                # Get modify record's old values to list
                st = [v for v in i.values()]
                break
            j += 1

        # This part display the old details of the record that need to modify
        print(f'\n[!] Modify record : {ModifyID}')
        print('\n[!] Old details')
        print(f'    Record ID : {ModifyID}')
        for x, y in zip(keys, st):
            print(f'    {x} : {InfoSec.Decode(y)}')

        print('\n[!] Enter new details')
        # Get new account name from user
        account = str(input('[!] Enter account name : '))
        # Get new username for the account from user
        username = str(input('[!] Enter account username : '))
        # Get new password for the account from user
        password = getpw(Owner,2)
        note = str(input('[!] Special notes(Optional) : '))

        # Encrypt the details user entered above
        ModifyID = InfoSec.Encode(ModifyID)
        account = InfoSec.Encode(account)
        username = InfoSec.Encode(username)
        password = InfoSec.Encode(password)
        note = InfoSec.Encode(note)

        # Update the record that user wish to update
        db.update({'Account': str(account), 'Username': str(
            username), 'Password': str(password), 'Note': note}, ((RQ.Account == st[0]) & (RQ.Username == st[1]) & (RQ.Password == st[2]) & (RQ.Note == st[3])))
        
        print(Fore.GREEN + '\n[+] Reocrd updated successfully')
        print(Fore.RESET)
        print('\nPress 1 to modify record. Press 2 to exit. Press any another key to return menu')

        # Get command from user
        x = input('[>>] Your Command : ')
        if x == '1':
            # Modify another record again
            modify(Owner)
        elif x == '2':
            # Exit RootHash
            os.system('EXIT')
        else:
            # Return to user options screen
            FUI.UserOptions()

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        modify(Owner)

# This function is called when changing master password
def change_mastercode(): 
    try:
        # Get decoded old master password from settings file
        old = decode_root_pw()

        # Displays RootHash ASCII Art
        displayTitle()

        # Get old master password from user
        opw = code.getpass('[!] Enter old root password : ')

        # Validate old master password user entered above
        if opw != old:
            print(Fore.RED + '\n[!] Old root password is incorrect')
            print(Fore.RESET)
            interrupt_input(1)
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

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        change_mastercode()

# RootHash Credits Displaying
def about():
    try:
        # Set RootHash Font styles
        styles = ('isometric', 'STAR WARS', 'larry 3d', 'swampland', 'big','merlin1','amcaaa','banner3-d','arrows','heapy3d', 'BROADWAY')
        from art import tprint as T
        t = ''

        # This part handle RootHash title animation =========================
        # Clear terminal window
        os.system('CLS')
        # Wait 5 Seconds.Ignore key press 
        print(COLOR)
        sleep(1)
        for i in 'RootHash':
            os.system('CLS')
            t += i
            T(t, FONT)
            sleep(1)
        print(Fore.RESET)
        print('\n')
        print(r'{===========================================')
        sleep(1)
        print(r'[+] RootHash Password Manager')
        sleep(1)
        print(r'[+] Developed By HRS CREAtions')
        sleep(1)
        print(r'[+] Version 1.0')
        sleep(1)
        print(r'[+] heshanhfernando@gmail.com')
        sleep(1)
        print(r'===========================================}')

        t = 'RootHash'        
        for i in range(len(t), 0, -1):
            f = t[:i]
            os.system('CLS')
            print(COLOR)
            T(f, FONT)
            print(Fore.RESET)
            print('\n')
            print(r'{===========================================')
            print(r'[+] RootHash Password Manager')
            print(r'[+] Developed By HRS CREAtions')
            print(r'[+] Version 1.0')
            print(r'[+] heshanhfernando@gmail.com')
            print(r'===========================================}')
            sleep(1)
        os.system('CLS')
        sleep(1)
        # This part handle RootHash title animation =========================
        FUI.UserOptions()

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        about()

# RootHash Login
def login():
    try:
        # Displays RootHash ASCII Art
        displayTitle()

        # Get decoded root password of RootHash from settings file
        pw = decode_root_pw()
        # Get password as secure input
        x = code.getpass('[!] Enter root password : ')

        # Validate Password
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

# This function displays RootHash ASCII Art
def displayTitle():    
    # Clear terminal window     
    os.system('CLS')
    print('\n')

    # Initialize color
    print(COLOR+Style.BRIGHT)

    # Display RootHash title as ASCII art
    tprint('RootHash', FONT)

    # Reset color to default
    print(Fore.RESET)

    print('\n')