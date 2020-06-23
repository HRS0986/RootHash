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
import getpass as code              #For get the windows user account name and secure input
import tinydb as TDB                #For store data and manipulate data
import Credit as CDT                #Credit.py Script
import initialize as ITZ            #initialize.py Script
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


def view_all(Owner):
    # This function displays all records.
        
    try:
        # Get access to database.
        db = TDB.TinyDB(f'{DPATH}/{Owner}.json')
        
        # Displays RootHash ASCII Art
        CDT.displayTitle(COLOR, FONT)

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


def delete_entry(Owner):
    # When deleting an exsiting record, this function is called.
    # User may input the record id that wish to delete from databse
    try:
        # Access to database.
        db = TDB.TinyDB(f'{DPATH}/{Owner}.json')

        # Displays RootHash ASCII Art
        CDT.displayTitle(COLOR, FONT)

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


def check_ID(Owner,func):
    # This function is called when deleting or modifying record
    # This will check the id that user enterd
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
            new_entry(Owner) if func == 1 else modify(Owner)

    # This part ignores 'Ctrl+C cancel operation'
    except KeyboardInterrupt:
        getpw(Owner,func)


def new_entry(Owner):
    # This function create a new record and save the record in database.
    
    try:
        # Get access to database.
        db = TDB.TinyDB(f'{DPATH}/{Owner}.json')
        
        # Displays RootHash ASCII Art
        CDT.displayTitle(COLOR, FONT)

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


def modify(Owner):
    # This function is called when modifying an exsiting record.
    # User may input the record id that wish to modify.
            
    try:
        # Access to database
        db = TDB.TinyDB(f'{DPATH}/{Owner}.json')

        # Displays RootHash ASCII Art
        CDT.displayTitle(COLOR, FONT)

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
    
