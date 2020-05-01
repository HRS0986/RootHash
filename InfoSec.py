# !/usr/bin/python3
# RootHash Password Manager
# Back End Script : Encryption Module
# Started Date : 2019.11.11
# Developed By Hirusha Fernando

'''
This script will handle password and username 
records encryption and decryption.
'''

import random as rm

def Encode(msg):
    # msg is the text to encrypt

    # Generate a random number between 60 and 125
    rnum = rm.randint(60, 125)  
    tp = enc = ''

    # Add int(317) and rnum to each character's ASCII value in msg
    # After that convert that value into string and add it to variable named tp
    for i in msg:
        tp += str(ord(i)+317+rnum)

    for i in tp:
        # Add zero or one random character after each character in msg
        for j in range(rm.randint(0, 1)):
            # Generate a character ASCII value between 65 and 122 and add it to variable named enc
            enc += chr(rm.randint(65, 122))
        # After every iteration add a character in tp to enc
        enc += i
    # Finally add the character of ASCII valued rnum to end of the enc
    ans = enc+chr(rnum)
    # Reversed the ans text
    HASH = ans[::-1]
    # Return encrypted text
    return HASH


def Decode(HASH):
    # HASH is the text to decrypt

    dec = tp = ''

    # Loop variable
    i = 0

    # Reverse characters in HASH
    msg = HASH[::-1]

    # Get the HASH's last character's ASCII value
    # This chcracter's ASCII value is the random number, added in encryption progress (rnum in encryption)
    dch = ord(msg[-1])

    # Loop through the characters in msg
    while (i < len(msg)):
        # Check, if the character is a digit
        if msg[i].isdigit():
            # Add the character to variable named tp
            tp += msg[i]
            # Check the length of tp is eq to 3
            if len(tp) == 3:
                # Subtract int(317) and int(dch) from int(tp)
                # After that get the ASCII character of above value
                # Add it into a variable named dec
                dec += chr(int(tp)-317-dch)
                # Set tp's value to ''
                tp = ''
        i += 1
    # Return decrypted text
    return dec
