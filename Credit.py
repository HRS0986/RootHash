from time import sleep
from art import tprint
from colorama import init, Fore, Style
import frontUI as FUI
import os


# Initialize colorama module
init(convert=True)

def about(COLOR, FONT):
    # RootHash Credits Displaying
    
    try:        
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
            tprint(t, FONT)
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
            tprint(f, FONT)
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

def displayTitle(COLOR, FONT):
    # This function displays RootHash ASCII Art
    
    # Clear terminal window     
    os.system('CLS')
    print('\n')

    # Initialize color
    print(COLOR+Style.BRIGHT)

    # Display RootHash title as ASCII art
    tprint(' RootHash', FONT)

    # Reset color to default
    print(Fore.RESET)

    print('\n')
