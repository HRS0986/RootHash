from colorama import Fore,Style     #For Colored Text In Terminal
from colorama import init           #For Colored Text In Terminal
import tinydb as TDB                #For store data and manipulate data
import Credit as CDT                #Credit.py Script
import Operations as OPT            #Credit.py Script
import initialize as ITZ            #initialize.py Script
import frontUI as FUI               #frontUI.py Script
import InfoSec                      #InfoSec.py Script
import os


# RootHash Database Path
DPATH = ITZ.DPATH

# Initialize colorama module
init(convert=True)

def new_entry(Owner):
    # This function create a new record and save the record in database.
    
    try:
        # Get access to database.
        db = TDB.TinyDB(f'{DPATH}/{Owner}.json')
        
        # Displays RootHash ASCII Art
        CDT.displayTitle(ITZ.COLOR, ITZ.FONT)

        # Get account name from user.(Ex:- Gmail,iCloud,FB,etc....).
        account = str(input('[!] Enter account name : '))

        # Get username or email for the account from user.
        username = str(input('[!] Enter account username : '))

        # Get password for the account from user.
        password = OPT.getpw(Owner,1)

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
        CDT.displayTitle(ITZ.COLOR, ITZ.FONT)

        print('[!] Enter record ID for the record that you want to modify')
        print('[!] You can get the record ID from view all option')
        print('[!] Enter V for view all.Enter Q for return to menu or enter record ID for modify\n')
        
        # Get the record id from user and check the id is a valid id
        ModifyID = check_record_ID(Owner,1)
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
        username = str(input('[!] Enter account username or email : '))
        # Get new password for the account from user
        password = OPT.getpw(Owner,2)
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


def view_all(Owner):
    # This function displays all records.
        
    try:
        # Get access to database.
        db = TDB.TinyDB(f'{DPATH}/{Owner}.json')
        
        # Displays RootHash ASCII Art
        CDT.displayTitle(ITZ.COLOR, ITZ.FONT)

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
        CDT.displayTitle(ITZ.COLOR, ITZ.FONT)

        print('[!] Enter record ID for the record that you want to delete')
        print('[!] You can get the record ID from view all option')
        print('[!] Enter V for view all.Enter Q for return to menu or enter record ID for delete\n')

        # Get the record id from user and check the id is a valid id
        DeleteID = check_record_ID(Owner,2)

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


def check_record_ID(Owner,func):
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
        check_record_ID(Owner,func)